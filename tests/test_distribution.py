import hashlib
import json
import shutil
import sys
import tempfile
import unittest
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from package import package
from validate import validate
from install import commands


class DistributionTests(unittest.TestCase):
    def test_archive_round_trip_and_reproducibility(self):
        with tempfile.TemporaryDirectory() as temp:
            temp = Path(temp)
            version, _ = validate(ROOT)
            first = package(output=temp / "a")
            second = package(output=temp / "b")
            self.assertEqual([p.read_bytes() for p in first], [p.read_bytes() for p in second])
            for line in (temp / "a/SHA256SUMS").read_text().splitlines():
                digest, name = line.split("  ")
                self.assertEqual(digest, hashlib.sha256((temp / "a" / name).read_bytes()).hexdigest())
            with zipfile.ZipFile(temp / f"a/skills-{version}.zip") as z:
                self.assertFalse(any(".git/" in n or "decisions.md" in n or "AGENTS.md" in n for n in z.namelist()))
                z.extractall(temp / "extracted")
            extracted = temp / f"extracted/skills-{version}"
            self.assertEqual(validate(extracted), validate(ROOT))
            self.assertIn(str(extracted), commands("codex", "show-me", extracted)[0])
            with zipfile.ZipFile(temp / f"a/show-me-{version}.zip") as z:
                self.assertIn(".claude-plugin/plugin.json", z.namelist())
                self.assertIn(".codex-plugin/plugin.json", z.namelist())
                self.assertIn(b"Copyright (c) 2026 HumanLayer", z.read("skills/show-me/LICENSE"))

    def test_catalog_tampering_is_rejected(self):
        with tempfile.TemporaryDirectory() as temp:
            target = Path(temp) / "repo"
            shutil.copytree(ROOT, target, ignore=shutil.ignore_patterns(".git", "dist", "__pycache__"))
            path = target / ".agents/plugins/marketplace.json"
            data = json.loads(path.read_text())
            data["plugins"][0]["source"]["path"] = "../../outside"
            path.write_text(json.dumps(data))
            with self.assertRaisesRegex(ValueError, "local plugin path"):
                package(target, Path(temp) / "output")

    def test_manifest_version_drift_is_rejected(self):
        with tempfile.TemporaryDirectory() as temp:
            target = Path(temp) / "repo"
            shutil.copytree(ROOT, target, ignore=shutil.ignore_patterns(".git", "dist", "__pycache__"))
            path = target / "plugins/show-me/.claude-plugin/plugin.json"
            data = json.loads(path.read_text())
            data["version"] = "9.9.9"
            path.write_text(json.dumps(data))
            with self.assertRaisesRegex(ValueError, "version mismatch"):
                validate(target)

    def test_installer_uses_native_engine_commands(self):
        self.assertEqual(commands("codex", "show-me")[1], ["codex", "plugin", "add", "show-me@admax-skills"])
        self.assertEqual(commands("claude", "show-me")[1], ["claude", "plugin", "install", "show-me@admax-skills"])
        with self.assertRaisesRegex(ValueError, "Unknown plugin"):
            commands("codex", "../../outside")


if __name__ == "__main__":
    unittest.main()
