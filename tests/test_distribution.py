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
from package import build_codex_plugin, build_marketplace, package
from validate import validate
from install import commands
from check_package import check


def clone(destination):
    shutil.copytree(ROOT, destination, ignore=shutil.ignore_patterns(".git", "dist", "__pycache__"))
    return destination


class DistributionTests(unittest.TestCase):
    def test_release_versions_accept_beta_and_reject_unsafe_tags(self):
        with tempfile.TemporaryDirectory() as temp:
            root = clone(Path(temp) / "repo")
            for version in ["1.0.0", "0.6.0-beta.1", "0.6.0-beta.12"]:
                (root / "VERSION").write_text(version)
                self.assertEqual(validate(root)[0], version)
            for version in ["01.0.0", "0.6.0-beta.01", "0.6.0-beta", "../main", "v0.6.0", "0.6.0\nunsafe"]:
                (root / "VERSION").write_text(version)
                with self.subTest(version=version), self.assertRaisesRegex(ValueError, "Invalid VERSION"):
                    validate(root)

    def test_source_root_manifest_contract(self):
        marketplace = json.loads((ROOT / ".agents/plugins/marketplace.json").read_text())
        self.assertEqual(marketplace["name"], "admax-skills")
        self.assertEqual(len(marketplace["plugins"]), 1)
        entry = marketplace["plugins"][0]
        self.assertEqual(entry["name"], "admax-skills")
        self.assertEqual(entry["source"], {"source": "local", "path": "./"})
        manifest = json.loads((ROOT / ".codex-plugin/plugin.json").read_text())
        self.assertEqual(manifest["name"], entry["name"])
        self.assertEqual(manifest["version"], (ROOT / "VERSION").read_text().strip())
        self.assertEqual(manifest["skills"], "./skills/")
        _, catalog = validate(ROOT)
        self.assertTrue(all(entry["status"] == "ready" for entry in catalog["skills"]),
                        "A root plugin exposes every skill; all catalog skills must be reviewed")

    def test_archives_round_trip_reproducibility_and_ready_gate(self):
        with tempfile.TemporaryDirectory() as temp:
            temp = Path(temp)
            version, catalog = validate(ROOT)
            first = package(output=temp / "a")
            second = package(output=temp / "b")
            self.assertEqual([p.name for p in first], [f"skills-{version}.zip", "SHA256SUMS"])
            self.assertEqual([p.read_bytes() for p in first], [p.read_bytes() for p in second])
            digest, name = (temp / "a/SHA256SUMS").read_text().strip().split("  ")
            self.assertEqual(digest, hashlib.sha256((temp / "a" / name).read_bytes()).hexdigest())
            with zipfile.ZipFile(first[0]) as z:
                self.assertFalse(any(".git/" in n or "catalog.json" in n or "AGENTS.md" in n for n in z.namelist()))
                z.extractall(temp / "extracted")
            extracted = temp / f"extracted/skills-{version}"
            self.assertEqual(check(extracted)[0], version)
            self.assertTrue((extracted / "INSTALL.md").is_file())
            self.assertFalse((extracted / ".codex-plugin").exists())
            self.assertFalse(any(p.name == ".skills-build" for p in extracted.rglob("*")))
            expected = {e["id"] for e in catalog["skills"] if e["status"] == "ready"}
            claude = extracted / "claude-plugins/admax-skills"
            for plugin in [extracted / "plugins/admax-skills", claude]:
                self.assertEqual({p.name for p in (plugin / "skills").iterdir()}, expected)
                self.assertIn(b"Copyright (c) 2026 HumanLayer", (plugin / "skills/show-me/LICENSE").read_bytes())
                self.assertTrue((plugin / "skills/pr-review-canvas/scripts/render.py").is_file())
            for engine in ["codex", "claude"]:
                subprocess.run([sys.executable, str(extracted / "scripts/install.py"),
                                "--engine", engine, "--dry-run"], check=True, capture_output=True)
                self.assertIn("admax-skills@admax-skills", commands(engine, extracted)[1])
            self.assertEqual(json.loads((extracted / ".agents/plugins/marketplace.json").read_text())["plugins"][0]["source"]["path"], "./plugins/admax-skills")
            self.assertEqual(json.loads((claude / ".claude-plugin/plugin.json").read_text())["version"], version)

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

    def test_package_audit_rejects_missing_or_escaping_plugin_and_assets(self):
        with tempfile.TemporaryDirectory() as temp:
            built = build_marketplace(ROOT, Path(temp) / "built")
            market_path = built / ".agents/plugins/marketplace.json"
            market = json.loads(market_path.read_text())
            for source in ["./plugins/missing", "../outside", "./../outside"]:
                market["plugins"][0]["source"]["path"] = source
                market_path.write_text(json.dumps(market))
                with self.subTest(source=source), self.assertRaises(ValueError):
                    check(built)
            market["plugins"][0]["source"]["path"] = "./plugins/admax-skills"
            market_path.write_text(json.dumps(market))
            manifest_path = built / "plugins/admax-skills/.codex-plugin/plugin.json"
            manifest = json.loads(manifest_path.read_text())
            manifest["interface"]["logo"] = "./assets/missing.png"
            manifest_path.write_text(json.dumps(manifest))
            with self.assertRaisesRegex(ValueError, "Missing or escaping"):
                check(built)

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
                             (built / "plugins/admax-skills/skills/example/SKILL.md").read_bytes())

    def test_builder_refuses_unowned_output(self):
        with tempfile.TemporaryDirectory() as temp:
            target = Path(temp) / "keep"
            target.mkdir()
            important = target / "user-file"
            important.write_text("keep")
            with self.assertRaisesRegex(ValueError, "not owned"):
                build_marketplace(ROOT, target)
            self.assertEqual(important.read_text(), "keep")

    def test_codex_builder_excludes_unreviewed_skills(self):
        with tempfile.TemporaryDirectory() as temp:
            root = clone(Path(temp) / "repo")
            path = root / "catalog.json"
            catalog = json.loads(path.read_text())
            next(e for e in catalog["skills"] if e["id"] == "show-me")["status"] = "review-needed"
            path.write_text(json.dumps(catalog))
            built = build_codex_plugin(root, Path(temp) / "chatgpt")
            self.assertFalse((built / "skills/show-me").exists())
            self.assertTrue((built / "skills/verify-this").is_dir())

    def test_dry_run_does_not_build_or_install(self):
        with tempfile.TemporaryDirectory() as temp:
            root = clone(Path(temp) / "repo")
            result = subprocess.run([sys.executable, str(root / "scripts/install.py"),
                                     "--engine", "codex", "--dry-run"], capture_output=True, text=True)
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertFalse((root / "dist").exists())
            major, minor, patch = (root / "VERSION").read_text().strip().split("-", 1)[0].split(".")
            (root / "VERSION").write_text(f"{major}.{minor}.{int(patch) + 1}\n")
            upgraded = subprocess.run([sys.executable, str(root / "scripts/install.py"),
                                       "--engine", "codex", "--dry-run"], capture_output=True, text=True)
            self.assertEqual(upgraded.returncode, 0, upgraded.stderr)
            self.assertEqual(result.stdout, upgraded.stdout, "Version upgrades must retain marketplace source identity")
            catalog_path = root / "catalog.json"
            data = json.loads(catalog_path.read_text())
            next(e for e in data["skills"] if e["id"] == "fix-ci")["status"] = "review-needed"
            catalog_path.write_text(json.dumps(data))
            manifest_path = root / ".codex-plugin/plugin.json"
            manifest = json.loads(manifest_path.read_text())
            manifest["version"] = (root / "VERSION").read_text().strip()
            manifest_path.write_text(json.dumps(manifest))
            built = build_marketplace(root, Path(temp) / "pending")
            self.assertFalse((built / "plugins/admax-skills/skills/fix-ci").exists())
            self.assertFalse((built / "claude-plugins/admax-skills/skills/fix-ci").exists())
            self.assertTrue((built / "plugins/admax-skills/skills/show-me").exists())

    def test_explicit_only_policy_requires_codex_mapping(self):
        with tempfile.TemporaryDirectory() as temp:
            root = clone(Path(temp) / "repo")
            (root / "skills/pr-review-canvas/agents/openai.yaml").unlink()
            with self.assertRaisesRegex(ValueError, "matching Codex"):
                validate(root)

    def test_engine_specific_invocation_policy(self):
        with tempfile.TemporaryDirectory() as temp:
            built = build_marketplace(ROOT, Path(temp) / "built")
            codex = built / "plugins/admax-skills"
            claude = built / "claude-plugins/admax-skills"
            for name in [e["id"] for e in json.loads((ROOT / "catalog.json").read_text())["skills"] if e.get("invocation") == "explicit"]:
                relative = Path("skills") / name
                self.assertNotIn("disable-model-invocation:", (codex / relative / "SKILL.md").read_text())
                self.assertIn("allow_implicit_invocation: false", (codex / relative / "agents/openai.yaml").read_text())
                self.assertIn("disable-model-invocation: true", (claude / relative / "SKILL.md").read_text())
            self.assertFalse((codex / ".claude-plugin/plugin.json").exists())
            self.assertFalse((claude / ".codex-plugin").exists())
            self.assertEqual((codex / "skills/pr-review-canvas/renderer.js").read_bytes(),
                             (claude / "skills/pr-review-canvas/renderer.js").read_bytes())
            catalog = json.loads((built / ".claude-plugin/marketplace.json").read_text())
            self.assertEqual(next(p for p in catalog["plugins"] if p["name"] == "admax-skills")["source"],
                             "./claude-plugins/admax-skills")

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
