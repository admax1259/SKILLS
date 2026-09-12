#!/usr/bin/env python3
"""Install this supplemental skill and command without touching managed Orca skills."""
import argparse
import hashlib
from pathlib import Path
import shutil
import sys

NAME = "orca-antigravity-launch"


def install(source, home):
    source, home = Path(source), Path(home)
    files = sorted(p for p in source.rglob("*") if p.is_file() and "__pycache__" not in p.parts)
    digest = hashlib.sha256()
    for path in files:
        if path.is_symlink():
            raise ValueError("Refusing symlink in installation source")
        digest.update(str(path.relative_to(source)).encode() + b"\0" + path.read_bytes())
    versions = home / ".local/share" / NAME
    target = versions / digest.hexdigest()[:16]
    links = {home / ".agents/skills" / NAME: target,
             home / ".local/bin" / NAME: target / "scripts/orca_antigravity_launch.py"}
    # Check all conflicts before changing any discoverable path.
    for link in links:
        if link.is_symlink():
            if not link.resolve().is_relative_to(versions.resolve()):
                raise ValueError("Refusing to replace an unrelated link: " + str(link))
        elif link.exists():
            raise ValueError("Refusing to overwrite an existing user path: " + str(link))
    if target.exists():
        actual = {str(p.relative_to(target)): p.read_bytes() for p in target.rglob("*") if p.is_file()}
        expected = {str(p.relative_to(source)): p.read_bytes() for p in files}
        if actual != expected:
            raise ValueError("Installed snapshot changed; preserving it")
    else:
        target.mkdir(parents=True, mode=0o700)
        for path in files:
            dest = target / path.relative_to(source)
            dest.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(path, dest)
    (target / "scripts/orca_antigravity_launch.py").chmod(0o755)
    for link, destination in links.items():
        link.parent.mkdir(parents=True, exist_ok=True)
        if link.is_symlink() and link.resolve() == destination.resolve():
            continue
        temporary = link.with_name(link.name + ".installing")
        if temporary.exists() or temporary.is_symlink():
            raise ValueError("Previous installation is incomplete: " + str(temporary))
        temporary.symlink_to(destination)
        temporary.replace(link)
    return links


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--home", type=Path, default=Path.home(), help="User home, or isolated test home")
    args = parser.parse_args()
    try:
        for link, target in install(Path(__file__).resolve().parents[1], args.home).items():
            print(f"{link} -> {target}")
    except (ValueError, OSError) as error:
        sys.exit(str(error))
