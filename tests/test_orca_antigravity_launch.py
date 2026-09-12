"""Synthetic contract tests: no Orca, model calls, account data or PTYs required."""
import argparse
import importlib.util
import json
from pathlib import Path
import sys
import tempfile
import unittest
from types import SimpleNamespace
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "skills/orca-antigravity-launch/scripts"


def load(name, file):
    spec = importlib.util.spec_from_file_location(name, SCRIPTS / file)
    module = importlib.util.module_from_spec(spec)
    # Keep bytecode out of the canonical skill tree and installed snapshots.
    with patch.object(sys, "dont_write_bytecode", True):
        spec.loader.exec_module(module)
    return module


launch = load("agy_launch", "orca_antigravity_launch.py")
installer = load("agy_install", "install.py")
SCREEN = {"source": "screen", "status": "running", "tail": [
    "Antigravity CLI 1.2.2", "synthetic@example.invalid (Google AI Pro)",
    "Gemini 3.8 Flash (High)", "─" * 30, ">", "─" * 30,
    "? for shortcuts     Gemini 3.8 Flash · high"]}
META = {"handle": "term_test", "incarnationId": "instance", "worktreeId": "repo::/synthetic",
        "connected": True, "writable": True, "agentIdentity": "antigravity"}


class ReadinessTests(unittest.TestCase):
    def test_positive_signed_in_prompt(self):
        self.assertTrue(launch.prompt_ready(SCREEN))
        self.assertTrue(launch.prompt_ready({**SCREEN, "tail": [
            "shell agy --dangerously-skip-permissions", *SCREEN["tail"]]}))

    def test_account_and_path_keywords_are_not_status(self):
        for cwd in ("/synthetic/authentication/trust", "▄▀▀    ▀▀▄     ~/trust/loading"):
            lines = [SCREEN["tail"][0], "trust@example.test (Google AI Pro)",
                     SCREEN["tail"][2], cwd, *SCREEN["tail"][3:]]
            self.assertTrue(launch.prompt_ready({**SCREEN, "tail": lines}))
            lines.insert(4, "Authentication required; please sign in")
            self.assertFalse(launch.prompt_ready({**SCREEN, "tail": lines}))

    def test_false_positives(self):
        changes = [
            {"source": "stream"}, {"source": "screen-unavailable"}, {"source": None},
            {"status": "exited"}, {"draft": "unsent task"},
            {"tail": ["shell", ">"]},
            {"tail": [x.replace("1.2.2", "1.3.0") for x in SCREEN["tail"]]},
            {"tail": [x for x in SCREEN["tail"] if "@" not in x]},
            {"tail": [x.replace(">", "> queued prompt") for x in SCREEN["tail"]]},
            {"tail": SCREEN["tail"] + ["Welcome, you are not signed in."]},
            {"tail": SCREEN["tail"][:3] + ["Loading authentication"] + SCREEN["tail"][3:]},
            {"tail": SCREEN["tail"][:3] + ["Trust this folder?"] + SCREEN["tail"][3:]},
            {"tail": SCREEN["tail"][:3] + ["Running command..."] + SCREEN["tail"][3:]},
        ]
        for change in changes:
            with self.subTest(change=change):
                self.assertFalse(launch.prompt_ready({**SCREEN, **change}))

    def test_login_regression_resets_stability(self):
        now, reads = [0.0], [0]
        def rpc(*args):
            if args[1] == "show":
                return {"result": {"terminal": META}}
            reads[0] += 1
            screen = SCREEN if reads[0] != 3 else {**SCREEN, "tail": ["Logging in"]}
            return {"result": {"terminal": screen}}
        result = launch.wait_ready("term_test", META, rpc=rpc, clock=lambda: now[0],
                                   sleep=lambda delay: now.__setitem__(0, now[0] + delay), timeout=10)
        self.assertGreaterEqual(now[0], 3.5)
        self.assertGreaterEqual(result["samples"], 3)

    def test_never_ready_times_out_without_input(self):
        now, calls = [0.0], []
        def rpc(*args):
            calls.append(args)
            return {"result": {"terminal": META if args[1] == "show" else {**SCREEN, "source": "stream"}}}
        with self.assertRaises(launch.LaunchError):
            launch.wait_ready("term_test", META, rpc=rpc, clock=lambda: now[0],
                              sleep=lambda d: now.__setitem__(0, now[0] + d), timeout=3)
        self.assertTrue(all(c[1] in {"read", "show"} for c in calls))

    def test_process_replacement_is_not_ready(self):
        rpc = lambda *a: {"result": {"terminal": {**META, "incarnationId": "replacement"}}}
        with self.assertRaisesRegex(launch.LaunchError, "identity changed"):
            launch.wait_ready("term_test", META, rpc=rpc)


class DispatchTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.journal = launch.Journal("run_test", "task_test", self.tmp.name)
        self.args = argparse.Namespace(run="run_test", task="task_test", worktree="path:/synthetic",
                                       agy_command="agy", timeout=10)
        self.calls, self.saved, self.lost = [], [], None

    def rpc(self, *args, **kwargs):
        self.calls.append(args)
        verb = args[1]
        if verb == "run-current":
            return {"result": {"run": {"id": "run_test"}}, "_meta": {"runtimeId": "runtime"}}
        if verb == "task-list":
            return {"result": {"tasks": [{"id": "task_test", "run_id": "run_test", "status": "ready"}]}}
        if verb == self.lost:
            raise launch.LaunchError("response lost")
        if verb == "create":
            return {"result": {"terminal": META}}
        if verb == "worker-start":
            return {"result": {"runId": "run_test", "taskId": "task_test", "dispatchId": "ctx_test",
                                "stage": "input_accepted", "state": "ready", "preamble": "PRIVATE DATA"}}
        return {}

    def run_start(self):
        with self.journal.locked():
            return launch.start(self.args, self.journal, self.rpc,
                                readiness=lambda *a, **kw: {"samples": 5, "stableSeconds": 2})

    def test_repeated_start_dispatches_once_and_does_not_store_preamble(self):
        self.assertEqual(self.run_start()["phase"], "dispatched")
        self.assertTrue(self.run_start()["replayed"])
        dispatches = [c for c in self.calls if c[1] == "worker-start"]
        self.assertEqual(len(dispatches), 1)
        self.assertIn("--terminal", dispatches[0])
        self.assertNotIn("--agent", dispatches[0])
        self.assertNotIn("PRIVATE DATA", self.journal.path.read_text())
        self.assertEqual(self.journal.path.stat().st_mode & 0o777, 0o600)

    def test_lost_create_or_dispatch_receipt_never_replays(self):
        for verb, phase in [("create", "creating"), ("worker-start", "dispatching")]:
            with self.subTest(verb=verb):
                if self.journal.path.exists():
                    self.journal.path.unlink()
                self.calls, self.lost = [], verb
                with self.assertRaises(launch.LaunchError):
                    self.run_start()
                before = list(self.calls)
                self.assertEqual(self.run_start()["phase"], phase)
                self.assertEqual(self.calls, before)

    def test_concurrent_owner_refused(self):
        with self.journal.locked():
            with self.assertRaisesRegex(launch.LaunchError, "Another launch"):
                with launch.Journal("run_test", "task_test", self.tmp.name).locked():
                    self.fail("second lock acquired")

    def test_readiness_failure_sends_no_dispatch(self):
        def blocked(*a, **kw):
            raise launch.LaunchError("not ready")
        with self.journal.locked(), self.assertRaises(launch.LaunchError):
            launch.start(self.args, self.journal, self.rpc, readiness=blocked)
        self.assertEqual(self.journal.read()["phase"], "readiness_blocked")
        self.assertNotIn("worker-start", [c[1] for c in self.calls])
        self.assertNotIn("close", [c[1] for c in self.calls])

    def test_task_already_dispatched_cannot_create_terminal(self):
        original = self.rpc
        def rpc(*args, **kw):
            value = original(*args, **kw)
            if args[1] == "task-list":
                value["result"]["tasks"][0]["status"] = "dispatched"
            return value
        with self.journal.locked(), self.assertRaises(launch.LaunchError):
            launch.start(self.args, self.journal, rpc)
        self.assertNotIn("create", [c[1] for c in self.calls])

    def test_user_owned_terminal_is_left_to_official_release_policy(self):
        self.run_start()
        calls = []
        def rpc(*args):
            calls.append(args)
            if args[1] == "task-list":
                return {"result": {"tasks": [{"id": "task_test", "run_id": "run_test", "result": json.dumps({
                    "provenance": "worker_report", "outcome": "succeeded", "reportedBy": "term_test", "messageId": "msg_test"})}]}}
            if args[1] == "worker-show":
                return {"result": {"projection": {"taskId": "task_test", "runId": "run_test", "outcome": "succeeded"}}}
            if args[1] == "worker-release":
                return {"result": {"state": "retained", "reason": "user_takeover", "processAction": "none"}}
            return {}
        with self.journal.locked():
            result = launch.finish(self.args, self.journal, rpc)
        self.assertEqual(result["cleanup"], "retained")
        self.assertFalse(any(c[0] == "terminal" for c in calls))

    def test_rejected_or_missing_report_cannot_release(self):
        self.run_start()
        with self.journal.locked(), self.assertRaises(launch.LaunchError):
            launch.finish(self.args, self.journal, self.rpc)
        self.assertNotIn("worker-release", [c[1] for c in self.calls])



class ResponseTests(unittest.TestCase):
    def test_current_guide_uses_direct_json(self):
        response = SimpleNamespace(returncode=0, stdout=json.dumps({"name": "orchestration", "markdown": "guide"}))
        with patch.object(launch.subprocess, "run", return_value=response):
            self.assertEqual(launch.call("skills", "get", "orchestration")["markdown"], "guide")

    def test_errors_do_not_echo_raw_data(self):
        response = SimpleNamespace(returncode=1, stdout=json.dumps({"ok": False,
            "error": {"code": "dispatch_capability_invalid", "message": "PRIVATE VALUE"}}))
        with patch.object(launch.subprocess, "run", return_value=response):
            with self.assertRaises(launch.LaunchError) as raised:
                launch.call("orchestration", "worker-start")
        self.assertNotIn("PRIVATE VALUE", str(raised.exception))


class InstallTests(unittest.TestCase):
    def test_install_is_idempotent_and_preserves_unrelated_paths(self):
        with tempfile.TemporaryDirectory() as directory:
            home = Path(directory)
            installer.install(SCRIPTS.parent, home)
            installer.install(SCRIPTS.parent, home)
            link = home / ".agents/skills/orca-antigravity-launch"
            self.assertTrue((link / "SKILL.md").is_file())
            self.assertTrue((home / ".local/bin/orca-antigravity-launch").is_file())
            link.unlink()
            link.mkdir()
            (link / "user.txt").write_text("keep")
            with self.assertRaises(ValueError):
                installer.install(SCRIPTS.parent, home)
            self.assertEqual((link / "user.txt").read_text(), "keep")


if __name__ == "__main__":
    unittest.main()
