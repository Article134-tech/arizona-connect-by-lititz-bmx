#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
import tempfile
import unittest
from pathlib import Path

from ux_baseline_guard import verify_baseline


class UxBaselineGuardTests(unittest.TestCase):
    def test_accepts_matching_asset_and_rejects_changed_asset(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            (root / 'styles.css').write_text('body{margin:0}\n', encoding='utf-8')
            digest = hashlib.sha256((root / 'styles.css').read_bytes()).hexdigest()
            manifest = root / 'manifest.json'
            manifest.write_text(json.dumps({'baseline':'v0.55.8','files':{'styles.css':digest}}), encoding='utf-8')
            self.assertEqual([], verify_baseline(root, manifest))
            (root / 'styles.css').write_text('body{margin:1px}\n', encoding='utf-8')
            issues = verify_baseline(root, manifest)
            self.assertEqual(1, len(issues))
            self.assertIn('styles.css', issues[0])

    def test_reports_missing_frozen_asset(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            manifest = root / 'manifest.json'
            manifest.write_text(json.dumps({'baseline':'v0.55.8','files':{'atlas/site.css':'0'*64}}), encoding='utf-8')
            issues = verify_baseline(root, manifest)
            self.assertEqual(['atlas/site.css: missing frozen UX asset'], issues)

    def test_timeline_data_mode_ignores_data_but_detects_logic_change(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            js = root / 'atlas' / 'timeline' / 'timeline.js'
            js.parent.mkdir(parents=True)
            js.write_text("const TIMELINE_DATA=[{\"id\":1}];\nconst LOGIC=1;\n", encoding='utf-8')
            from ux_baseline_guard import baseline_digest
            digest = baseline_digest(js, 'timeline_logic')
            manifest = root / 'manifest.json'
            manifest.write_text(json.dumps({'baseline':'v0.55.8','files':{'atlas/timeline/timeline.js':{'sha256':digest,'mode':'timeline_logic'}}}), encoding='utf-8')
            js.write_text("const TIMELINE_DATA=[{\"id\":2}];\nconst LOGIC=1;\n", encoding='utf-8')
            self.assertEqual([], verify_baseline(root, manifest))
            js.write_text("const TIMELINE_DATA=[{\"id\":2}];\nconst LOGIC=2;\n", encoding='utf-8')
            self.assertEqual(1, len(verify_baseline(root, manifest)))


if __name__ == '__main__':
    unittest.main(verbosity=2)
