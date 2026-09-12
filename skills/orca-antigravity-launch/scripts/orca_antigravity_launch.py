#!/usr/bin/env python3
"""Separate Antigravity cold startup from one authoritative Orca dispatch."""
import argparse
import contextlib
import fcntl
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import sys
import time
import uuid

ORCA = "/Applications/Orca.app/Contents/Resources/bin/orca"
STATE_ROOT = Path.home() / ".local/state/orca-antigravity-launch"
PROFILE = "agy-1.2.2"


class LaunchError(Exception):
    pass


def call(*args, timeout=30):
    """Keep provider output, account data and preambles in memory, never in logs."""
    try:
        result = subprocess.run([ORCA, *args, "--json"], capture_output=True,
                                text=True, timeout=timeout, check=False)
        value = json.loads(result.stdout)
    except (OSError, subprocess.TimeoutExpired, ValueError):
        raise LaunchError("Orca response unavailable; inspect the recorded operation before retrying") from None
    # Bundled guides use a direct JSON object, unlike runtime RPC envelopes.
    if args[:2] == ("skills", "get") and result.returncode == 0 and value.get("markdown"):
        return value
    if not value.get("ok"):
        code = value.get("error", {}).get("code", "unknown")
        if not re.fullmatch(r"[a-z_]+", code):
            code = "unknown"
        raise LaunchError("Orca rejected command: " + code)
    return value


def fingerprint(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True).encode()).hexdigest()


def prompt_ready(terminal):
    """Recognize only the tested post-login *rendered* initial prompt, not history."""
    if terminal.get("source") != "screen" or terminal.get("status") != "running":
        return False
    if terminal.get("draft"):
        return False
    lines = [line.strip() for line in terminal.get("tail", []) if line.strip()]
    banners = [i for i, line in enumerate(lines) if re.search(r"\bAntigravity CLI 1\.2\.2\b", line)]
    if not banners:
        return False
    lines = lines[banners[-1]:]
    # Positive post-auth account/plan and model indicators. Never persist their text.
    if len(lines) < 7 or not re.search(r"\S+@\S+\s+\(Google AI (?:Pro|Ultra)\)", lines[1]):
        return False
    if "Gemini" not in lines[2]:
        return False
    # Banner identity, account, model and cwd are data, not login/status text.
    # agy prints cwd in the fourth banner row, optionally with its ASCII logo.
    status_lines = lines[3:]
    if status_lines and re.match(r"^[▄▀\s]*(?:/|~/)\S.*$", status_lines[0]):
        status_lines = status_lines[1:]
    if re.search(r"not signed in|sign in|log(?:ging)? in|authenticat|loading|"
                 r"trust|permission (?:required|request)|allow once|running command|thinking|interrupted",
                 "\n".join(status_lines), re.I):
        return False
    if len(lines) < 5 or not lines[-1].startswith("? for shortcuts") or "Gemini" not in lines[-1]:
        return False
    border = lambda line: len(line) >= 12 and set(line) <= {"─", "━"}
    return lines[-3] == ">" and border(lines[-4]) and border(lines[-2])


def terminal_identity(meta):
    return (meta.get("handle"), meta.get("incarnationId"), meta.get("worktreeId"))


def wait_ready(handle, expected, rpc=call, clock=time.monotonic, sleep=time.sleep,
               timeout=120, stable_seconds=2, interval=0.5):
    deadline = clock() + timeout
    previous, since, samples = None, None, 0
    while clock() < deadline:
        meta = rpc("terminal", "show", "--terminal", handle)["result"]["terminal"]
        if terminal_identity(meta) != terminal_identity(expected):
            raise LaunchError("Terminal identity changed; retained without dispatch")
        valid = (meta.get("connected") is True and meta.get("writable") is True
                 and meta.get("agentIdentity") == "antigravity" and not meta.get("orphaned"))
        screen = rpc("terminal", "read", "--terminal", handle, "--screen", "--limit", "80")["result"]["terminal"]
        now = clock()
        if valid and prompt_ready(screen):
            frame = fingerprint(screen["tail"])
            if frame != previous:
                previous, since, samples = frame, now, 1
            else:
                samples += 1
            if samples >= 3 and now - since >= stable_seconds:
                return {"profile": PROFILE, "samples": samples,
                        "stableSeconds": round(now - since, 3)}
        else:
            previous, since, samples = None, None, 0
        sleep(interval)
    raise LaunchError("No supported stable post-login prompt; terminal retained, no task input sent")


