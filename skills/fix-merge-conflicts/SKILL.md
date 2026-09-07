---
name: fix-merge-conflicts
description: Resolve an active Git merge, rebase, or cherry-pick conflict while preserving both sides' intent and validating the resolution.
---

# Resolve conflicts

1. Inspect git status, unmerged index entries, and the active operation. Record unrelated staged/unstaged work; do not reset, abort, stash, or start a new operation implicitly.
2. Read the common ancestor and both variants for each conflicted file. During rebase, ours/theirs refers to the rebased target and replayed commit, not necessarily the user's intuitive branch labels; inspect the actual contents.
3. Resolve intended behavior rather than choosing whichever side compiles. Keep changes scoped to the conflict. Explain ambiguity that needs a product decision before choosing a destructive interpretation.
4. Handle rename/delete and binary conflicts explicitly. For generated files and lockfiles, reconcile their source inputs and use the project's generator or dependency manager; do not install arbitrary new versions to force resolution.
5. Run relevant compilation, checks, and tests. Missing tools are a blocker, not evidence that a resolution works.
6. Confirm the unmerged index is empty after selectively staging resolved files and inspect the staged diff. Search for accidental conflict markers, distinguishing legitimate examples from unresolved content. Avoid staging unrelated files.
7. Report the active operation, resolved files, semantic choices, checks, and remaining blockers. Continue the operation or create its final commit only when included in the user's request; resolving files alone does not request a push or tag.

A successful resolution preserves both branches' requirements, not necessarily both implementations. Do not turn conflict handling into broad cleanup.
