# Validation and limits

This is a local workaround for Orca 1.4.200 and Antigravity CLI 1.2.2, not an upstream fix.
The supported screen profile requires an English signed-in Google AI Pro/Ultra
header, a Gemini model indicator, and an empty framed input with a shortcuts
footer. Screen access, process identity, and repeated stable observations must
all pass. Login screens, trust prompts, stream fallbacks and unknown versions fail closed.

The coordinator must still validate accepted worker reports; readiness is not proof of task completion.
The helper does not automate login, change tool permissions, retry uncertain mutations,
or claim Windows, remote workers, other agy versions or every account plan is supported.

## Sources

- [Orca issue 13854](https://github.com/stablyai/orca/issues/13854) describes early input acceptance during Antigravity login and recommends separating startup from dispatch.
- [macOS report on issue 18088](https://github.com/stablyai/orca/issues/18088#issuecomment-5549808852) reports successful structured delivery on Orca 1.4.197. That report does not prove cold-start reliability on every later build.
- Current guides come from `/Applications/Orca.app/Contents/Resources/bin/orca skills get`, especially orchestration and its recovery reference.
- [Grok skill discovery](https://docs.x.ai/build/features/skills-plugins-marketplaces) includes the shared user directory `~/.agents/skills/`.

## Verification

Synthetic tests cover login and stale-screen false positives, process replacement,
readiness timeouts, concurrent invocations, lost creation/dispatch receipts, and
idempotent installation without overwriting unrelated user files.
On 2026-09-12, three independent fresh terminals in the synthetic setup-check
workspace passed through the installed helper, with separate Tasks and Dispatches:

| Check | Stable prompt observations | Accepted worker report |
|---|---:|---|
| FRESH_A | 4 over 2.049 seconds | succeeded, unique marker and ORCA_SETUP_BASELINE |
| FRESH_B | 4 over 2.095 seconds | succeeded, unique marker and ORCA_SETUP_BASELINE |
| FRESH_C | 4 over 2.098 seconds | succeeded, unique marker and ORCA_SETUP_BASELINE |

Each worker read the README and sent its own capability-authorized worker_done.
No manual Enter, UI intervention, follow-up prompt, or prompt replay was used.
A second helper invocation for FRESH_A returned the original journal without
creating a terminal or dispatch. Initial development exposed a false negative
from the echoed permission flag and a direct-JSON guide response mismatch;
both were corrected before acceptance. A further review added regressions for
account/path words such as trust and authentication; FRESH_C used that correction.

All accepted messages were processed and acknowledged. Official worker-release
classified these separately created terminals as external_terminal. B and C
were retained according to that verdict. A was closed during development before
the explicit retention correction; the shipped helper contains no terminal-close
path. It preserves external and user-owned terminals and reports retained status.

The launch command in these tests used the existing local agy permission option
explicitly. The helper defaults to plain agy and never enables that option itself.
The helper does not change Orca or Antigravity binaries or their managed skills.

The installed skill was enumerated by Orca and by grok inspect as a user skill
under ~/.agents/skills/. New Codex/Grok sessions can discover it implicitly;
this does not guarantee model selection in every future conversation.

Repository validation passed: 47 catalog entries, 43 unit tests including 16
helper tests, reproducible packaging, and the extracted package audit with an
isolated Codex CLI installation. This is not a desktop UI install test.
