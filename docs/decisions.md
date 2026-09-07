# Decisions / 决策记录

## Repository management

Owner: admax1259. Remote: https://github.com/admax1259/SKILLS . Repository changes are synchronized through PRs. Merge, tagging, and public directory submission are separate actions.

## Replace plugin-first source layout

The owner rejected plugins/show-me/skills/show-me as the primary organization for a growing collection. Adopt stable skills/<id> paths, catalog-based categories/readiness/bundles, source records, and generated distribution. Both show-me and all 18 cursor-team-kit skills are now physically present. See architecture.md for researched alternatives and installation tradeoffs.

Native marketplace output is generated; direct registration of the source Git URL is replaced by the build installer or prebuilt ZIP. Version 0.2.0 identifies this layout change; it is not a formal published release.

## Migration discussion 1 — check-compiler-errors (pending)

Original: run checks, group failures, automatically fix high-confidence issues, retry. Proposed: check/report by default, repair when asked. Await the owner's choice before adapting the imported skill. No behavior choice has been inferred from the repository reorganization request.
