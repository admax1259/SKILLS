import hashlib
import json
import shutil
import subprocess
import sys
import tempfile
import unittest
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from package import build_chatgpt_plugin, build_marketplace, package
from validate import validate
from install import commands


def clone(destination):
    shutil.copytree(ROOT, destination, ignore=shutil.ignore_patterns(".git", "dist", "__pycache__"))
    return destination


class DistributionTests(unittest.TestCase):
    def test_archives_round_trip_reproducibility_and_ready_gate(self):
        with tempfile.TemporaryDirectory() as temp:
            temp = Path(temp)
            version, catalog = validate(ROOT)
            first = package(output=temp / "a")
            second = package(output=temp / "b")
            self.assertEqual([p.read_bytes() for p in first], [p.read_bytes() for p in second])
            for line in (temp / "a/SHA256SUMS").read_text().splitlines():
                digest, name = line.split("  ")
                self.assertEqual(digest, hashlib.sha256((temp / "a" / name).read_bytes()).hexdigest())
            with zipfile.ZipFile(temp / f"a/skills-{version}.zip") as z:
                self.assertFalse(any(".git/" in n or "catalog.json" in n or "AGENTS.md" in n for n in z.namelist()))
                self.assertTrue(any("check-compiler-errors/SKILL.md" in n for n in z.namelist()))
                self.assertTrue(any("fix-ci/SKILL.md" in n for n in z.namelist()))
                self.assertTrue(any("pr-review-canvas/scripts/render.py" in n for n in z.namelist()))
                z.extractall(temp / "extracted")
            extracted = temp / f"extracted/skills-{version}"
            subprocess.run([sys.executable, str(extracted / "scripts/install.py"),
                            "--engine", "claude", "--dry-run"], check=True, capture_output=True)
            self.assertIn(str(extracted.resolve()), commands("codex", "show-me", extracted)[0])
            self.assertIn("engineering-kit@admax-skills", commands("codex", "engineering-kit", extracted)[1])
            with zipfile.ZipFile(temp / f"a/show-me-{version}.zip") as z:
                self.assertIn(".claude-plugin/plugin.json", z.namelist())
                self.assertIn(".codex-plugin/plugin.json", z.namelist())
                self.assertIn(b"Copyright (c) 2026 HumanLayer", z.read("skills/show-me/LICENSE"))
            with zipfile.ZipFile(temp / f"a/admax-skills-chatgpt-{version}.zip") as z:
                names = z.namelist()
                self.assertIn(".codex-plugin/plugin.json", names)
                self.assertFalse(any(name.startswith(f"chatgpt-plugin-{version}/") for name in names))
                manifest = json.loads(z.read(".codex-plugin/plugin.json"))
                self.assertEqual(manifest["name"], "admax-skills")
                self.assertEqual(manifest["skills"], "./skills/")
                self.assertEqual(
                    {entry["id"] for entry in catalog["skills"] if entry["status"] == "ready"},
                    {Path(name).parts[1] for name in names
                     if len(Path(name).parts) >= 3 and Path(name).parts[0] == "skills"})
                self.assertNotIn(b"disable-model-invocation: true",
                                 z.read("skills/pr-review-canvas/SKILL.md"))

    def test_cursor_import_preserves_all_recorded_files(self):
        source = json.loads((ROOT / "sources/cursor-team-kit.json").read_text())
        for relative, digest in source["imported_files"].items():
            with self.subTest(path=relative):
                adaptation = source.get("adapted_files", {}).get(relative)
                if adaptation:
                    self.assertTrue(adaptation["reason"])
                    self.assertEqual(adaptation["baseline_sha256"], digest)
                    digest = adaptation["sha256"]
                self.assertEqual(digest, hashlib.sha256((ROOT / "skills" / relative).read_bytes()).hexdigest())

    def test_unlisted_skill_is_rejected(self):
        with tempfile.TemporaryDirectory() as temp:
            root = clone(Path(temp) / "repo")
            (root / "skills/unlisted").mkdir()
            with self.assertRaisesRegex(ValueError, "every skill"):
                validate(root)

    def test_invalid_bundle_member_is_rejected(self):
        with tempfile.TemporaryDirectory() as temp:
            root = clone(Path(temp) / "repo")
            path = root / "catalog.json"
            data = json.loads(path.read_text())
            data["bundles"][0]["skills"] = ["../../outside"]
            path.write_text(json.dumps(data))
            with self.assertRaisesRegex(ValueError, "bundle member"):
                package(root, Path(temp) / "output")

    def test_ready_skill_can_be_added_without_duplicate_source(self):
        with tempfile.TemporaryDirectory() as temp:
            root = clone(Path(temp) / "repo")
            skill = root / "skills/example"
            skill.mkdir()
            (skill / "SKILL.md").write_text("---\nname: example\ndescription: Example workflow for distribution testing.\n---\nExample.\n")
            shutil.copyfile(root / "skills/show-me/LICENSE", skill / "LICENSE")
            path = root / "catalog.json"
            data = json.loads(path.read_text())
            data["skills"].append({"id": "example", "category": "visualization", "source": "humanlayer",
                                   "upstream_path": "example", "status": "ready"})
            next(b for b in data["bundles"] if b["id"] == "show-me")["skills"].append("example")
            path.write_text(json.dumps(data))
            built = build_marketplace(root, Path(temp) / "built")
            self.assertEqual((skill / "SKILL.md").read_bytes(),
                             (built / "plugins/show-me/skills/example/SKILL.md").read_bytes())

    def test_builder_refuses_unowned_output(self):
        with tempfile.TemporaryDirectory() as temp:
            target = Path(temp) / "keep"
            target.mkdir()
            important = target / "user-file"
            important.write_text("keep")
            with self.assertRaisesRegex(ValueError, "not owned"):
                build_marketplace(ROOT, target)
            self.assertEqual(important.read_text(), "keep")

    def test_chatgpt_builder_excludes_unreviewed_skills(self):
        with tempfile.TemporaryDirectory() as temp:
            root = clone(Path(temp) / "repo")
            path = root / "catalog.json"
            catalog = json.loads(path.read_text())
            next(e for e in catalog["skills"] if e["id"] == "show-me")["status"] = "review-needed"
            path.write_text(json.dumps(catalog))
            built = build_chatgpt_plugin(root, Path(temp) / "chatgpt")
            self.assertFalse((built / "skills/show-me").exists())
            self.assertTrue((built / "skills/verify-this").is_dir())

    def test_dry_run_does_not_build_or_install(self):
        with tempfile.TemporaryDirectory() as temp:
            root = clone(Path(temp) / "repo")
            result = subprocess.run([sys.executable, str(root / "scripts/install.py"),
                                     "--engine", "codex", "--dry-run"], capture_output=True, text=True)
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertFalse((root / "dist").exists())
            major, minor, patch = (root / "VERSION").read_text().strip().split(".")
            (root / "VERSION").write_text(f"{major}.{minor}.{int(patch) + 1}\n")
            upgraded = subprocess.run([sys.executable, str(root / "scripts/install.py"),
                                       "--engine", "codex", "--dry-run"], capture_output=True, text=True)
            self.assertEqual(upgraded.returncode, 0, upgraded.stderr)
            self.assertEqual(result.stdout, upgraded.stdout, "Version upgrades must retain marketplace source identity")
            catalog_path = root / "catalog.json"
            data = json.loads(catalog_path.read_text())
            next(e for e in data["skills"] if e["id"] == "fix-ci")["status"] = "review-needed"
            catalog_path.write_text(json.dumps(data))
            built = build_marketplace(root, Path(temp) / "pending")
            self.assertFalse((built / "plugins/engineering-kit").exists())
            rejected = subprocess.run([sys.executable, str(root / "scripts/install.py"),
                                       "--engine", "codex", "--bundle", "engineering-kit", "--dry-run"],
                                      capture_output=True, text=True)
            self.assertNotEqual(rejected.returncode, 0)

    def test_explicit_only_policy_requires_codex_mapping(self):
        with tempfile.TemporaryDirectory() as temp:
            root = clone(Path(temp) / "repo")
            (root / "skills/pr-review-canvas/agents/openai.yaml").unlink()
            with self.assertRaisesRegex(ValueError, "matching Codex"):
                validate(root)

    def test_engine_specific_invocation_policy(self):
        with tempfile.TemporaryDirectory() as temp:
            built = build_marketplace(ROOT, Path(temp) / "built")
            codex = built / "plugins/engineering-kit"
            claude = built / "claude-plugins/engineering-kit"
            for name in ["pr-review-canvas", "thermo-nuclear-code-quality-review"]:
                relative = Path("skills") / name
                self.assertNotIn("disable-model-invocation:", (codex / relative / "SKILL.md").read_text())
                self.assertIn("allow_implicit_invocation: false", (codex / relative / "agents/openai.yaml").read_text())
                self.assertIn("disable-model-invocation: true", (claude / relative / "SKILL.md").read_text())
            self.assertFalse((codex / ".claude-plugin").exists())
            self.assertFalse((claude / ".codex-plugin").exists())
            self.assertEqual((codex / "skills/pr-review-canvas/renderer.js").read_bytes(),
                             (claude / "skills/pr-review-canvas/renderer.js").read_bytes())
            catalog = json.loads((built / ".claude-plugin/marketplace.json").read_text())
            self.assertEqual(next(p for p in catalog["plugins"] if p["name"] == "engineering-kit")["source"],
                             "./claude-plugins/engineering-kit")

    def test_package_output_rebuild_excludes_stale_archives(self):
        with tempfile.TemporaryDirectory() as temp:
            target = Path(temp) / "output"
            package(output=target)
            (target / "obsolete.zip").write_bytes(b"old generated artifact")
            package(output=target)
            self.assertFalse((target / "obsolete.zip").exists())
            other = Path(temp) / "user-directory"
            other.mkdir()
            (other / "keep").write_text("user work")
            with self.assertRaisesRegex(ValueError, "not owned"):
                package(output=other)
            self.assertEqual((other / "keep").read_text(), "user work")


if __name__ == "__main__":
    unittest.main()
