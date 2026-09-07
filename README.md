# SKILLS · 个人 Agent Skills 收集器

[English](README.en.md) · [规划](docs/ROADMAP.md) · [贡献](CONTRIBUTING.md) · [版本](https://github.com/admax1259/SKILLS/releases)

收集值得复用的 skills，保留来源和授权，逐项适配，在自己的工作流中验证。一份技能内容，分别通过 Codex 和 Claude Code 插件分发。

## 当前收录

| 插件 | 用途 | 来源 | 状态 |
|---|---|---|---|
| show-me | 用 Mermaid、代码结构图、diff 或 HTML 解释当前问题 | [HumanLayer](plugins/show-me/UPSTREAM.md) · MIT | 已打包；运行验证状态见下文 |

cursor-team-kit 的 18 项技能仍在[逐项评审](docs/migration-review.zh-CN.md)，尚未作为插件分发。

## 安装

需要 Python 3.10+ 和所选引擎的 CLI。初始基础设施 PR 合并前，请使用该 PR 分支或 CI artifact；main 的安装入口在合并后才可用。

克隆仓库后，一条命令安装所选插件：

```sh
git clone https://github.com/admax1259/SKILLS.git
cd SKILLS
python3 scripts/install.py --engine codex --plugin show-me
# 或者：
python3 scripts/install.py --engine claude --plugin show-me
```

加 `--dry-run` 只显示将运行的命令。安装器向所选引擎注册本地 marketplace，再调用原生安装命令；它不直接覆盖技能目录。已有同名 marketplace 的冲突由引擎处理，失败时不会继续下一步。保留克隆/解压目录，供本地 marketplace 更新使用。

也可以在 Claude Code 对话中使用：

```text
/plugin marketplace add admax1259/SKILLS
/plugin install show-me@admax-skills
/show-me:show-me 请用图解释这段代码
```

Codex 原生命令：

```sh
codex plugin marketplace add admax1259/SKILLS
codex plugin add show-me@admax-skills
```

安装后开启新会话，用 `$show-me` 请求可视化解释；Claude Code 使用 `/show-me:show-me`。已经手动安装过同名独立 skill 时，请确认其来源后自行移除旧副本，避免重复发现。

## 下载 ZIP 后本地安装

从 [Actions](https://github.com/admax1259/SKILLS/actions) 的成功运行下载 `skills-packages-<commit>` artifact，或从 [Releases](https://github.com/admax1259/SKILLS/releases) 下载正式版本。

- `skills-<version>.zip`：完整 marketplace，解压后进入 `skills-<version>`，执行上面的 Python 安装命令，无需 Git。
- `show-me-<version>.zip`：单插件 ZIP，根目录包含两种 manifest；适用于明确支持插件 ZIP 的导入入口，不是 marketplace 根目录。
- `SHA256SUMS`：下载文件的 SHA-256。macOS 用 `shasum -a 256 -c SHA256SUMS`，Linux 用 `sha256sum -c SHA256SUMS`；Windows 可用 `Get-FileHash -Algorithm SHA256` 逐个核对。

artifact 是临时构建产物，保留 30 天；正式版本资产走独立 Release 流程。首次正式版本尚未发布。

## 支持范围

| 入口/能力 | 当前范围 |
|---|---|
| Codex | 官方本地校验器通过；原生 CLI 注册和安装成功；新会话行为验证尚未完成 |
| ChatGPT Plugins | 按 OpenAI 插件格式打包；支持入口和权限取决于宿主，尚未提交公共目录或完成界面安装测试 |
| Claude Code | 提供原生 manifest、marketplace 与安装命令；当前开发机未安装 Claude CLI，运行验证待完成 |
| Claude 其他界面 | 单插件 ZIP 已生成；具体入口的导入能力尚未验证，不承诺任意 Claude 对话都能安装 |
| GitHub / GitLab 托管 | 从任意 Git 主机克隆后可本地注册；当前项目远程和 CI 在 GitHub |
| GitHub PR / GitLab MR 工作流 | 属于下一批工程 skills 的适配范围，当前 show-me 不操作 PR/MR |

模型能阅读 skill 不等于宿主提供终端、浏览器或仓库权限。纯文本/图表能力与本地 HTML 预览也需要分别验证。

## 开发与发版

```sh
python3 scripts/validate.py
python3 -m unittest discover -s tests -v
python3 scripts/package.py
```

输出在 `dist/`。每次仓库变动通过分支提交、推送和 PR 交付。CI 自动验证并打包；版本 tag 必须匹配 VERSION、位于 main 历史中，才发布 ZIP 和校验文件。详见[发版流程](docs/releases.md)。

## 授权与来源

仓库自有基础设施使用 [Apache-2.0](LICENSE)。第三方内容继续使用自己的许可证：show-me 为 [MIT](plugins/show-me/skills/show-me/LICENSE)，Copyright © 2026 HumanLayer。适配说明与固定上游版本见 [UPSTREAM.md](plugins/show-me/UPSTREAM.md)。此仓库是个人收集与适配项目，不代表原作者或任何引擎官方出品。

格式参考：[OpenAI Plugins](https://developers.openai.com/plugins/build/plugins)、[Claude Code marketplaces](https://code.claude.com/docs/en/plugin-marketplaces)。
