"""Catch standalone distribution failures from upstream-relative references."""
import json
from pathlib import Path
import re
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
from package import build_marketplace

class HallmarkImportTests(unittest.TestCase):
    def test_references_resolve_in_both_engine_payloads(self):
        with tempfile.TemporaryDirectory() as temp:
            built = build_marketplace(ROOT, Path(temp) / 'marketplace')
            for engine in ['plugins', 'claude-plugins']:
                skill = built / engine / 'admax-skills/skills/hallmark'
                for doc in skill.rglob('*.md'):
                    for target in re.findall(r'\]\(([^)]+)\)', doc.read_text()):
                        path = target.split('#')[0]
                        if not path or '://' in path or '<' in path:
                            continue
                        resolved = (doc.parent / path).resolve()
                        with self.subTest(engine=engine, doc=str(doc.relative_to(skill)), target=target):
                            self.assertTrue(resolved.is_relative_to(skill.resolve()))
                            self.assertTrue(resolved.exists())
                self.assertEqual((skill / 'assets/catalog-tokens.css').read_bytes(),
                                 (ROOT / 'skills/hallmark/assets/catalog-tokens.css').read_bytes())
                self.assertIn('Copyright (c) 2026 Hallmark contributors', (skill / 'LICENSE').read_text())
