"""Detect dropped resources, attribution, or unrecorded upstream adaptations."""
import hashlib
import json
from pathlib import Path
import subprocess
import unittest

ROOT = Path(__file__).resolve().parents[1]

class ImportedSkillsTests(unittest.TestCase):
    def test_imported_files_and_adaptations(self):
        for source in (ROOT / 'sources').glob('*.json'):
            data = json.loads(source.read_text())
            for relative, baseline in data.get('imported_files', {}).items():
                with self.subTest(source=source.name, file=relative):
                    adjustment = data.get('adapted_files', {}).get(relative)
                    if adjustment:
                        self.assertEqual(adjustment['baseline_sha256'], baseline)
                    expected = adjustment['sha256'] if adjustment else baseline
                    self.assertEqual(hashlib.sha256((ROOT / 'skills' / relative).read_bytes()).hexdigest(), expected)

    def test_requested_groups_and_attribution(self):
        entries = [e for e in json.loads((ROOT / 'catalog.json').read_text())['skills'] if e['source'] == 'matt-pocock']
        self.assertEqual(len(entries), 25)
        self.assertEqual(sum(e['category'] == 'engineering' for e in entries), 18)
        self.assertEqual(sum(e['category'] == 'productivity' for e in entries), 7)
        for entry in entries:
            self.assertIn('Copyright (c) 2026 Matt Pocock', (ROOT / 'skills' / entry['id'] / 'LICENSE').read_text())

    def test_shell_templates_parse_without_execution(self):
        for relative in ['wizard/template.sh', 'diagnosing-bugs/scripts/hitl-loop.template.sh']:
            subprocess.run(['bash', '-n', str(ROOT / 'skills' / relative)], check=True)
