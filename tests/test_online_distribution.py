import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
from package import build_marketplace
from publish_distribution import publish
from install import github_commands

class OnlineDistributionTests(unittest.TestCase):
    def test_publish_retry_upgrade_and_downgrade(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            remote = root / 'remote.git'
            subprocess.run(['git', 'init', '--bare', '-q', str(remote)], check=True)
            built = build_marketplace(ROOT, root / 'built')
            first = publish(built, str(remote), 'a' * 40)
            self.assertEqual(first, publish(built, str(remote), 'a' * 40))
            (built / 'README.md').write_text('changed without version bump')
            with self.assertRaisesRegex(ValueError, 'Same channel version'):
                publish(built, str(remote), 'b' * 40)
            def set_version(version):
                (built / 'VERSION').write_text(version + '\n')
                for relative in ['plugins/admax-skills/.codex-plugin/plugin.json',
                                 'claude-plugins/admax-skills/.claude-plugin/plugin.json']:
                    path = built / relative
                    data = json.loads(path.read_text()); data['version'] = version
                    path.write_text(json.dumps(data))
                path = built / '.claude-plugin/marketplace.json'
                data = json.loads(path.read_text()); data['plugins'][0]['version'] = version
                path.write_text(json.dumps(data))
            set_version('99.0.0-beta.1')
            second = publish(built, str(remote), 'b' * 40)
            self.assertNotEqual(first, second)
            parent = subprocess.check_output(['git', '--git-dir', str(remote), 'rev-parse', second + '^'], text=True).strip()
            self.assertEqual(parent, first)
            set_version('0.1.0')
            with self.assertRaisesRegex(ValueError, 'downgrade'):
                publish(built, str(remote), 'c' * 40)

    def test_online_installer_dry_run_does_not_build_or_mutate(self):
        for engine in ['codex', 'claude']:
            for update in [False, True]:
                args = ['python3', str(ROOT / 'scripts/install.py'), '--engine', engine, '--source', 'github', '--dry-run']
                if update: args += ['--update']
                result = subprocess.run(args, capture_output=True, text=True, check=True)
                self.assertIn('admax-skills@admax-skills', result.stdout)
                self.assertNotIn('Would build', result.stdout)
                steps = github_commands(engine, update)
                self.assertEqual(len(steps), 2)
                if not update: self.assertIn('distribution', ' '.join(steps[0]))
