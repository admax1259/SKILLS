---
name: make-pr-easy-to-review
description: Improve GitHub PR or GitLab MR descriptions and review guidance while preserving code behavior and shared history.
---

# Make PR easy to review

Resolve the explicit PR/MR or current branch, provider/host, source and target projects, and base/head revisions. Inspect the full diff, commits, generated files, existing description, and verification evidence using available connectors or authenticated gh/glab.

Identify actual friction: mixed purposes, hidden generated changes, stale scope, unclear entry points, missing rationale, and undocumented test limits. Prefer a concise problem/result description, suggested reading order, and important tradeoffs. A large change may need splitting; do not hide it with a polished summary.

If editing the PR/MR is authorized, update its description through a structured API argument or newline-preserving body file. Posting comments or requesting reviewers needs corresponding authorization. Otherwise return the prepared text locally.

Do not rewrite history merely to improve reviewability. When the user explicitly requests cleanup, record the original commit and tree, check for collaborators' newer commits, and preserve a recovery ref. Work on task-owned history only. Verify the final tree equals the original unless content changes were separately requested.

Force-push only with explicit authorization, a verified remote expectation, and lease protection. If the remote moved, stop and reconcile rather than overriding it. Do not bypass hooks.

Return the changes or prepared guidance, code/tree identity evidence when history changed, and unresolved review friction. Do not claim tests ran or reviewers approved based on description text.
