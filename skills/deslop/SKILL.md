---
name: deslop
description: Clean redundant or inconsistent code in the current diff while preserving behavior. Use for deslop or focused cleanup requests, not broad refactoring or unrelated bug fixes.
---

# Clean diff noise

Remove demonstrable redundancy in the requested changes. Judge code by its purpose and surrounding conventions, not by guessing whether a person or an AI wrote it. A valid outcome is no changes when the diff contains no justified cleanup.

## Establish the scope

1. Read repository instructions and inspect staged, unstaged, and untracked work. Preserve unrelated user edits.
2. Use the user's requested files or comparison ref first. For branch cleanup, resolve the target branch from available PR/MR metadata, tracking configuration, or the remote's default-branch reference; do not hard-code `main`. If these disagree and change the scope, resolve the ambiguity before editing. Without a usable base, restrict cleanup to the user's explicit files or working-tree diff and disclose that limit.
3. Inspect the branch diff from its merge base and any in-scope staged/unstaged changes. Read surrounding code and relevant callers before deciding something is redundant. Untracked files are included only when part of the requested change.

## Make justified edits

- Remove comments that merely repeat the adjacent code. Preserve explanations of intent, invariants, compatibility constraints, security decisions, and legal notices.
- Remove redundant checks only when the relevant invariant is demonstrated across callers. Preserve validation at external input boundaries and exception handling for real failure modes. Unusual style alone is not evidence that a guard or catch is unnecessary.
- Replace type escapes only when a correct type or narrowing is supported by the code. Do not substitute another assertion, suppression, or weakened compiler setting to silence an error.
- Simplify nesting only when evaluation order, side effects, cleanup, exceptions, return values, and async behavior remain equivalent. Prefer the smallest clear edit; do not introduce helpers solely to move code around.
- Match established local conventions. Avoid repository-wide formatting, unrelated renames, dependency changes, or broad abstraction work in a diff-cleanup task.

## Verify and report

Review the final diff to confirm each edit is in scope. Run the project's relevant checks for the kind of change: a meaningful behavior check for control-flow edits, type checks for type changes, or a focused diff review for comment-only edits. State unavailable checks rather than claiming equivalence from inspection alone.

Keep behavior unchanged. If you discover a bug, explain it separately and only fix it when the user's task includes that repair. If a proposed cleanup cannot be justified, leave it in place and state the uncertainty briefly.

Summarize what changed, the verification performed, and any remaining uncertainty in a few sentences. Report no changes when appropriate. Follow separately authorized repository delivery rules; this skill alone does not request commits, pushes, PR/MR comments, or history rewrites.
