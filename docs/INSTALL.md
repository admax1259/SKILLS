# 安装完整插件 / Install the complete plugin

一个 ZIP、一个插件、全部已审核技能。Codex 与 Claude Code 共用同一个下载包。
One ZIP, one plugin, all reviewed skills; the download supports both engines.

## Codex：你截图中的 Add plugin marketplace 窗口

打开 Plugins → 添加 marketplace。在下面两种来源中选择一种填写。
Open Plugins → Add plugin marketplace. Choose one source below.

| 字段 / Field | GitHub 安装 / GitHub | Release 离线包 / Extracted Release |
|---|---|---|
| Source | `admax1259/SKILLS` | 解压后 `skills-<version>` 文件夹的绝对路径 / Absolute path to the extracted `skills-<version>` folder |
| Git ref | 所下载版本的 tag，如 `v0.6.0-beta.3` / Release tag, e.g. `v0.6.0-beta.3` | 留空 / Leave empty |
| Sparse paths | 留空 / Leave empty | 留空 / Leave empty |

点击 **Add marketplace**，选择 **Admax Skills** 来源，打开同名插件卡片，再点击 **Install**。注册来源和安装插件是两个步骤。界面未刷新时，退出并重启应用，然后新建会话。

Click **Add marketplace**, select the **Admax Skills** source, open its plugin card, then click **Install**. Registering the source and installing the plugin are separate steps. Restart the app if the directory has not refreshed; test in a new conversation.

Source 不接受 ZIP 文件路径、Release 网页地址或 ZIP 下载地址。离线包必须先解压，选含 `.agents/plugins/marketplace.json` 的外层目录，不是 `plugins/admax-skills` 子目录。Finder 默认隐藏点开头的目录，按 ⌘⇧. 可显示。

Source is a repository or local marketplace directory, not a ZIP or Release URL. Extract first and select the outer folder containing `.agents/plugins/marketplace.json`, not the inner plugin directory. Finder hides dot-directories; press Command-Shift-period to reveal them.

Sparse paths 的 `plugins/codex` 是窗口示例占位文字，不是本仓库路径；不要填入。GitHub 来源使用源码根清单，Release 包使用生成的独立插件目录，两者都提供一个完整插件。

The `plugins/codex` placeholder is not a path in this repository. Leave Sparse paths blank. The Git source uses the canonical root manifest; the Release uses dedicated generated plugin directories. Both expose one complete plugin.

## 命令行 / Command line

在解压目录执行以下之一，需要 Python 3.10+ 与对应引擎 CLI：
From the extracted directory, choose one command (Python 3.10+ and the engine CLI required):

```sh
python3 scripts/install.py --engine codex
python3 scripts/install.py --engine claude
```

仅注册 Codex 来源、保留界面点击安装：`codex plugin marketplace add .`。
To register only and finish installation in the UI: `codex plugin marketplace add .`.

Claude Code 界面：`/plugin marketplace add <解压目录绝对路径>`，然后 Discover → Admax Skills → Install。
Claude Code UI: `/plugin marketplace add <absolute-extracted-directory>`, then Discover → Admax Skills → Install.

## 已注册旧来源 / Existing source

若提示同名来源已从其他路径添加，先检查 `codex plugin marketplace list`。确认旧 `admax-skills` 属于本仓库后，用 `codex plugin marketplace remove admax-skills` 移除旧注册，再添加新来源。不要删除其他来源。移除旧来源可能影响其已安装插件，因此随后重新安装完整插件。

If the same name is registered from another path, inspect `codex plugin marketplace list`. Remove only this collection's old registration using `codex plugin marketplace remove admax-skills`, add the new source, and reinstall. Preserve unrelated sources.

## 校验 / Verify

下载 ZIP 和 SHA256SUMS 后，macOS 执行 `LC_ALL=C shasum -a 256 -c SHA256SUMS`。
On Linux use `sha256sum -c SHA256SUMS`. Retain the extracted directory while registered.

```sh
python3 scripts/check_package.py .
# Optional: real CLI install in a temporary Codex home, without changing personal plugins
python3 scripts/check_package.py . --codex-install
```

安装后 `codex plugin list` 应列出 admax-skills 与对应版本。新会话尝试 `$show-me`；Claude Code 尝试 `/admax-skills:show-me`。CLI 安装验证不代表已验证桌面点击或技能实际完成任务。

After installation, `codex plugin list` should show admax-skills and its version. Try `$show-me` in a new Codex conversation or `/admax-skills:show-me` in Claude Code. CLI installation does not prove desktop UI or workflow execution.

官方规范 / Official specification: https://developers.openai.com/plugins/build/plugins
