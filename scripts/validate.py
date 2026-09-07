"""Validate this collection's portable packaging contract (Python 3.10+)."""
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def read_json(path):
    return json.loads(path.read_text(encoding="utf-8"))


def validate(root=ROOT):
    root = Path(root).resolve()
    version = (root / "VERSION").read_text().strip()
    if not re.fullmatch(r"(?:0|[1-9]\d*)\.(?:0|[1-9]\d*)\.(?:0|[1-9]\d*)", version):
        raise ValueError("VERSION must be a stable semantic version")
    codex = read_json(root / ".agents/plugins/marketplace.json")
    claude = read_json(root / ".claude-plugin/marketplace.json")
    if codex["name"] != claude["name"] or not re.fullmatch(r"[a-z0-9-]+", codex["name"]):
        raise ValueError("Marketplace names must match")
    catalogs = []
    for catalog in (codex, claude):
        names = [item["name"] for item in catalog["plugins"]]
        if not names or len(names) != len(set(names)):
            raise ValueError("Empty catalog or duplicate plugin name")
        catalogs.append(set(names))
    directories = {p.name for p in (root / "plugins").iterdir() if p.is_dir()}
    if catalogs[0] != catalogs[1] or catalogs[0] != directories:
        raise ValueError("Both catalogs must include every plugin exactly once")
    for entry in codex["plugins"]:
        name = entry["name"]
        if not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", name):
            raise ValueError("Invalid plugin name")
        relative = "./plugins/" + name
        if entry["source"] != {"source": "local", "path": relative}:
            raise ValueError("Codex source must be a local plugin path")
        if entry["policy"] != {"installation": "AVAILABLE", "authentication": "ON_INSTALL"}:
            raise ValueError("Unexpected installation policy")
        other = next(e for e in claude["plugins"] if e["name"] == name)
        if other["source"] != relative or other["version"] != version:
            raise ValueError("Claude catalog source/version mismatch")
        plugin = root / "plugins" / name
        for p in [plugin, *plugin.rglob("*")]:
            if p.is_symlink():
                raise ValueError(f"Plugin packages cannot contain symlinks: {p}")
        for engine in ("codex", "claude"):
            manifest = read_json(plugin / f".{engine}-plugin/plugin.json")
            if manifest["name"] != name or manifest["version"] != version:
                raise ValueError("Manifest name/version mismatch")
            for key in ("description", "license", "repository"):
                if not isinstance(manifest.get(key), str) or not manifest[key].strip():
                    raise ValueError(f"Missing manifest {key}")
            if not manifest.get("author", {}).get("name"):
                raise ValueError("Missing author")
        if not (plugin / "UPSTREAM.md").is_file():
            raise ValueError("Missing provenance")
        skills = list((plugin / "skills").glob("*/SKILL.md"))
        if not skills:
            raise ValueError("No skills")
        for skill in skills:
            text = skill.read_text(encoding="utf-8")
            # Collection policy uses simple, single-line name and description fields.
            if not text.startswith("---\n") or "\n---\n" not in text[4:]:
                raise ValueError("Missing skill frontmatter")
            front = text.split("---", 2)[1]
            if not re.search(r"^name: " + re.escape(skill.parent.name) + r"$", front, re.M):
                raise ValueError("Skill name must match its directory")
            if not re.search(r"^description: \S.+$", front, re.M):
                raise ValueError("Missing skill description")
            if not (skill.parent / "LICENSE").is_file():
                raise ValueError("Each installable skill must retain its license")
    return version, sorted(directories)


if __name__ == "__main__":
    version, names = validate()
    print(f"Validated collection {version}: {', '.join(names)}")
