# UI UX Pro Max import / 导入记录

Upstream: [nextlevelbuilder/ui-ux-pro-max-skill](https://github.com/nextlevelbuilder/ui-ux-pro-max-skill/tree/4aad0584d92131626b16d4ff4d77f0455385013c), revision `4aad0584d92131626b16d4ff4d77f0455385013c` (2.13.0), MIT, Copyright (c) 2024 Next Level Builder.

## Scope / 收录范围

Canonical path: `skills/ui-ux-pro-max/`. Import baseline: upstream `.claude/skills/ui-ux-pro-max/`.

- Complete `data/` and `references/`, including catalog, font-license and icon-provenance metadata.
- Four unchanged runtime modules: `search.py`, `core.py`, `design_system.py`, `reasoning_contract.py`.
- Adapted `SKILL.md` and copied root MIT `LICENSE`.
- Excluded CLI/npm installer, platform generators, maintainer validator/tests, screenshots and demos. No font binaries or external asset downloads are added.

完整数据随唯一插件分发，不需要再安装上游 CLI。保留所有运行时引用的数据与来源元数据；不打包维护工具或演示站。原始及适配后 SHA-256 记录在 [source manifest](../sources/ui-ux-pro-max.json)。

## Adaptations / 适配

Resolve the directory of the loaded skill, then use `python3 -B` with an absolute script path. No Claude-specific environment variable, assumed project cwd, npm dependency or network service is required. Python 3.10+ is the runtime prerequisite; Windows can use `py -3 -B` with suitable shell quoting.

Existing project design instructions, tokens, Hallmark `design.md` and saved design-system documents take precedence. Use UI UX Pro Max for focused product/UX/stack retrieval and Hallmark for composition/review when useful. Do not automatically run both workflows or create competing design systems. Chinese requests can be translated into focused English search terms, with findings explained in Chinese.

默认检索不保存文件。只读审查不使用 `--persist`；用户任务包含保存设计文档时，显式指定项目输出目录。已有文件默认不覆盖，`--force` 需要明确授权。推荐数据不能替代实际界面、键盘操作和可访问性验证。

## Validation / 验证范围

Automated regression tests build both Codex and Claude Code payloads and invoke the bundled runtime from an unrelated working directory. They check UX retrieval, Next.js guidance, design-system JSON, absence of read-only file writes, explicit persistence and preservation of edited existing documents. Generic import tests verify all recorded file hashes.

Native Codex installation is separately checked using an isolated temporary profile. Claude Code payload and Python execution checks do not constitute a live Claude Code session test. Data coverage is not evidence that every recommendation is correct for every project; Windows runtime behavior is not exercised by the macOS checks.
