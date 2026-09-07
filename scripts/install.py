"""Install plugins from this local marketplace through the selected engine CLI."""
import argparse
import shlex
import shutil
import subprocess
from validate import ROOT, read_json, validate


def commands(engine, plugin, root=ROOT):
    _, names = validate(root)
    if plugin not in names:
        raise ValueError(f"Unknown plugin {plugin}; available: {', '.join(names)}")
    market = read_json(root / ".agents/plugins/marketplace.json")["name"]
    return [[engine, "plugin", "marketplace", "add", str(root)],
            [engine, "plugin", "add" if engine == "codex" else "install", f"{plugin}@{market}"]]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--engine", choices=["codex", "claude"], required=True)
    parser.add_argument("--plugin", default="show-me")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    steps = commands(args.engine, args.plugin)
    for step in steps:
        print(shlex.join(step), flush=True)
    if args.dry_run:
        return
    if not shutil.which(args.engine):
        parser.error(f"Install the {args.engine} CLI first, or use --dry-run for commands.")
    for step in steps:
        subprocess.run(step, check=True)
    print("Installed. Start a fresh engine session to verify discovery. Keep this marketplace directory.")


if __name__ == "__main__":
    main()
