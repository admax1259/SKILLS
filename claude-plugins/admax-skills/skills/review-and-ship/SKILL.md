---
name: review-and-ship
description: Review and verify a change, fix scoped issues, and deliver focused commits through a GitHub PR or GitLab MR.
---

# Review and ship

Resolve user intent, repository instructions, actual base/head, provider/host, source and target projects, staged/unstaged edits, and existing PR/MR. Review the entire proposed diff, including packaging, generated contracts, and tests. Prioritize correctness, regressions, security, and intent fit over cosmetic changes.

Use focused tests for changed behavior. Add tests when they establish a meaningful regression boundary; do not mirror implementation or invent a passing suite when no harness exists. State environmental blockers and untested integrations.

Report evidence-backed findings with location, trigger, consequence, and severity. Repair task-scoped issues when authorized, then rerun affected verification and inspect the resulting diff. Do not expand a delivery request into an unrelated architectural rewrite. Independent review is optional when available and authorized; a single-agent review must not be described as independent.

Stage only task-owned changes and make focused commits. Preserve existing local commit history and user work. Push through an authorized transport to the correct source project. API-based transfer must verify the remote tree against the local tree, including executable modes and deletions.

Open or update the matching GitHub PR/GitLab MR, checking for duplicates first. Describe the final behavior for a reviewer without chat context; include verification and material limits. Preserve target/source distinctions for forks and explicit self-managed hosts.

Inspect current-head CI: GitHub's full PR checks, or GitLab's MR-associated pipeline and jobs. An Actions-only list omits external GitHub checks; an unrelated GitLab branch pipeline cannot prove MR readiness. No checks, stale results, and manual/pending states remain explicit. Passing checks do not establish approvals or merge authorization.

Return findings/fixes, tests, current commit, URL, and remaining checks. “Ship” here means the authorized PR/MR delivery; merging, tagging, release publication, and deployment require their own user instruction.
