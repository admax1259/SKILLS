"""Build native plugin layouts from canonical sources; never edit generated output."""
import argparse
import hashlib
import json
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
        claude_entries.append({"name": name, "source": "./plugins/" + name, "version": version})
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


def package(root=ROOT, output=None):
    root = Path(root).resolve()
    version, _ = validate(root)
    output = Path(output) if output else root / "dist" / "packages"
    output.mkdir(parents=True, exist_ok=True)
    marketplace = build_marketplace(root, output / ("marketplace-" + version))
    archives = []
    for plugin in sorted((marketplace / "plugins").iterdir()):
        dest = output / f"{plugin.name}-{version}.zip"
        write_zip(dest, plugin)
        archives.append(dest)
    dest = output / f"skills-{version}.zip"
    write_zip(dest, marketplace, f"skills-{version}/")
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
