# Decisions / 决策记录

## Repository management

Owner: admax1259. Remote: https://github.com/admax1259/SKILLS . Repository changes are synchronized through PRs. Merge, tagging, and public directory submission are separate actions.

## Replace plugin-first source layout

The owner rejected plugins/show-me/skills/show-me as the primary organization for a growing collection. Adopt stable skills/<id> paths, catalog-based categories/readiness/bundles, source records, and generated distribution. Both show-me and all 18 cursor-team-kit skills are now physically present. See architecture.md for researched alternatives and installation tradeoffs.

Native marketplace output is generated; direct registration of the source Git URL is replaced by the build installer or prebuilt ZIP. Version 0.2.0 identifies this layout change; it is not a formal published release.

## Migration discussion 1 — check-compiler-errors (accepted)

The owner accepted the recommendation: check and report by default; repair when explicitly requested or already included in the active task. Discover real repository commands, distinguish environment blockers from compiler errors, preserve existing edits, report only the checked scope, and stop unproductive retries. The compiler-checks bundle makes this skill independently installable while engineering-kit remains withheld.

Validation: a maintainer-led C/Make fixture walkthrough detected an undeclared identifier without modifying files; an explicit fixture repair passed the same command. This is a workflow rehearsal, not an independent model evaluation. Native packaging and engine installation are tracked separately.

Next discussion: deslop. Proposed scope is removing demonstrable diff noise while preserving behavior and necessary error handling; no adaptation decision has been applied yet.
