# Decisions / 决策记录

## Repository management

Owner: admax1259. Remote: https://github.com/admax1259/SKILLS . Repository changes are synchronized through PRs. Merge, tagging, and public directory submission are separate actions.

## Replace plugin-first source layout

The owner rejected plugins/show-me/skills/show-me as the primary organization for a growing collection. Adopt stable skills/<id> paths, catalog-based categories/readiness/bundles, source records, and generated distribution. Both show-me and all 18 cursor-team-kit skills are now physically present. See architecture.md for researched alternatives and installation tradeoffs.

Native marketplace output is generated; direct registration of the source Git URL is replaced by the build installer or prebuilt ZIP. Version 0.2.0 identifies this layout change; it is not a formal published release.

## Migration discussion 1 — check-compiler-errors (accepted)

The owner accepted the recommendation: check and report by default; repair when explicitly requested or already included in the active task. Discover real repository commands, distinguish environment blockers from compiler errors, preserve existing edits, report only the checked scope, and stop unproductive retries. The compiler-checks bundle makes this skill independently installable while engineering-kit remains withheld.

Validation: a maintainer-led C/Make fixture walkthrough detected an undeclared identifier without modifying files; an explicit fixture repair passed the same command. This is a workflow rehearsal, not an independent model evaluation. Native packaging and engine installation are tracked separately.

## Migration discussion 2 — deslop (implemented)

After the compiler-check PR was merged, the owner requested continuation. Implement the proposed narrow cleanup scope: preserve behavior, necessary boundary checks and rationale; discover the comparison ref instead of assuming main; allow no changes when cleanup is unjustified. Bug repair and broad refactoring remain separate tasks. Publish independently as code-cleanup.

Maintainer rehearsal: removing a redundant comment left the Python AST identical, preserved a rationale comment and input exception handling, passed valid/invalid/null input cases, and left an unrelated file unchanged. This is not independent model evaluation. Packaging and native Codex installation are checked separately.

## Batch adaptation — 0.5.0

The owner changed the delivery process to focused local commits followed by one aggregate PR, with repository bootstrap checks. All remaining 16 skills are adapted under the accepted intent/scope/evidence principles. See migration-review.zh-CN.md and bootstrap.md.

Preserve the two inherited explicit-only review policies. Native Codex validation rejects Claude's disable-model-invocation: true, so bundles requiring that policy generate separate Codex and Claude plugin directories. Only generated Codex frontmatter removes the Claude flag; agents/openai.yaml retains allow_implicit_invocation: false. Canonical sources remain single-copy.

Package output is rebuilt in owned dist/packages/current to prevent obsolete ZIPs from entering artifact/release globs. Keep formal publication separate from a version bump.
