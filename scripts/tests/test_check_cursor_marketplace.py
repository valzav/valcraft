#!/usr/bin/env python3
"""Discriminating tests for the Cursor marketplace path-join checker."""

from __future__ import annotations

import json
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

REPOSITORY = Path(__file__).resolve().parents[2]
CHECKER = REPOSITORY / "scripts" / "check-cursor-marketplace.py"
MARKETPLACE = Path(".cursor-plugin") / "marketplace.json"
PLUGIN = Path("plugins") / "valcraft" / ".cursor-plugin" / "plugin.json"


class CursorMarketplaceCheckTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary_directory = tempfile.TemporaryDirectory()
        self.root = Path(self.temporary_directory.name)
        marketplace_path = self.root / MARKETPLACE
        plugin_path = self.root / PLUGIN
        marketplace_path.parent.mkdir(parents=True)
        plugin_path.parent.mkdir(parents=True)
        shutil.copy(REPOSITORY / MARKETPLACE, marketplace_path)
        shutil.copy(REPOSITORY / PLUGIN, plugin_path)

    def tearDown(self) -> None:
        self.temporary_directory.cleanup()

    def run_check(self) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [sys.executable, str(CHECKER), str(self.root)],
            capture_output=True,
            text=True,
        )

    def write_catalog(self, catalog: dict) -> None:
        (self.root / MARKETPLACE).write_text(json.dumps(catalog, indent=2) + "\n")

    def catalog(self) -> dict:
        return json.loads((self.root / MARKETPLACE).read_text())

    def test_shipped_catalog_resolves(self) -> None:
        result = self.run_check()
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn(PLUGIN.as_posix(), result.stdout)

    def test_retargeted_source_fails(self) -> None:
        catalog = self.catalog()
        catalog["plugins"][0]["source"] = "missing"
        self.write_catalog(catalog)
        result = self.run_check()
        self.assertNotEqual(result.returncode, 0, result.stdout)
        self.assertIn("does not exist", result.stderr)

    def test_missing_plugin_root_fails(self) -> None:
        catalog = self.catalog()
        del catalog["metadata"]["pluginRoot"]
        self.write_catalog(catalog)
        result = self.run_check()
        self.assertNotEqual(result.returncode, 0, result.stdout)
        self.assertIn("metadata.pluginRoot is missing", result.stderr)

    def test_missing_owner_name_fails(self) -> None:
        catalog = self.catalog()
        del catalog["owner"]
        self.write_catalog(catalog)
        result = self.run_check()
        self.assertNotEqual(result.returncode, 0, result.stdout)
        self.assertIn("owner.name is missing", result.stderr)

    def test_catalog_name_mismatch_fails(self) -> None:
        catalog = self.catalog()
        catalog["plugins"][0]["name"] = "other-plugin"
        self.write_catalog(catalog)
        result = self.run_check()
        self.assertNotEqual(result.returncode, 0, result.stdout)
        self.assertIn("does not match", result.stderr)


if __name__ == "__main__":
    unittest.main()
