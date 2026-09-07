"""Validate canonical skill sources and the collection catalog (Python 3.10+)."""
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
        raise ValueError("Invalid VERSION")
    catalog = read_json(root / "catalog.json")
    if catalog.get("schema_version") != 1:
        raise ValueError("Unsupported catalog schema")
    entries = catalog["skills"]
    names = [e["id"] for e in entries]
    if not names or len(names) != len(set(names)):
        raise ValueError("Duplicate or empty skill catalog")
    disk = {p.name for p in (root / "skills").iterdir() if p.is_dir()}
    if set(names) != disk:
        raise ValueError("Catalog must list every skill directory exactly once")
    for entry in entries:
        name = entry["id"]
        if not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", name):
            raise ValueError("Invalid skill id")
        if entry["status"] not in {"ready", "review-needed", "deprecated"}:
            raise ValueError("Invalid skill status")
        if entry["category"] not in catalog["categories"]:
            raise ValueError("Unknown category")
        source = entry["source"]
        if not re.fullmatch(r"[a-z0-9-]+", source):
            raise ValueError("Invalid source id")
        provenance = read_json(root / "sources" / (source + ".json"))
        if not re.fullmatch(r"[a-f0-9]{40}", provenance["revision"]):
            raise ValueError("Source revision must be immutable")
        if not provenance["repository"].startswith("https://") or not provenance.get("license"):
            raise ValueError("Missing source URL/license")
        skill = root / "skills" / name
        for p in [skill, *skill.rglob("*")]:
            if p.is_symlink():
                raise ValueError("Skill sources cannot contain symlinks")
            if p.name in {".git", ".env", "__pycache__", "node_modules", ".DS_Store"}:
                raise ValueError(f"Unexpected local file: {p}")
        text = (skill / "SKILL.md").read_text(encoding="utf-8")
        if not text.startswith("---\n") or "\n---" not in text[4:]:
            raise ValueError("Missing skill frontmatter")
        front = text.split("---", 2)[1]
        if not re.search(r"^name: " + re.escape(name) + r"\s*$", front, re.M):
            raise ValueError("Skill name must match directory")
        if not re.search(r"^description: \S.+$", front, re.M):
            raise ValueError("Missing skill description")
        if entry["status"] == "ready" and re.search(r"^disable-model-invocation: true", front, re.M):
            policy = skill / "agents/openai.yaml"
            if not policy.is_file() or policy.read_text().strip() != "policy:\n  allow_implicit_invocation: false":
                raise ValueError("Explicit-only policy needs matching Codex invocation policy")
        if not (skill / "LICENSE").is_file():
            raise ValueError("Each skill must retain its license")
    bundles = catalog["bundles"]
    ids = [b["id"] for b in bundles]
    if not ids or len(ids) != len(set(ids)):
        raise ValueError("Duplicate or empty bundle catalog")
    for bundle in bundles:
        if not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", bundle["id"]):
            raise ValueError("Invalid bundle id")
        members = bundle["skills"]
        if not members or len(members) != len(set(members)) or not set(members) <= set(names):
            raise ValueError("Unknown or duplicate bundle member")
    return version, catalog


def ready_bundles(catalog):
    ready = {e["id"] for e in catalog["skills"] if e["status"] == "ready"}
    return [b for b in catalog["bundles"] if set(b["skills"]) <= ready]


if __name__ == "__main__":
    version, catalog = validate()
    ready = sum(e["status"] == "ready" for e in catalog["skills"])
    print(f"Validated {len(catalog['skills'])} skills; {ready} ready; version {version}")
