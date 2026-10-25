#!/usr/bin/env python3
"""Resolver behavior that the shared conformance cases cannot express portably."""

from __future__ import annotations

import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

NAVIGATION = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(NAVIGATION / "herdr"))
sys.path.insert(0, str(NAVIGATION / "tests"))

from test_conformance import git, prepare_fixture
from valcraft_navigate import checkout
from valcraft_navigate.resolve import Failure, Target, resolve


class ResolverTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.roots = prepare_fixture(cls)

    def test_primary_checkout_from_a_linked_worktree(self) -> None:
        worktree = self.roots["worktree"]
        self.assertEqual(checkout.checkout_root(worktree / "src"), worktree)
        self.assertEqual(
            checkout.primary_checkout(worktree / "src"), self.roots["primary"]
        )
        self.assertEqual(
            checkout.primary_checkout(self.roots["primary"]), self.roots["primary"]
        )

    def test_untracked_config_is_not_a_valcraft_project(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(os.path.realpath(directory))
            git(root, "init", "--quiet")
            (root / ".valcraft").mkdir()
            (root / ".valcraft" / "config.yaml").write_text(
                'valcraft_version: "0.12.2"\n', encoding="utf-8"
            )
            self.assertEqual(resolve(root, "T-001"), Failure("not_valcraft_checkout"))

    def test_file_reference_needs_no_checkout(self) -> None:
        outside = self.roots["outside"]
        (outside / "note.txt").write_text("one\ntwo\n", encoding="utf-8")
        self.assertEqual(
            resolve(outside, "note.txt:2"), Target(str(outside / "note.txt"), 2, 1)
        )

    def test_absolute_path_ignores_the_base(self) -> None:
        page = self.roots["primary"] / "src" / "app" / "page.tsx"
        self.assertEqual(
            resolve(self.roots["outside"], f"{page}:4:2"), Target(str(page), 4, 2)
        )

    def test_home_relative_path(self) -> None:
        with mock.patch.object(Path, "home", return_value=self.roots["primary"]):
            result = resolve(self.roots["outside"], "~/src/app/page.tsx:3")
        self.assertEqual(
            result,
            Target(str(self.roots["primary"] / "src" / "app" / "page.tsx"), 3, 1),
        )

    def test_symbolic_link_resolves_to_its_target(self) -> None:
        link = self.roots["outside"] / "page-link.tsx"
        page = self.roots["primary"] / "src" / "app" / "page.tsx"
        link.symlink_to(page)
        self.assertEqual(
            resolve(self.roots["outside"], "page-link.tsx"), Target(str(page), 1, 1)
        )

    def test_command_prints_json(self) -> None:
        def run(reference: str) -> dict:
            completed = subprocess.run(
                [
                    sys.executable,
                    "-m",
                    "valcraft_navigate",
                    "resolve",
                    "--base",
                    str(self.roots["primary"]),
                    reference,
                ],
                cwd=NAVIGATION / "herdr",
                capture_output=True,
                text=True,
                check=True,
            )
            return json.loads(completed.stdout)

        self.assertEqual(
            run("FEAT-001/T-002"),
            {
                "result": "target",
                "path": str(self.roots["primary"] / "specs/001-alpha/tasks.md"),
                "line": 15,
                "column": 1,
            },
        )
        self.assertEqual(
            run("T-01"), {"result": "failure", "failure": "malformed_identity"}
        )
        ambiguous = run("QT-001")
        self.assertEqual(ambiguous["result"], "ambiguous")
        self.assertEqual(
            [candidate["identity"] for candidate in ambiguous["candidates"]],
            ["Q-001/QT-001", "Q-002/QT-001"],
        )


if __name__ == "__main__":
    unittest.main()
