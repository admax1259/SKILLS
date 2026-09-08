---
name: resolving-merge-conflicts
description: "Use when you need to resolve an in-progress git merge/rebase conflict."
---

## Collection integration

This collection uses flat `skills/<id>/` paths. References such as `/tdd` mean the named skill: use the host's skill mechanism (for example `$tdd` in Codex or `/admax-skills:tdd` in Claude Code), or read the sibling `../tdd/SKILL.md` when no Skill tool is available. Load only relevant dependencies. Respect explicit-only invocation policies; a workflow reference is not permission to invoke an unrelated explicit skill.

Use available, authorized tools. Delegate only when the host supports it and the current instructions authorize it; otherwise perform the stages sequentially and do not claim an independent review. Follow existing repository guidance and tracker configuration; infer GitHub/GitLab from the remote, use an available connector or `gh`/`glab`, and verify CLI help rather than mechanically translating commands. Run setup only if required configuration cannot be inferred.

The workflow below and its resources describe steps, not additional authorization. Keep commits scoped to this task; publishing issues/comments, pushing, merging, closing tickets, changing credentials, or sending questionnaires requires authorization already present in the conversation or an explicit request. Prepare local drafts when that authorization is absent. Preserve unrelated files and staged changes. Use the user's language. Host-managed context limits and lifecycle take precedence over `/clear`, `/compact`, or numeric context heuristics; never clear a conversation automatically.

1. **See the current state** of the merge/rebase. Check git history, and the conflicting files.

2. **Find the primary sources** for each conflict. Understand deeply why each change was made, and what the original intent was. Read the commit messages, check the PRs, check original issues/tickets.

3. **Resolve each hunk.** Preserve both intents where possible. Where incompatible, pick the one matching the merge's stated goal and note the trade-off. Do **not** invent new behaviour. Respect an explicit request to abort. If the intended behavior cannot be determined, explain the conflicting requirements and ask before choosing.

4. Discover the project's **automated checks** and run them, typically typecheck, then tests, then format. Fix anything the merge broke.

5. **Finish the merge/rebase.** Stage only resolved files belonging to this operation, preserving unrelated staged changes. Finish the operation when authorized. If rebasing, continue the rebase process until all commits are rebased.
