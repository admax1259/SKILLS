"""Validate an extracted marketplace; optionally install in a temporary Codex home."""
import argparse
import json
import os
from pathlib import Path
import subprocess
import tempfile


def read_json(path):
    return json.loads(path.read_text(encoding="utf-8"))


def inside(root, value):
    if not isinstance(value, str) or not value.startswith("./"):
        raise ValueError("Component paths must start with ./")
    path = (root / value).resolve()
    if not path.is_relative_to(root.resolve()) or not path.exists():
        raise ValueError(f"Missing or escaping component: {value}")
    return path


def check(root):
    root = Path(root).resolve()
    version = (root / "VERSION").read_text().strip()
    member_sets = []
    for engine, manifest_path in [("codex", ".agents/plugins/marketplace.json"),
                                  ("claude", ".claude-plugin/marketplace.json")]:
        market = read_json(root / manifest_path)
        if market["name"] != "admax-skills" or len(market["plugins"]) != 1:
            raise ValueError("Expected one admax-skills marketplace plugin")
        entry = market["plugins"][0]
        source = entry["source"]
        if engine == "codex":
            if source["source"] != "local" or entry["policy"] != {
                "installation": "AVAILABLE", "authentication": "ON_INSTALL"
            } or not entry.get("category"):
                raise ValueError("Invalid Codex marketplace policy")
            source = source["path"]
        plugin = inside(root, source)
        if plugin == root or plugin.name != entry["name"]:
            raise ValueError("Release plugins must have a dedicated named directory")
        manifest = read_json(plugin / f".{engine}-plugin/plugin.json")
        if manifest["name"] != "admax-skills" or manifest["version"] != version:
            raise ValueError("Plugin name/version mismatch")
        skills = inside(plugin, manifest.get("skills", "./skills/"))
        sources = read_json(plugin / "SOURCES.json")
        members = {p.name for p in skills.iterdir() if p.is_dir()}
        if not members or members != set(sources):
            raise ValueError("Skills and attribution entries differ")
        for member in members:
            for filename in ["SKILL.md", "LICENSE"]:
                if not (skills / member / filename).is_file():
                    raise ValueError(f"Missing {member}/{filename}")
        for key in ["apps", "mcpServers"]:
            if isinstance(manifest.get(key), str):
                inside(plugin, manifest[key])
        interface = manifest.get("interface", {})
        for key in ["composerIcon", "logo", "logoDark"]:
            if key in interface:
                inside(plugin, interface[key])
        for value in interface.get("screenshots", []):
            inside(plugin, value)
        if (plugin / "claude-plugins").exists() or (plugin / "scripts/install.py").exists():
            raise ValueError("Installer or other engine payload leaked into plugin")
        member_sets.append(members)
    if member_sets[0] != member_sets[1]:
        raise ValueError("Engine skill inventories differ")
    return version, member_sets[0]


def install_codex(root):
    version, members = check(root)
    with tempfile.TemporaryDirectory(prefix="admax-install-check-") as temp:
        env = {**os.environ, "CODEX_HOME": temp}
        def run(*args):
            result = subprocess.run(["codex", "plugin", *args, "--json"],
                                    env=env, cwd=temp, check=True, capture_output=True, text=True)
            return json.loads(result.stdout)
        run("marketplace", "add", str(Path(root).resolve()))
        result = run("add", "admax-skills@admax-skills")
        installed = Path(result["installedPath"])
        if result["version"] != version or not installed.is_relative_to(Path(temp).resolve()):
            raise ValueError("Unexpected installed version/cache location")
        if {p.parent.name for p in installed.glob("skills/*/SKILL.md")} != members:
            raise ValueError("Installed skill inventory differs")
        source = Path(root) / "plugins/admax-skills"
        for path in source.rglob("*"):
            if path.is_file() and path.name != ".skills-build":
                if (installed / path.relative_to(source)).read_bytes() != path.read_bytes():
                    raise ValueError("Installed payload differs from extracted package")
        if (installed / "claude-plugins").exists():
            raise ValueError("Installed payload contains nested Claude plugin")
    return version, members


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("marketplace", type=Path)
    parser.add_argument("--codex-install", action="store_true")
    args = parser.parse_args()
    version, members = install_codex(args.marketplace) if args.codex_install else check(args.marketplace)
    print(f"Verified {version}: {len(members)} skills per engine; "
          + ("isolated Codex install passed (not UI verification)" if args.codex_install else "package structure passed"))
