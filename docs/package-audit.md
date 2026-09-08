# 安装包核对 / Package audit

依据 / Specification: [Package your plugin](https://developers.openai.com/plugins/build/plugins), reviewed 2026-09-08.

## 结论 / Findings

beta.2 的必需清单已存在，隔离 Codex CLI 安装成功；不能把“用户还未完成界面添加”解释为缺少 MCP 配置。该版本的实际问题是插件根与 marketplace 根重叠，Codex 安装时还复制了嵌套 Claude 插件和安装工具。beta.3 使用独立插件目录，并给截图中的 Source、Git ref、Sparse paths 提供逐字段说明。

Beta.2 already contained required manifests and passed an isolated Codex CLI installation. Its concrete packaging issue was overlapping plugin and marketplace roots: Codex also cached the nested Claude plugin and installer. Beta.3 isolates the payloads and documents the Add plugin marketplace fields. UI installation remains a separate verification item.

## 文件要求 / File contract

| 文件 / File | 要求与处理 / Requirement and decision |
|---|---|
| `.agents/plugins/marketplace.json` | Codex source catalog; one plugin, relative source path, installation/authentication policy and category. At the outer extracted root. |
| `plugins/admax-skills/.codex-plugin/plugin.json` | Required Codex plugin manifest. Name, version, skills path and install metadata validated. |
| `plugins/admax-skills/skills/*/SKILL.md` | All reviewed workflows with resources, invocation policy and original LICENSE files. |
| `.claude-plugin/marketplace.json` | Claude source catalog; one complete plugin. |
| `claude-plugins/admax-skills/.claude-plugin/plugin.json` | Claude manifest and full skill payload, with Claude explicit-invocation metadata. |
| `.app.json`, `.mcp.json`, `hooks/` | Optional integrations. Not added: this collection has no registered MCP connection, bundled server or lifecycle hooks. Empty placeholders would not improve installation. |
| `assets/`, icon, screenshots | Optional presentation resources. No unresolved asset paths are declared. |
| `INSTALL.md` | Added: exact GUI field values for Git and local folder sources, source collision recovery, CLI alternatives and verification. |
| `scripts/check_package.py` | Added: fail packaging on broken paths/metadata, missing skills/licenses, engine inventory mismatches; optional real install in temporary CODEX_HOME. |

## 目录 / Release layout

```text
skills-<version>/                 ← Local Source 填这个目录 / Select this folder
├── .agents/plugins/marketplace.json
├── .claude-plugin/marketplace.json
├── plugins/admax-skills/
│   ├── .codex-plugin/plugin.json
│   ├── skills/                  ← 全部 19 项 / All 19
│   └── SOURCES.json
├── claude-plugins/admax-skills/
│   ├── .claude-plugin/plugin.json
│   ├── skills/                  ← 同样 19 项，生成引擎元数据 / Same 19
│   └── SOURCES.json
├── scripts/install.py
├── scripts/check_package.py
├── INSTALL.md
├── README.md
├── LICENSE
└── VERSION
```

GitHub Source 使用仓库根已有清单（source.path 为 `./`），直接引用唯一 skills 源码，官方路径规则允许这一点。Release 使用 `./plugins/admax-skills` 隔离安装载荷；生成文件不提交源码仓库。两条来源路径都需要分别测试。

Git registration uses the canonical repository-root manifest (`source.path: ./`), allowed by the documented relative-path rules. Release registration uses dedicated plugin payloads; generated files are not committed. Test both source types independently.

## 证据与边界 / Evidence and limits

- Unit tests cover a single reproducible ZIP, SHA256SUMS, extraction, source paths, missing assets, both skill inventories and engine invocation policies.
- `python3 scripts/check_package.py <extracted-root> --codex-install` registers and installs in a temporary Codex home, verifies installed version and every payload file, then removes only that temporary test home.
- Git installation must use the published version tag and verify its installed skill count separately.
- Desktop UI clicks and actual skill execution are not established by those tests. Computer Use is prohibited from controlling the Codex native app in this session. Claude CLI is absent on this machine; its manifest/installer checks do not prove Claude runtime behavior.
