"""Build native plugin layouts from canonical sources; never edit generated output."""
import argparse
import hashlib
import json
import re
import shutil
import zipfile
from pathlib import Path
from validate import ROOT, read_json, validate
from check_package import check


def write_json(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def build_marketplace(root=ROOT, destination=None):
    """One downloadable marketplace, one all-skills plugin per engine."""
    root = Path(root).resolve()
    version, catalog = validate(root)
    destination = prepare_destination(root, destination or root / "dist/marketplace")
    codex = build_codex_plugin(root, destination / "plugins/admax-skills")
    marketplace = read_json(root / ".agents/plugins/marketplace.json")
    marketplace["plugins"][0]["source"]["path"] = "./plugins/admax-skills"
    write_json(destination / ".agents/plugins/marketplace.json", marketplace)
    claude = destination / "claude-plugins/admax-skills"
    shutil.copytree(codex / "skills", claude / "skills")
    shutil.copyfile(codex / "SOURCES.json", claude / "SOURCES.json")
    for entry in catalog["skills"]:
        if entry["status"] == "ready" and entry.get("invocation") == "explicit":
            path = claude / "skills" / entry["id"] / "SKILL.md"
            path.write_text(re.sub(r"^(description:.*\n)",
                                  r"\1disable-model-invocation: true\n",
                                  path.read_text(encoding="utf-8"), count=1, flags=re.M),
                            encoding="utf-8")
    manifest = read_json(codex / ".codex-plugin/plugin.json")
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
    shutil.copyfile(root / "docs/INSTALL.md", destination / "README.md")
    shutil.copyfile(root / "docs/INSTALL.md", destination / "INSTALL.md")
    shutil.copyfile(root / "scripts/check_package.py", destination / "scripts/check_package.py")
    return destination


def write_zip(destination, root, prefix=""):
    with zipfile.ZipFile(destination, "w", compression=zipfile.ZIP_DEFLATED) as archive:
        for path in sorted(root.rglob("*")):
            if not path.is_file() or path.name == ".skills-build":
                continue
            if path.is_symlink():
                raise ValueError("Archive cannot contain symlinks")
            name = prefix + path.relative_to(root).as_posix()
            info = zipfile.ZipInfo(name, date_time=(2026, 1, 1, 0, 0, 0))
            info.compress_type = zipfile.ZIP_DEFLATED
            info.create_system = 3
            info.external_attr = 0o100644 << 16
            archive.writestr(info, path.read_bytes())


def prepare_destination(root, destination):
    root = Path(root).resolve()
    destination = Path(destination)
    if destination.is_symlink():
        raise ValueError("Build destination cannot be a symlink")
    destination = destination.resolve()
    if destination == root or root.is_relative_to(destination):
        raise ValueError("Build destination cannot contain source repository")
    marker = destination / ".skills-build"
    if destination.exists():
        if not marker.is_file() or marker.read_text() != "admax-skills\n":
            raise ValueError("Refusing to replace a directory not owned by this builder")
        shutil.rmtree(destination)
    destination.mkdir(parents=True)
    marker.write_text("admax-skills\n")
    return destination


def build_codex_plugin(root=ROOT, destination=None):
    """Build only the plugin payload; marketplace metadata lives outside it."""
    root = Path(root).resolve()
    version, catalog = validate(root)
    destination = prepare_destination(root, destination or root / "dist/codex-plugin")

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
        "# Admax Skills\n\nAll reviewed skills in one plugin. / 全部已审核技能。\n"
        "See SOURCES.json and skills/*/LICENSE for attribution and licenses.\n"
        "Installation / 安装：https://github.com/admax1259/SKILLS#readme\n", encoding="utf-8")
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
    check(marketplace)
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
