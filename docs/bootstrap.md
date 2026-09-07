# Bootstrap evidence / 自举验证

Version under review: **0.5.0**. This is explicit maintainer-led use of adapted workflows on this repository, not an independent model evaluation or proof of automatic skill routing.

本次自举是当前助手主动读取并应用仓库技能：检查真实命令、审查差异、验证插件包、生成仓库 PR 的 Canvas、整理并交付一个汇总 PR。ready 表示指令已审阅适配且可分发，不代表每项均已跨引擎端到端验证。

## Executed locally / 本地执行

- Applied check-compiler-errors/run-smoke-tests command discovery: Python AST parsing passed for six script files; node --check passed for the Canvas renderer. No invented application compiler or npm smoke target.
- validate.py, catalog.py --check, and unittest discovery: 19 catalog entries and 16 regression tests. Tests cover provenance, pending-skill gating, reproducible ZIP bytes/checksums, extracted installers, invocation mapping, pagination, moving heads, missing patches, HTML escaping, and original diff line numbers.
- Applied verify-this: prior main had 3 ready skills; this catalog has 19. engineering-kit contains 18 skill entrypoints plus Canvas resources. Package eligibility is distinct from runtime behavior.
- Review of the actual diff exposed a native schema mismatch: Codex rejects Claude's explicit-only frontmatter. The build now generates separate engine variants when needed, preserving one canonical source and invocation intent. Tests verify both variants.
- Review found stale ZIPs persisting across local builds. Only builder-owned dist/packages/current is replaced; CI/release globs use this directory. Tests verify stale output removal and protection of unowned files.
- Native Codex validate_plugin.py passed for engineering-kit. The source installer installed 0.5.0; codex plugin list --json reported installed and enabled. Installation is not automatic-selection evidence.
- Applied pr-review-canvas to live [PR #4](https://github.com/admax1259/SKILLS/pull/4): collected 12 files and rechecked the head; rendered 233 diff rows. An owned headless Chrome session opened the local HTML, collapsed/reopened a file, and reported no page errors. Screenshot inspection confirmed the layout. The bundled Playwright browser was absent, so existing Chrome was used and closed afterward.

Disposable artifacts are under ignored dist/bootstrap/. No reviewed code was executed to generate the page; collection and rendering do not mutate the remote repository.

## Per-skill scope / 逐项验证范围

| Skill(s) | Evidence and limits |
|---|---|
| show-me | Previously installed native skill; current bundle built. No new independent routing evaluation. |
| check-compiler-errors, run-smoke-tests | Actual repository syntax/regression commands; broader toolchains remain task-dependent. |
| deslop, thermo-nuclear-code-quality-review | Maintainer review of changed implementation; no independent reviewer or remote approval claimed. |
| verify-this | Catalog baseline/treatment and package invariants, including extracted installer checks. |
| control-ui | Owned browser lifecycle, page rendering, interaction and screenshot inspection. |
| control-cli | Owned subprocesses and exit results; PTY/TUI behavior not exercised in this batch. |
| pr-review-canvas | Live GitHub collection/browser rendering; GitLab nested-project, rename and incomplete-diff fixtures. |
| new-branch-and-pr, review-and-ship, make-pr-easy-to-review | Topic branch, focused commits, diff review and aggregate PR preparation. Remote evidence is recorded on the PR. |
| get-pr-comments, loop-on-ci | Exercise against the aggregate PR; consult its latest status rather than this static file for live CI. |
| fix-ci | Both-provider instructions and retry bounds reviewed; no artificial remote failure created to claim repair coverage. |
| fix-merge-conflicts | Active-operation semantics reviewed; no live user merge/rebase conflict changed during this batch. |
| what-did-i-get-done, weekly-review | Identity/time/ref and shipped-vs-committed rules reviewed; no private weekly report published. |
| workflow-from-chats | Owner's explicit batch-delivery preference applied to AGENTS.md; no private chat corpus exported. |

## Compatibility boundaries / 兼容边界

- **Codex:** native validation/installation. A fresh session may be required. Automatic selection and explicit-only dispatch are not independently behavior-tested.
- **Claude Code:** native marketplace and policy-preserving plugin generated; extracted installer dry-run tested. Real installation/model behavior unverified because Claude CLI is unavailable here.
- **GitHub:** live reads; aggregate PR delivery uses the authorized connector because the local CLI account lacks write access. Remote tree identity must be verified, not inferred from API success.
- **GitLab:** documented MR/discussions/pipeline and host/fork semantics; deterministic Canvas fixtures. No authenticated live MR creation, CI repair, approval or thread resolution claimed.
- **Other ChatGPT/Claude surfaces:** artifacts provided; UI import, public listing and available tools are separate capabilities.

Provider contracts checked against [GitHub checks](https://cli.github.com/manual/gh_pr_checks), [PR files](https://docs.github.com/en/rest/pulls/pulls#list-pull-requests-files), [GitLab MRs](https://docs.gitlab.com/api/merge_requests/), [discussions](https://docs.gitlab.com/api/discussions/), [pipelines](https://docs.gitlab.com/api/pipelines/) and [glab API](https://docs.gitlab.com/cli/api/). These support instructions, not claims of live integration tests.
