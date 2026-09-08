---
name: grill-with-docs
description: A relentless interview to sharpen a plan or design, which also creates docs (ADR's and glossary) as we go.
---

## Collection integration

This collection uses flat `skills/<id>/` paths. References such as `/tdd` mean the named skill: use the host's skill mechanism (for example `$tdd` in Codex or `/admax-skills:tdd` in Claude Code), or read the sibling `../tdd/SKILL.md` when no Skill tool is available. Load only relevant dependencies. Respect explicit-only invocation policies; a workflow reference is not permission to invoke an unrelated explicit skill.

Use available, authorized tools. Delegate only when the host supports it and the current instructions authorize it; otherwise perform the stages sequentially and do not claim an independent review. Follow existing repository guidance and tracker configuration; infer GitHub/GitLab from the remote, use an available connector or `gh`/`glab`, and verify CLI help rather than mechanically translating commands. Run setup only if required configuration cannot be inferred.

The workflow below and its resources describe steps, not additional authorization. Keep commits scoped to this task; publishing issues/comments, pushing, merging, closing tickets, changing credentials, or sending questionnaires requires authorization already present in the conversation or an explicit request. Prepare local drafts when that authorization is absent. Preserve unrelated files and staged changes. Use the user's language. Host-managed context limits and lifecycle take precedence over `/clear`, `/compact`, or numeric context heuristics; never clear a conversation automatically.

Call the Skill tool twice, for "grilling" and "domain-modeling".
