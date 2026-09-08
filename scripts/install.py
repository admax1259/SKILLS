"""Build (from source) and install all reviewed skills through native engine CLIs."""
import argparse
import json
import shlex
import shutil
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def commands(engine, marketplace):
    if engine not in {"codex", "claude"}:
        raise ValueError("Unsupported engine")
    marketplace = Path(marketplace).resolve()
    manifest = ".agents/plugins/marketplace.json" if engine == "codex" else ".claude-plugin/marketplace.json"
    catalog = json.loads((marketplace / manifest).read_text())
    bundle = "admax-skills"
    names = {e["name"] for e in catalog["plugins"]}
    if bundle not in names:
        raise ValueError(f"Bundle {bundle!r} is not installable; ready bundles: {', '.join(sorted(names))}")
    return [[engine, "plugin", "marketplace", "add", str(marketplace)],
            [engine, "plugin", "add" if engine == "codex" else "install", f"{bundle}@{catalog['name']}"]]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--engine", choices=["codex", "claude"], required=True)
    parser.add_argument("--dry-run", action="store_true", help="Preview; do not build or install")
    args = parser.parse_args()
    if (ROOT / "catalog.json").is_file():
        from validate import validate
        version, catalog = validate(ROOT)
        if not any(entry["status"] == "ready" for entry in catalog["skills"]):
            parser.error("No reviewed skills are available")
        target = ROOT / "dist" / "marketplace"
        if args.dry_run:
            print(f"Would build all reviewed skills into {target}")
            print(shlex.join([args.engine, "plugin", "marketplace", "add", str(target)]))
            print(shlex.join([args.engine, "plugin", "add" if args.engine == "codex" else "install",
                              "admax-skills@admax-skills"]))
            return
        if not shutil.which(args.engine):
            parser.error(f"Install the {args.engine} CLI first")
        from package import build_marketplace
        marketplace = build_marketplace(ROOT, target)
    else:
        marketplace = ROOT
    steps = commands(args.engine, marketplace)
    for step in steps:
        print(shlex.join(step), flush=True)
    if args.dry_run:
        return
    if not shutil.which(args.engine):
        parser.error(f"Install the {args.engine} CLI first")
    for step in steps:
        subprocess.run(step, check=True)
    print("Installed. Keep the generated marketplace directory. Start a fresh engine session.")


if __name__ == "__main__":
    main()
