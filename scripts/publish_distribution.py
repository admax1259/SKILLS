"""Publish a validated release payload to the moving distribution branch."""
import argparse
import re
from pathlib import Path
import shutil
import subprocess
import tempfile
from check_package import check


def publish(marketplace, remote, source_commit):
    marketplace = Path(marketplace).resolve()
    version, _ = check(marketplace)
    with tempfile.TemporaryDirectory(prefix='skills-distribution-') as temp:
        root = Path(temp)
        def git(*args):
            return subprocess.check_output(['git', '-C', str(root), *args], text=True).strip()
        git('init', '-q')
        # No background writers may outlive this disposable checkout.
        git('config', 'gc.auto', '0')
        git('config', 'maintenance.auto', 'false')
        git('config', 'user.name', 'github-actions[bot]')
        git('config', 'user.email', '41898282+github-actions[bot]@users.noreply.github.com')
        git('remote', 'add', 'origin', remote)
        existing = git('ls-remote', '--heads', 'origin', 'refs/heads/distribution')
        if existing:
            git('fetch', '-q', 'origin', 'distribution')
            git('checkout', '-q', '-b', 'distribution', 'FETCH_HEAD')
            previous = (root / 'VERSION').read_text().strip()
            def order(value):
                match = re.fullmatch(r'(\d+)\.(\d+)\.(\d+)(?:-beta\.(\d+))?', value)
                if not match:
                    raise ValueError("Invalid channel VERSION")
                major, minor, patch, beta = match.groups()
                return (int(major), int(minor), int(patch), beta is None, int(beta or 0))
            if order(version) < order(previous):
                raise ValueError("Refusing to downgrade the distribution channel")
            # This checkout is disposable and contains generated output only.
            for p in root.iterdir():
                if p.name != '.git':
                    shutil.rmtree(p) if p.is_dir() else p.unlink()
        else:
            git('checkout', '-q', '--orphan', 'distribution')
        shutil.copytree(marketplace, root, dirs_exist_ok=True,
                        ignore=shutil.ignore_patterns('.skills-build'))
        git('add', '--all')
        if existing and not git('diff', '--cached', '--name-only'):
            return git('rev-parse', 'HEAD')
        if existing and version == previous:
            raise ValueError("Same channel version has different content; bump VERSION")
        git('commit', '-q', '-m', f'Release {version} from {source_commit}')
        # Normal fast-forward push: a concurrent update must fail, never be overwritten.
        git('push', '-q', 'origin', 'HEAD:refs/heads/distribution')
        return git('rev-parse', 'HEAD')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('marketplace', type=Path)
    parser.add_argument('--remote', required=True)
    parser.add_argument('--source-commit', required=True)
    args = parser.parse_args()
    print(publish(args.marketplace, args.remote, args.source_commit))
