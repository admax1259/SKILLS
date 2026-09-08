---
name: verify-this
description: Verify a concrete claim with fresh reproducible evidence and return VERIFIED, NOT VERIFIED, or INCONCLUSIVE.
---

# Verify a claim

Translate the claim into an observable condition and a meaningful acceptance criterion. Use the user's threshold; do not invent a favorable one after seeing the result. If the claim is ambiguous, narrow it from context or ask for the missing decision.

For a change claim, compare a baseline and treatment under the same command, inputs, environment, warmup, and measurement procedure. Use separate worktrees or disposable copies rather than overwriting the user's working tree. For an absolute claim (for example, an archive includes all 19 skills), inspect the current artifact against the stated invariant; an artificial historical baseline is unnecessary.

Choose the smallest surface that could disprove the claim:
- CLI/TUI: an existing harness, PTY transcript, exit status and timing.
- UI: an available browser harness, actual interactions, screenshots and console output.
- Code/API: a focused behavior test or a minimal reproduction.
- Performance/memory: repeated comparable measurements, distributions and confounds; one noisy timing is not proof.
- Packaging: inspect extracted bytes and run the installed entry point, not just a filename check.

Use control-cli or control-ui when available and relevant; otherwise use existing host tools. Do not claim those capabilities exist because another skill mentions them. Keep reusable artifacts in a user-approved project/output location, minimize sensitive data, and record the tested commit or artifact identity.

Verdicts:
- VERIFIED: the tested criterion is satisfied by direct evidence at the claimed scope.
- NOT VERIFIED: valid measurements contradict the claim or miss its threshold.
- INCONCLUSIVE: missing baseline for a change claim, unavailable tools, partial execution, noisy evidence, or a confound prevents a conclusion.

Report the claim, exact commands/inputs, measurements or artifact links, verdict, and limits. Distinguish manually rehearsing a workflow from evaluating an independent agent's behavior. Static schema checks cannot establish skill routing, remote writes, or cross-engine execution.
