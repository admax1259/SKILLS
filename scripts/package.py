"""Build deterministic, allowlisted marketplace and plugin archives."""
import argparse
import hashlib
import zipfile
from pathlib import Path
from validate import ROOT, validate


def write_zip(destination, files):
    with zipfile.ZipFile(destination, "w", compression=zipfile.ZIP_DEFLATED) as archive:
        for name, path in sorted(files.items()):
            if path.is_symlink():
                raise ValueError(f"Refusing symlink: {path}")
            info = zipfile.ZipInfo(name, date_time=(2026, 1, 1, 0, 0, 0))
            info.compress_type = zipfile.ZIP_DEFLATED
            info.create_system = 3
            info.external_attr = 0o100644 << 16
            archive.writestr(info, path.read_bytes())


def package(root=ROOT, output=None):
    root = Path(root).resolve()
    version, names = validate(root)
    output = Path(output) if output else root / "dist"
    output.mkdir(parents=True, exist_ok=True)
    # Only audited distribution content belongs in public install archives.
    allowed = ["VERSION", "LICENSE", "README.md", "README.en.md", "CHANGELOG.md",
               ".agents/plugins/marketplace.json", ".claude-plugin/marketplace.json",
               "scripts/install.py", "scripts/validate.py", "CONTRIBUTING.md",
               "docs/ROADMAP.md", "docs/releases.md", "docs/migration-review.zh-CN.md"]
    files = {name: root / name for name in allowed}
    archives = []
    for name in names:
        plugin = root / "plugins" / name
        members = {}
        for path in plugin.rglob("*"):
            if not path.is_file():
                continue
            rel = path.relative_to(plugin)
            # Disallow accidental local output and executable hooks in this skills-only release.
            if any(part in {".git", "__pycache__", "node_modules"} for part in rel.parts):
                raise ValueError(f"Unexpected plugin content: {rel}")
            if path.suffix not in {".md", ".json", ".yaml", ".html", ".css", ".js"} and path.name != "LICENSE":
                raise ValueError(f"Review new distribution file type: {rel}")
            members[rel.as_posix()] = path
            files["plugins/" + name + "/" + rel.as_posix()] = path
        dest = output / f"{name}-{version}.zip"
        write_zip(dest, members)
        archives.append(dest)
    dest = output / f"skills-{version}.zip"
    write_zip(dest, {f"skills-{version}/{name}": path for name, path in files.items()})
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
