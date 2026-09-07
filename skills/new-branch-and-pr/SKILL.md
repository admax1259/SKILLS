---
name: new-branch-and-pr
description: Implement requested work on a topic branch and open a GitHub PR or GitLab MR with scoped commits and verification.
---

# New branch and PR

Inspect repository instructions, working tree/index, remotes, branch tracking, and existing PRs/MRs. Resolve provider and hostname, target project, source/fork project, and base from the user or repository default; do not assume main. Preserve unrelated edits. Reuse an existing task branch/request when continuing rather than creating duplicates.

Fetch the selected base. Use the user's chosen starting state; otherwise branch from the fetched default base. A dirty checkout may require an isolated worktree, without discarding/stashing user changes implicitly. Keep branch names descriptive and check collisions before creation.

Implement and verify the requested change. Inspect the full diff against the actual base, stage task-owned paths, and record focused local commits. Preserve commit hooks and repository checks; include material validation gaps.

Push to the intended source repository with an already authorized Git, connector, or CLI transport. If CLI and connector identities differ, verify repository write access for the chosen one; do not rewrite credentials. When transferring commits through an API, preserve the local history, parent order, file modes/deletions, and compare each resulting remote tree with the local tree. Do not claim a push succeeded until verified.

Find an existing open PR/MR for the exact source and target before creating one. On GitHub use a connector or gh with explicit head/base/repo. On GitLab use a connector or glab with explicit source/target projects and branches; a fork MR targets the destination project. Preserve actual newlines in descriptions with structured arguments or a body file.

Create the requested PR/MR with a concrete problem/result, review entry points, verification, and limitations. Use a draft when work remains incomplete. Do not merge, enable auto-merge, force-push, tag, or deploy merely because a PR/MR was requested.

Return the branch, verified remote commit, PR/MR URL, and check status. If remote creation fails, keep local commits and report the exact failed action and evidence without exposing credentials.
