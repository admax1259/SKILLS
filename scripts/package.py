"""Build native plugin layouts from canonical sources; never edit generated output."""
import argparse
import hashlib
import json
import re
import shutil
import zipfile
from pathlib import Path
from validate import ROOT, read_json, validate


def write_json(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def build_marketplace(root=ROOT, destination=None):
    """One downloadable marketplace, one all-skills plugin per engine."""
    root = Path(root).resolve()
    version, catalog = validate(root)
    destination = build_codex_plugin(root, destination or root / "dist/marketplace")
    claude = destination / "claude-plugins/admax-skills"
    shutil.copytree(destination / "skills", claude / "skills")
    shutil.copyfile(destination / "SOURCES.json", claude / "SOURCES.json")
    for entry in catalog["skills"]:
        if entry["status"] == "ready" and entry.get("invocation") == "explicit":
            path = claude / "skills" / entry["id"] / "SKILL.md"
            path.write_text(re.sub(r"^(description:.*\n)",
                                  r"\1disable-model-invocation: true\n",
                                  path.read_text(encoding="utf-8"), count=1, flags=re.M),
                            encoding="utf-8")
    manifest = read_json(destination / ".codex-plugin/plugin.json")
    write_json(claude / ".claude-plugin/plugin.json",
               {key: manifest[key] for key in
                ["name", "version", "description", "author", "repository", "license"]})
    write_json(destination / ".claude-plugin/marketplace.json", {
        "name": "admax-skills", "owner": {"name": "admax1259"},
        "plugins": [{"name": "admax-skills", "version": version,
                     "source": "./claude-plugins/admax-skills"}]})
    (destination / "VERSION").write_text(version + "\n")
    (destination / "scripts").mkdir()
    shutil.copyfile(root / "scripts/install.py", destination / "scripts/install.py")
    shutil.copyfile(root / "LICENSE", destination / "LICENSE")
    (destination / "README.md").write_text(
        "# Admax Skills — complete package / 完整安装包\n\n"
        "One plugin contains every reviewed skill, including show-me and all engineering skills.\n"
        "一个插件包含全部已审核技能，包括 show-me 与全部工程技能。\n\n"
        "Extract to a permanent directory, then run / 解压到固定目录后执行：\n\n"
        "    python3 scripts/install.py --engine codex\n\n"
        "For Claude Code / Claude Code 使用：\n\n"
        "    python3 scripts/install.py --engine claude\n\n"
        "Requires Python 3.10+ and the selected engine CLI. / 需要 Python 3.10+ 与对应引擎 CLI。\n"
        "Use --dry-run to preview commands. Start a fresh session after installation.\n"
        "追加 --dry-run 预览命令；安装后开启新会话。\n\n"
        "For Codex UI installation: codex plugin marketplace add .; restart the app,\n"
        "then select Admax Skills in Plugins Directory and click Install.\n"
        "Codex 界面安装：先注册上述本地 marketplace，重启应用，在插件目录点击安装。\n"
        "This is not an MCP server URL or a verified generic ChatGPT ZIP upload.\n"
        "此包不是 MCP 服务器地址，未验证通用 ChatGPT ZIP 上传。\n\n"
        "Sources and licenses are included. Keep this extracted directory while registered.\n"
        "保留来源与许可证；注册期间请保留解压目录。\n",
        encoding="utf-8")
    return destination


def write_zip(destination, root, prefix=""):
    with zipfile.ZipFile(destination, "w", compression=zipfile.ZIP_DEFLATED) as archive:
        for path in sorted(root.rglob("*")):
            if not path.is_file():
                continue
            if path.is_symlink():
                raise ValueError("Archive cannot contain symlinks")
            name = prefix + path.relative_to(root).as_posix()
            info = zipfile.ZipInfo(name, date_time=(2026, 1, 1, 0, 0, 0))
            info.compress_type = zipfile.ZIP_DEFLATED
            info.create_system = 3
            info.external_attr = 0o100644 << 16
            archive.writestr(info, path.read_bytes())


def build_codex_plugin(root=ROOT, destination=None):
    """Build one OpenAI plugin with a local marketplace for reviewed skills."""
    root = Path(root).resolve()
    version, catalog = validate(root)
    destination = Path(destination) if destination else root / "dist" / "codex-plugin"
    if destination.is_symlink():
        raise ValueError("Build destination cannot be a symlink")
    destination = destination.resolve()
    marker = destination / ".skills-build"
    if destination.exists():
        if destination.is_symlink() or not marker.is_file() or marker.read_text() != "admax-skills\n":
            raise ValueError("Refusing to replace a directory not owned by this builder")
        if destination == root or root.is_relative_to(destination):
            raise ValueError("Build destination cannot contain source repository")
        shutil.rmtree(destination)
    destination.mkdir(parents=True)
    marker.write_text("admax-skills\n")

    ready = [entry for entry in catalog["skills"] if entry["status"] == "ready"]
    if not ready:
        raise ValueError("No reviewed skill is available")
    sources = {}
    for entry in ready:
        member = entry["id"]
        shutil.copytree(root / "skills" / member, destination / "skills" / member)
        sources[member] = {"upstream_path": entry["upstream_path"],
                           **read_json(root / "sources" / (entry["source"] + ".json"))}
    # ChatGPT uses the OpenAI invocation policy in agents/openai.yaml. Claude's
    # frontmatter flag is not accepted by OpenAI plugin ingestion.
    for path in (destination / "skills").glob("*/SKILL.md"):
        if re.search(r"^disable-model-invocation: true\s*$", path.read_text(), re.M):
            path.write_text(re.sub(r"^disable-model-invocation: true\n", "",
                                   path.read_text(encoding="utf-8"), count=1, flags=re.M),
                            encoding="utf-8")
    write_json(destination / "SOURCES.json", sources)
    manifest = read_json(root / ".codex-plugin/plugin.json")
    if manifest.get("version") != version:
        raise ValueError("Root plugin manifest version must match VERSION")
    write_json(destination / ".codex-plugin/plugin.json", manifest)
    write_json(destination / ".agents/plugins/marketplace.json",
               read_json(root / ".agents/plugins/marketplace.json"))
    (destination / "README.md").write_text(
        "# Admax Skills for Codex / Codex 安装包\n\n"
        "Extract to a permanent directory and run there / 解压到固定目录后执行：\n\n"
        "    codex plugin marketplace add .\n\n"
        "Restart the app, select Admax Skills in Plugins Directory and click Install.\n"
        "重启应用，在 Plugins Directory 选择 Admax Skills，点击安装。\n\n"
        "CLI alternative / 命令行：codex plugin add admax-skills@admax-skills\n\n"
        "This is a local marketplace, not an MCP connection. Generic ChatGPT ZIP upload is unverified.\n"
        "这是本地 marketplace，不是 MCP 连接；未验证通用 ChatGPT ZIP 上传。\n"
        "Host tools still determine which workflows can run. Sources and licenses are bundled.\n",
        encoding="utf-8")
    return destination


def package(root=ROOT, output=None):
    root = Path(root).resolve()
    version, _ = validate(root)
    output = Path(output) if output else root / "dist" / "packages" / "current"
    if output.is_symlink():
        raise ValueError("Package output cannot be a symlink")
    output = output.resolve()
    if output == root or root.is_relative_to(output):
        raise ValueError("Package output cannot contain source repository")
    marker = output / ".skills-packages"
    if output.exists():
        if not marker.is_file() or marker.read_text() != "admax-skills\n":
            raise ValueError("Refusing to replace package output not owned by this builder")
        shutil.rmtree(output)
    output.mkdir(parents=True)
    marker.write_text("admax-skills\n")
    marketplace = build_marketplace(root, output / ("marketplace-" + version))
    dest = output / f"skills-{version}.zip"
    write_zip(dest, marketplace, f"skills-{version}/")
    archives = [dest]
    checksums = output / "SHA256SUMS"
    checksums.write_text("".join(f"{hashlib.sha256(p.read_bytes()).hexdigest()}  {p.name}\n"
                                 for p in sorted(archives)), encoding="utf-8")
    return archives + [checksums]


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    for path in package(output=args.output):
        print(path)