class Journal:
    """One private, locked journal per Run/Task; no specs, screens or capabilities."""
    def __init__(self, run, task, root=STATE_ROOT):
        self.root = Path(root)
        self.path = self.root / (fingerprint([run, task]) + ".json")

    @contextlib.contextmanager
    def locked(self):
        self.root.mkdir(parents=True, exist_ok=True, mode=0o700)
        lock = os.open(str(self.path) + ".lock", os.O_CREAT | os.O_RDWR | os.O_NOFOLLOW, 0o600)
        try:
            try:
                fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
            except BlockingIOError:
                raise LaunchError("Another launch owns this Run/Task; no duplicate started") from None
            yield self
        finally:
            os.close(lock)

    def read(self):
        if self.path.is_symlink():
            raise LaunchError("Refusing symlink journal")
        return json.loads(self.path.read_text()) if self.path.exists() else None

    def save(self, value):
        temporary = self.path.with_suffix(".tmp")
        fd = os.open(temporary, os.O_CREAT | os.O_TRUNC | os.O_WRONLY | os.O_NOFOLLOW, 0o600)
        with os.fdopen(fd, "w") as output:
            json.dump(value, output, indent=2)
            output.write("\n")
            output.flush()
            os.fsync(output.fileno())
        os.replace(temporary, self.path)
        directory = os.open(self.root, os.O_RDONLY)
        try:
            os.fsync(directory)
        finally:
            os.close(directory)


def task_row(rpc, run, task):
    data = rpc("orchestration", "task-list", "--run", run)["result"]
    rows = [t for t in data["tasks"] if t["id"] == task and t["run_id"] == run]
    if len(rows) != 1:
        raise LaunchError("Task not found in requested Run")
    return rows[0]


def start(args, journal, rpc=call, readiness=wait_ready):
    state = journal.read()
    if state:
        if state["worktreeSelector"] != args.worktree:
            raise LaunchError("Existing attempt uses a different workspace; no duplicate started")
        # Never replay launch or dispatch after an uncertain RPC, even on restart.
        return {**state, "replayed": True}
    for guide in ("orca-cli", "orchestration"):
        rpc("skills", "get", guide)
    current = rpc("orchestration", "run-current")
    if current["result"]["run"]["id"] != args.run:
        raise LaunchError("Bind the requested Run in this coordinator terminal first")
    runtime = current["_meta"]["runtimeId"]
    row = task_row(rpc, args.run, args.task)
    if row["status"] != "ready" or row.get("dispatch_id"):
        raise LaunchError("Only a fresh ready Task can start; use official recovery for existing attempts")
    state = {"schema": 1, "run": args.run, "task": args.task,
             "worktreeSelector": args.worktree, "runtime": runtime,
             "phase": "creating", "request": str(uuid.uuid4())}
    journal.save(state)
    # terminal create lacks a durable retry identity. A lost receipt stays uncertain.
    created = rpc("terminal", "create", "--worktree", args.worktree,
                  "--title", "Antigravity " + args.task, "--command", args.agy_command)["result"]["terminal"]
    for key in ("handle", "incarnationId", "worktreeId"):
        if not created.get(key):
            raise LaunchError("Terminal creation identity is incomplete; inspect Orca before retrying")
    state.update(terminal=created["handle"], incarnation=created["incarnationId"],
                 workspace=created["worktreeId"], phase="waiting")
    journal.save(state)
    try:
        state["readiness"] = readiness(created["handle"], created, rpc=rpc, timeout=args.timeout)
        # Recheck task authority after the potentially long login, before dispatch.
        if task_row(rpc, args.run, args.task)["status"] != "ready":
            raise LaunchError("Task changed during login; terminal retained without dispatch")
        state["phase"] = "dispatching"
        journal.save(state)
        receipt = rpc("orchestration", "worker-start", "--task", args.task,
                      "--terminal", created["handle"], "--worktree", "id:" + created["worktreeId"],
                      "--run", args.run, "--retry-request", state["request"],
                      "--timeout-ms", "60000", timeout=75)["result"]
        if receipt.get("taskId") != args.task or receipt.get("runId") != args.run or not receipt.get("dispatchId"):
            raise LaunchError("Dispatch receipt identity is incomplete; inspect recorded request")
        state.update(dispatch=receipt["dispatchId"], phase="dispatched",
                     stage=receipt.get("stage"), workerState=receipt.get("state"))
        journal.save(state)
        return state
    except LaunchError:
        # Leave dispatching intact if the call may have accepted the prompt.
        if state["phase"] == "waiting":
            state["phase"] = "readiness_blocked"
            journal.save(state)
        raise


