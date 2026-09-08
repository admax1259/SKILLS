"""Exercise the actual standalone runtime, including preservation of user files."""
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
from package import build_marketplace

class UIUXImportTests(unittest.TestCase):
    def test_search_and_persistence_in_both_engine_payloads(self):
        with tempfile.TemporaryDirectory() as temp:
            base = Path(temp).resolve()
            built = build_marketplace(ROOT, base / 'marketplace')
            for engine in ['plugins', 'claude-plugins']:
                with self.subTest(engine=engine):
                    skill = built / engine / 'admax-skills/skills/ui-ux-pro-max'
                    work = base / engine
                    work.mkdir()
                    before = {p.relative_to(skill): p.read_bytes() for p in skill.rglob('*') if p.is_file()}
                    def search(*args):
                        return json.loads(subprocess.check_output([
                            sys.executable, '-B', str(skill / 'scripts/search.py'),
                            *args, '--json'], cwd=work, text=True))
                    self.assertGreater(search('keyboard focus modal', '--domain', 'ux')['count'], 0)
                    self.assertGreater(search('suspense streaming bundle', '--stack', 'nextjs')['count'], 0)
                    args = ['SaaS analytics dashboard', '--design-system', '-p', 'Trial Dashboard']
                    result = search(*args)
                    self.assertTrue(result['design_system'])
                    self.assertIsNone(result['persistence'])
                    self.assertEqual(list(work.iterdir()), [])
                    persist = [*args, '--persist', '--output-dir', str(work)]
                    self.assertEqual(search(*persist)['persistence']['status'], 'success')
                    master = next(work.rglob('MASTER.md'))
                    master.write_text('User-owned design decisions\n')
                    self.assertEqual(search(*persist)['persistence']['status'], 'skipped_exists')
                    self.assertEqual(master.read_text(), 'User-owned design decisions\n')
                    after = {p.relative_to(skill): p.read_bytes() for p in skill.rglob('*') if p.is_file()}
                    self.assertEqual(before, after, 'Runtime must not modify installed plugin files')
