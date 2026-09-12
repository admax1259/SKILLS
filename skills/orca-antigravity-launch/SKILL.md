---
name: orca-antigravity-launch
description: Launch supervised Antigravity (agy) workers reliably in Orca on macOS by waiting for a stable post-login prompt before dispatch. Use when a Codex, Grok, or other Orca coordinator starts an Antigravity task; supplements the official orchestration skill.
---

# Antigravity startup in Orca

Use the installed `~/.local/bin/orca-antigravity-launch` for a fresh Antigravity
worker in an existing local Orca workspace. This is a user-owned workaround,
not a change to Orca or its managed skills. It currently recognizes the English
Antigravity CLI 1.2.2 signed-in Google AI Pro/Ultra prompt on macOS. Unsupported
or ambiguous screens stop before dispatch.

Read the current official guides using the exact executable:

```sh
/Applications/Orca.app/Contents/Resources/bin/orca skills get orchestration --json
/Applications/Orca.app/Contents/Resources/bin/orca skills get orca-cli --json
```

Follow their coordinator authority, task specification, mailbox, settlement,
and resource ownership rules. This skill grants no permission to launch agents
outside the user's requested work. Do not use it for ownership handoffs or
remote workers.

## Start a task

Bind the intended Run in the coordinator terminal and create a unique ready
Task with the official `task-create`. Include target, change, constraints,
ownership, and observable acceptance. Then run:

```sh
~/.local/bin/orca-antigravity-launch start \
  --run <run_id> --task <task_id> --worktree <exact_existing_selector>
```

The default launch command is `agy`. If the user has selected a different agy
permission mode, pass that exact authorized command with `--agy-command`.
The helper never adds permission-bypass flags. Login and tool permission
questions remain user decisions. Do not type Enter or replay task prompts to
make a smoke test pass.

The helper creates a terminal without a task prompt, reads its current rendered
screen in memory, and waits for signed-in indicators plus an empty framed input
and shortcuts footer. It requires stable observations and matching writable
Antigravity process identity, then calls official `worker-start --terminal` once.
Orca generates and injects the valid lifecycle capability. No capability is
recovered, copied, or stored by this helper.

`dispatched` means Orca accepted dispatch input. Confirm actual completion through
an accepted `worker_done` matching both Task and Dispatch. Never infer completion
from readiness, terminal idle, or the helper's exit code.

## Resume and finish

Repeated `start` for the same Run/Task reports its existing journal with
`replayed: true`; it does not send another prompt or create another terminal.
`status --run <run_id> --task <task_id>` is read-only. A lock also excludes
concurrent invocations for the same task on this Mac.

For `creating`, `readiness_blocked`, or `dispatching`, inspect the named terminal
and official Run state. A timeout is not exit evidence. Do not delete the journal
to force another launch. Load the current recovery reference before deciding
whether to abandon, stop, or retry. `dispatching` records an official request ID;
use `orchestration request-show --request <id>` to inspect an ambiguous call.
The helper deliberately does not auto-retry ambiguous mutations.

After processing a valid completion from the coordinator mailbox:

```sh
~/.local/bin/orca-antigravity-launch finish --run <run_id> --task <task_id>
```

This verifies an accepted worker report and calls official `worker-release`.
Respect `retained`, especially `user_owned`, `pre_existing`, or unproven identity;
never substitute `terminal close` for an uncertain release. Acknowledge the whole
Delivery only after processing all its messages and resource decisions. Keep
waiting for other in-scope tasks.

## Installation and validation

Run `python3 scripts/install.py` from this skill directory. It copies an immutable
user-owned snapshot into `~/.local/share/orca-antigravity-launch/` and links the
command plus `~/.agents/skills/orca-antigravity-launch`. Codex and Grok discover
the shared user skill directory in fresh sessions. Existing unrelated paths and
official `orca-cli` / `orchestration` skills are never replaced.

Private journals under `~/.local/state/orca-antigravity-launch/` contain only
operational IDs, readiness counts and outcomes. They contain no task specs,
account identifiers, terminal output, or capabilities. Do not commit journals
or raw Orca responses. Tests use invented screens with non-personal fixtures.

See [validation and limits](references/validation.md) for the measured local
behavior and upstream reports. For new agy versions, test a separate readiness
profile before broadening the matcher; a longer fixed sleep is not a substitute.