def finish(args, journal, rpc=call):
    state = journal.read()
    if not state or not state.get("dispatch"):
        raise LaunchError("No recorded dispatch; inspect status and official recovery")
    row = task_row(rpc, args.run, args.task)
    result = json.loads(row["result"]) if row.get("result") else {}
    if result.get("provenance") != "worker_report" or result.get("outcome") not in {"succeeded", "failed"}:
        raise LaunchError("No accepted worker_report; no cleanup authorized")
    worker = rpc("orchestration", "worker-show", "--dispatch", state["dispatch"])["result"]
    projection = worker.get("projection", {})
    if projection.get("taskId") != args.task or projection.get("runId") != args.run:
        raise LaunchError("Worker identity mismatch; retained")
    if projection.get("outcome") != result["outcome"] or result.get("reportedBy") != state["terminal"]:
        raise LaunchError("Settlement does not match this worker; retained")
    rpc("skills", "get", "orchestration", "--reference", "references/recovery-and-cleanup.md")
    # Orca owns resource policy; user_owned/pre-existing terminals are never closed here.
    released = rpc("orchestration", "worker-release", "--dispatch", state["dispatch"])["result"]
    state.update(outcome=result["outcome"], message=result["messageId"],
                 phase="settled", cleanup=released.get("state"),
                 cleanupReason=released.get("reason"), processAction=released.get("processAction"))
    journal.save(state)
    return state


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("action", choices=["start", "status", "finish"])
    parser.add_argument("--run", required=True)
    parser.add_argument("--task", required=True)
    parser.add_argument("--worktree", help="Exact existing Orca workspace selector")
    parser.add_argument("--agy-command", default="agy",
                        help="Explicit agy launch command; permission settings are never added implicitly")
    parser.add_argument("--timeout", type=float, default=120, help="Post-login readiness deadline in seconds")
    args = parser.parse_args()
    if not re.fullmatch(r"run_[a-zA-Z0-9]+", args.run) or not re.fullmatch(r"task_[a-zA-Z0-9]+", args.task):
        parser.error("Use runtime-issued Run and Task IDs")
    if args.action == "start" and (not args.worktree or args.timeout <= 0):
        parser.error("start requires --worktree and a positive --timeout")
    journal = Journal(args.run, args.task)
    try:
        if args.action == "status":
            result = journal.read() or {"phase": "absent"}
        else:
            with journal.locked():
                if args.action == "start":
                    result = start(args, journal)
                else:
                    result = finish(args, journal)
        print(json.dumps(result, indent=2))
        if result.get("phase") in {"creating", "waiting", "readiness_blocked", "dispatching"}:
            return 2
    except (LaunchError, OSError, ValueError, KeyError) as error:
        # Unknown data/OS errors can include paths or data; emit only controlled errors.
        message = str(error) if isinstance(error, LaunchError) else "Invalid local state or Orca response; inspect status"
        print(json.dumps({"error": message, "journal": str(journal.path)}), file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
