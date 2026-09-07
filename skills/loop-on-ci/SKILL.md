---
name: loop-on-ci
description: Watch current GitHub PR or GitLab MR checks with bounded waits, and repair failures when requested.
---

# Loop on CI

Resolve the provider, hostname, target repository, PR/MR, and head SHA from the request and repository. Prefer available connectors; otherwise use authenticated gh or glab. Monitoring alone is read-only. Repair only when requested or already authorized.

For GitHub, use the full PR checks set (`gh pr checks` or connector equivalent), including external providers, and associate individual runs with the current head. For GitLab, use the MR's pipelines and pipeline jobs, retaining pipeline project IDs, downstream checks, and MR association. Do not substitute the target branch's pipeline for the MR pipeline. A synthetic merged-results SHA needs explicit association evidence.

Inspect before waiting. Separate required failures, optional failures, pending work, manual action, cancellation, and unknown coverage. No checks is unknown, not green. Verify approvals and merge rules separately from CI.

Poll with bounded tool waits, normally 15–30 seconds and at most 10 minutes total unless the user specifies otherwise. Report meaningful changes; do not loop indefinitely or create a scheduler task unless the user requests later monitoring.

If repair is authorized, diagnose actual failed logs, apply a focused correction, run affected checks, and push using existing authorization. Limit to three repair cycles and one evidence-backed transient retry. After a new push, discard the old head's success and inspect the new head's complete check set.

Stop on current required checks passing, the wait/repair budget, repeated identical failure, required manual action, lost access, or a superseding user instruction. Report the PR/MR URL, observed SHA, checks and remaining action. Passing CI does not authorize merge or release.
