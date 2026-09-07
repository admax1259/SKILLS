---
name: fix-ci
description: Diagnose and repair failing GitHub PR or GitLab MR checks using current revision evidence and focused fixes.
---

# Fix CI

Resolve the requested repository, provider, host, PR/MR number, and current head SHA before choosing a connector or authenticated CLI. An explicit URL wins over the current checkout. A fork's source project can differ from its target. Do not change authentication to make a tool work; use another already authorized transport when available.

## Gather the failure

- GitHub: inspect the complete PR check set with a connector or `gh pr checks <number> --repo <owner/repo> --json name,bucket,state,workflow,link`. This includes checks outside Actions. For Actions, inspect the associated run's head SHA and failed job logs; follow external check links with an available authorized tool.
- GitLab: read `GET /projects/:id/merge_requests/:iid`, its MR pipelines, and jobs of the selected pipeline in that pipeline's project. Use an encoded full project path or numeric ID; keep the selected self-managed hostname. Check pipeline SHA and association with the MR; a merged-results pipeline may use a synthetic SHA. Read failing job traces, including downstream failures when relevant.
- Follow pagination. An empty check list, missing logs, skipped/manual jobs, stale pipeline, or permission error does not prove success. Distinguish optional failures from required checks using the repository's actual policy.

Identify the failing command and first actionable cause. Separate product regression, environment failure, and suspected flake. Reproduce narrowly when feasible; preserve original failure evidence.

## Repair and verify

Fix within the requested scope, then run the affected check. Do not weaken assertions, remove required checks, expose credentials, or bypass hooks to obtain green status. Avoid unrelated refactors or importing unrelated main-branch changes without establishing that they solve this failure.

When delivery is authorized, commit selective files and push through the existing authorized transport. Re-read the PR/MR head and its full checks after every push. Local passing tests do not establish remote CI success.

Use at most three focused repair cycles unless the user gives another bound. Retry a suspected transient failure at most once with evidence. Stop earlier on repeated identical failure, inaccessible logs, required manual intervention, or an unrelated failure outside scope; report the next actionable step.

Return the cause, changes, commands and results, current head SHA, remote check state, and unresolved blockers. Fixing CI does not authorize merging or releasing.
