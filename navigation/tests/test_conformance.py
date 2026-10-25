#!/usr/bin/env python3
"""Runs the shared conformance cases in navigation/fixtures/cases.json."""

from __future__ import annotations

import json
import os
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

NAVIGATION = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(NAVIGATION / "herdr"))

from valcraft_navigate.resolve import Ambiguous, Failure, Target, resolve

CASES = json.loads((NAVIGATION / "fixtures" / "cases.json").read_text(encoding="utf-8"))
GIT_ENV = {
    **{key: value for key, value in os.environ.items() if not key.startswith("GIT_")},
    "GIT_AUTHOR_NAME": "Fixture",
    "GIT_AUTHOR_EMAIL": "fixture@example.invalid",
    "GIT_COMMITTER_NAME": "Fixture",
    "GIT_COMMITTER_EMAIL": "fixture@example.invalid",
    "GIT_CONFIG_GLOBAL": os.devnull,
    "GIT_CONFIG_NOSYSTEM": "1",
}


def git(cwd: Path, *args: str) -> None:
    subprocess.run(
        ["git", *args], cwd=cwd, env=GIT_ENV, check=True, capture_output=True
    )


def prepare_fixture(stack: "type[unittest.TestCase]") -> dict:
    """Builds the primary checkout, its linked worktree, and an outside directory."""
    roots = {}
    for name in ("primary", "worktree", "outside"):
        directory = tempfile.TemporaryDirectory()
        stack.addClassCleanup(directory.cleanup)
        roots[name] = Path(os.path.realpath(directory.name))
    primary = roots["primary"] / "checkout"
    shutil.copytree(NAVIGATION / "fixtures" / "checkout", primary)
    git(primary, "init", "--quiet", "--initial-branch=main")
    git(primary, "add", "--all")
    git(primary, "commit", "--quiet", "--message", "fixture")
    worktree = roots["worktree"] / "checkout"
    git(primary, "worktree", "add", "--quiet", "-b", "fixture-worktree", str(worktree))
    for relative, content in CASES["worktree_edits"].items():
        (worktree / relative).write_text(content, encoding="utf-8")
    return {"primary": primary, "worktree": worktree, "outside": roots["outside"]}


class ConformanceTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.roots = prepare_fixture(cls)

    def test_cases(self) -> None:
        for case in CASES["cases"]:
            with self.subTest(case["name"]):
                root = (
                    self.roots["worktree"]
                    if case.get("worktree")
                    else self.roots["primary"]
                )
                base = (
                    self.roots["outside"]
                    if case["base"] == "@outside"
                    else root / case["base"]
                )
                result = resolve(base, case["reference"])
                self.assertEqual(self.describe(result, root), self.expected(case))

    @staticmethod
    def describe(result, root: Path) -> dict:
        def relative(path: str) -> str:
            return Path(path).relative_to(root).as_posix()

        if isinstance(result, Target):
            return {
                "target": {
                    "path": relative(result.path),
                    "line": result.line,
                    "column": result.column,
                }
            }
        if isinstance(result, Ambiguous):
            return {
                "ambiguous": [
                    {
                        "path": relative(candidate.path),
                        "line": candidate.line,
                        "column": candidate.column,
                        "identity": candidate.identity,
                        "title": candidate.title,
                        "text": candidate.text,
                    }
                    for candidate in result.candidates
                ]
            }
        assert isinstance(result, Failure)
        return {"failure": result.failure}

    @staticmethod
    def expected(case: dict) -> dict:
        return {
            key: case[key] for key in ("target", "ambiguous", "failure") if key in case
        }


if __name__ == "__main__":
    unittest.main()
