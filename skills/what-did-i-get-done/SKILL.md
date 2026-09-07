---
name: what-did-i-get-done
description: Summarize a person's repository work within an explicit time window, distinguishing commits, merged changes, and deployment evidence.
---

# Summarize completed work

Resolve the user's requested dates and timezone into a concrete interval. Use a half-open interval (start inclusive, end exclusive) when filtering timestamps to avoid counting a boundary twice. State whether authored or committed time is used.

Identify the author from the user's supplied identity, repository config and .mailmap, or authorized provider data. Multiple emails, bots, squash merges, and connector commits can obscure attribution; do not attribute all repository activity to the user. If identity is ambiguous, ask or label the available evidence rather than changing git config.

Collect commits/diffs from the stated branch or default branch and requested repositories. State limits of a shallow clone, missing refs, unavailable PR/MR data, or partial date coverage. Avoid double-counting merge commits, cherry-picks, and squash equivalents.

Group meaningful changes by delivered behavior or theme. Distinguish:
- authored commits on a branch;
- changes merged into the target branch;
- releases/deployments supported by separate evidence.

A commit alone is not proof of shipping or production deployment. Exclude uncommitted work unless requested and label it separately. Do not infer motivation, business impact, or ownership from a commit title alone.

Return a concise status update, actual interval/timezone, evidence scope, and links or commit IDs for the main claims. Mention attribution gaps where they affect the result. This is a read-only workflow.
