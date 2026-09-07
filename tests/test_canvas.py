import importlib.util
import json
import subprocess
import sys
import unittest
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
CANVAS = ROOT / "skills/pr-review-canvas"
sys.dont_write_bytecode = True


def module(name):
    spec = importlib.util.spec_from_file_location(name, CANVAS / "scripts" / (name + ".py"))
    result = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(result)
    return result


collector, renderer = module("collect"), module("render")


class CanvasTests(unittest.TestCase):
    def test_github_pagination_and_missing_patch(self):
        calls = []
        meta = {"head": {"sha": "abc"}, "title": "Title", "html_url": "https://github.com/o/r/pull/1", "changed_files": 101}

        def get(endpoint):
            calls.append(endpoint)
            if endpoint.endswith("&page=1"):
                return [{"filename": str(i), "status": "modified", "patch": "@@ -1 +1 @@\n-a\n+b"} for i in range(100)]
            if endpoint.endswith("&page=2"):
                return [{"filename": "binary", "status": "added"}]
            return meta

        result = collector.collect("github", "github.com", "o/r", 1, get)
        self.assertEqual(len(result["files"]), 101)
        self.assertIsNone(result["files"][-1]["patch"])
        self.assertEqual(calls[-1], "repos/o/r/pulls/1")

    def test_gitlab_nested_project_and_oversized_diff(self):
        calls = []

        def get(endpoint):
            calls.append(endpoint)
            if "/diffs?" in endpoint:
                return [{"new_path": "new.py", "old_path": "old.py", "renamed_file": True,
                         "collapsed": True, "diff": ""}]
            return {"sha": "abc", "title": "Title", "web_url": "https://git.example/g/s/r/-/merge_requests/8",
                    "changes_count": "2"}

        result = collector.collect("gitlab", "git.example", "g/s/r", 8, get)
        self.assertTrue(all(p.startswith("projects/g%2Fs%2Fr/merge_requests/8") for p in calls))
        self.assertTrue(result["files"][0]["incomplete"])
        self.assertEqual(result["files"][0]["status"], "renamed")
        self.assertTrue(any("count differs" in note for note in result["limitations"]))

    def test_moving_head_is_rejected(self):
        heads = iter(["old", "new"])

        def get(endpoint):
            if "/files?" in endpoint:
                return []
            return {"head": {"sha": next(heads)}, "title": "", "html_url": "", "changed_files": 0}

        with self.assertRaisesRegex(ValueError, "Head changed"):
            collector.collect("github", "github.com", "o/r", 1, get)

    def test_cli_keeps_explicit_host_and_uses_no_shell(self):
        with patch.object(collector.subprocess, "run") as run:
            run.return_value.stdout = "{}"
            collector.cli_get("gitlab", "git.example", "projects/a%2Fb/merge_requests/1")
            self.assertEqual(run.call_args.args[0],
                             ["glab", "api", "--hostname", "git.example", "projects/a%2Fb/merge_requests/1"])
            self.assertNotIn("shell", run.call_args.kwargs)

    def test_html_escapes_content_and_template_markers(self):
        attack = '</script><script>alert("x")</script><!-- INJECT_BODY -->'
        snapshot = {"title": attack, "head_sha": "abc", "summary": "/* INJECT_JS */",
                    "files": [{"path": attack, "patch": "+ " + attack}, {"path": "missing", "patch": None}]}
        page = renderer.render(snapshot)
        self.assertNotIn(attack, page)
        self.assertIn("&lt;/script&gt;", page)
        self.assertIn("\\u003c/script\\u003e", page)
        self.assertIn("/* INJECT_JS */", page)
        self.assertIn("Patch unavailable or incomplete", page)
        self.assertNotIn("fonts.googleapis.com", page)
        self.assertEqual(page.count('data-diff="'), 2)

    def test_original_lines_survive_rendering(self):
        # Node is an explicit CI test dependency; missing it must fail, not silently skip.
        script = r"""
const assert = require('node:assert/strict');
const {parseDiff, renderDiff} = require(process.argv[1]);
const input = '@@ -4,3 +4,3 @@\n-import a\n+import b\n-x = 1\n+x=1\n context\n\\ No newline at end of file\n@@ -20 +21 @@\n--- tricky\n+++ tricky\n';
const rows = parseDiff(input);
assert.deepEqual(rows.filter(r => r.type === 'del').map(r => [r.code, r.oldLine]),
  [['import a', 4], ['x = 1', 5], ['-- tricky', 20]]);
assert.deepEqual(rows.filter(r => r.type === 'add').map(r => [r.code, r.newLine]),
  [['import b', 4], ['x=1', 5], ['++ tricky', 21]]);
assert.equal(rows.find(r => r.type === 'ctx').newLine, 6);
const el = {};
renderDiff(el, '@@ -1 +1 @@\n-a\n+<script>alert(1)</script>');
assert.ok(el.innerHTML.includes('&lt;script&gt;'));
assert.ok(!el.innerHTML.includes('<script>'));
"""
        subprocess.run(["node", "-e", script, str(CANVAS / "renderer.js")], check=True, capture_output=True)
