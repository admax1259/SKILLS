"""Build native plugin layouts from canonical sources; never edit generated output."""
import argparse
import hashlib
import json
import re
import shutil
import zipfile
from pathlib import Path
from validate import ROOT, read_json, ready_bundles, validate


def write_json(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def build_marketplace(root=ROOT, destination=None):
    root = Path(root).resolve()
    version, catalog = validate(root)
    destination = Path(destination) if destination else root / "dist" / "marketplace"
    if destination.is_symlink():
        raise ValueError("Build destination cannot be a symlink")
    destination = destination.resolve()
    # Generated directories are replaceable only when owned by this builder.
    marker = destination / ".skills-build"
    if destination.exists():
        if destination.is_symlink() or not marker.is_file() or marker.read_text() != "admax-skills\n":
            raise ValueError("Refusing to replace a directory not owned by this builder")
        if destination == root or root.is_relative_to(destination):
            raise ValueError("Build destination cannot contain source repository")
        shutil.rmtree(destination)
    destination.mkdir(parents=True)
    marker.write_text("admax-skills\n")
    (destination / "VERSION").write_text(version + "\n")
    bundles = ready_bundles(catalog)
    if not bundles:
        raise ValueError("No fully reviewed bundle is available")
    entries = {e["id"]: e for e in catalog["skills"]}
    codex_entries, claude_entries = [], []
    for bundle in bundles:
        name = bundle["id"]
        plugin = destination / "plugins" / name
        sources = {}
        for member in bundle["skills"]:
            shutil.copytree(root / "skills" / member, plugin / "skills" / member)
            entry = entries[member]
            sources[member] = {"upstream_path": entry["upstream_path"],
                               **read_json(root / "sources" / (entry["source"] + ".json"))}
        write_json(plugin / "SOURCES.json", sources)
        base = {"name": name, "version": version, "description": bundle["description"],
                "author": {"name": "admax1259", "url": "https://github.com/admax1259"},
                "repository": "https://github.com/admax1259/SKILLS",
                "license": " AND ".join(sorted({s["license"] for s in sources.values()}))}
        write_json(plugin / ".claude-plugin/plugin.json", base)
        write_json(plugin / ".codex-plugin/plugin.json", {
            **base, "skills": "./skills/",
            "interface": {"displayName": name, "shortDescription": base["description"],
                          "longDescription": base["description"] + ". See SOURCES.json for attribution.",
                          "developerName": "admax1259", "category": "Productivity",
                          "capabilities": ["Write"], "defaultPrompt": ["Use the " + name + " skills."]}})
        codex_entries.append({"name": name, "source": {"source": "local", "path": "./plugins/" + name},
                              "policy": {"installation": "AVAILABLE", "authentication": "ON_INSTALL"},
                              "category": "Productivity"})
        explicit = [plugin / "skills" / member / "SKILL.md" for member in bundle["skills"]
                    if entries[member].get("invocation") == "explicit"]
        claude_source = "./plugins/" + name
        if explicit:
            # Engine metadata differs; copies exist only in generated distribution.
            claude_plugin = destination / "claude-plugins" / name
            shutil.copytree(plugin, claude_plugin)
            shutil.rmtree(claude_plugin / ".codex-plugin")
            shutil.rmtree(plugin / ".claude-plugin")
            for path in explicit:
                claude_path = claude_plugin / path.relative_to(plugin)
                claude_path.write_text(re.sub(r"^(description:.*\n)",
                                              r"\1disable-model-invocation: true\n",
                                              claude_path.read_text(encoding="utf-8"), count=1,
                                              flags=re.M), encoding="utf-8")
            claude_source = "./claude-plugins/" + name
        claude_entries.append({"name": name, "source": claude_source, "version": version})
    write_json(destination / ".agents/plugins/marketplace.json",
               {"name": "admax-skills", "interface": {"displayName": "Admax Skills"}, "plugins": codex_entries})
    write_json(destination / ".claude-plugin/marketplace.json",
               {"name": "admax-skills", "owner": {"name": "admax1259"}, "plugins": claude_entries})
    (destination / "scripts").mkdir()
    shutil.copyfile(root / "scripts/install.py", destination / "scripts/install.py")
    shutil.copyfile(root / "LICENSE", destination / "LICENSE")
    (destination / "README.md").write_text(
        "# SKILLS install package / 安装包\n\n"
        "Requires Python 3.10+ and the selected engine CLI. / 需要 Python 3.10+ 与对应引擎 CLI。\n\n"
        "Run from this directory / 在本目录执行：\n\n"
        "    python3 scripts/install.py --engine codex --bundle show-me\n\n"
        "Use --engine claude for Claude Code; --dry-run previews commands.\n"
        "Keep this directory while registered as a local marketplace. / 注册后保留此目录。\n\n"
        "Only reviewed bundles are included. / 仅包含已就绪技能包。\n"
        "Plugin licenses are beside each skill; origins are in plugins/*/SOURCES.json.\n\n"
        "Documentation / 源码与说明：https://github.com/admax1259/SKILLS\n", encoding="utf-8")
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


def build_chatgpt_plugin(root=ROOT, destination=None):
    """Build one uploadable ChatGPT plugin containing every reviewed skill."""
    root = Path(root).resolve()
    version, catalog = validate(root)
    destination = Path(destination) if destination else root / "dist" / "chatgpt-plugin"
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
    (destination / "README.md").write_text(
        "# Admax Skills for ChatGPT\n\n"
        "Upload this plugin directory or its ZIP in ChatGPT. It contains every reviewed skill.\n"
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
    chatgpt = build_chatgpt_plugin(root, output / ("chatgpt-plugin-" + version))
    archives = []
    for plugin in sorted((marketplace / "plugins").iterdir()):
        suffix = "" if (plugin / ".claude-plugin").exists() else "-codex"
        dest = output / f"{plugin.name}{suffix}-{version}.zip"
        write_zip(dest, plugin)
        archives.append(dest)
    for plugin in sorted((marketplace / "claude-plugins").glob("*")):
        dest = output / f"{plugin.name}-claude-{version}.zip"
        write_zip(dest, plugin)
        archives.append(dest)
    dest = output / f"skills-{version}.zip"
    write_zip(dest, marketplace, f"skills-{version}/")
    archives.append(dest)
    dest = output / f"admax-skills-chatgpt-{version}.zip"
    write_zip(dest, chatgpt)
    archives.append(dest)
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
