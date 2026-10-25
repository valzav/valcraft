#!/usr/bin/env python3
"""Herdr plugin behavior, driven through its real entry points with a fake herdr and a fake editor."""

from __future__ import annotations

import json
import os
import re
import socket
import subprocess
import sys
import tempfile
import time
import unittest
from pathlib import Path
from typing import Optional

NAVIGATION = Path(__file__).resolve().parents[1]
PLUGIN = NAVIGATION / "herdr"
sys.path.insert(0, str(PLUGIN))
sys.path.insert(0, str(NAVIGATION / "tests"))

from test_conformance import git, prepare_fixture
from valcraft_navigate import actions, config, links, picker
from valcraft_navigate.scan import scan

FAKE_HERDR = """#!{python}
import json, os, sys
with open(os.environ["FAKE_HERDR_LOG"], "a") as log:
    log.write(json.dumps(sys.argv[1:]) + "\\n")
if sys.argv[1:3] == ["pane", "read"]:
    sys.stdout.write(open(os.environ["FAKE_PANE_TEXT"]).read())
"""
FAKE_EDITOR = """#!{python}
import json, os, sys
with open(os.environ["FAKE_EDITOR_LOG"], "a") as log:
    log.write(json.dumps(sys.argv) + "\\n")
"""


def write_executable(path: Path, content: str) -> Path:
    path.write_text(content.format(python=sys.executable), encoding="utf-8")
    path.chmod(0o755)
    return path


class PluginTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.roots = prepare_fixture(cls)
        work = tempfile.TemporaryDirectory()
        cls.addClassCleanup(work.cleanup)
        cls.work = Path(os.path.realpath(work.name))
        cls.herdr = write_executable(cls.work / "herdr", FAKE_HERDR)
        cls.editor = write_executable(cls.work / "editor", FAKE_EDITOR)

    def setUp(self) -> None:
        self.case = Path(tempfile.mkdtemp(dir=self.work))
        self.state = self.case / "state"
        self.overlay = self.roots["primary"] / ".valcraft" / "config.local.yaml"
        self.write_overlay("zed", str(self.editor))

    def tearDown(self) -> None:
        self.overlay.unlink(missing_ok=True)

    def write_overlay(self, adapter: str, executable: str) -> None:
        self.overlay.write_text(
            "foreman:\n  approval_mode: attended\n"
            f"editor:\n  adapter: {adapter}\n  executable: {executable}\n",
            encoding="utf-8",
        )

    def run_entry(
        self,
        command: str,
        cwd: Path,
        selected: Optional[str] = None, url: Optional[str] = None,
        pane_text: str = "",
    ) -> None:
        context = {"focused_pane_id": "w1:p1", "focused_pane_cwd": str(cwd)}
        if selected is not None:
            context["selected_text"] = selected
        (self.case / "pane.txt").write_text(pane_text, encoding="utf-8")
        environ = {
            "PATH": os.environ["PATH"],
            "HOME": os.environ.get("HOME", "/"),
            "HERDR_BIN_PATH": str(self.herdr),
            "HERDR_PLUGIN_CONTEXT_JSON": json.dumps(context),
            "HERDR_PLUGIN_STATE_DIR": str(self.state),
            "FAKE_HERDR_LOG": str(self.case / "herdr.log"),
            "FAKE_EDITOR_LOG": str(self.case / "editor.log"),
            "FAKE_PANE_TEXT": str(self.case / "pane.txt"),
        }
        if url is not None:
            environ["HERDR_PLUGIN_CLICKED_URL"] = url
        subprocess.run(
            [sys.executable, "-B", "-m", "valcraft_navigate", command],
            cwd=PLUGIN,
            env=environ,
            check=True,
            capture_output=True,
        )

    def herdr_calls(self) -> list:
        log = self.case / "herdr.log"
        return (
            [json.loads(line) for line in log.read_text().splitlines()]
            if log.exists()
            else []
        )

    def messages(self) -> list:
        """Messages the plugin showed in its own popup."""
        prefix = "VALCRAFT_NAVIGATION_MESSAGE="
        return [
            call[call.index("--env") + 1][len(prefix) :]
            for call in self.herdr_calls()
            if call[:3] == ["plugin", "pane", "open"] and "--env" in call and call[call.index("--env") + 1].startswith(prefix)
        ]

    def editor_calls(self, expected: int = 1) -> list:
        """The editor runs detached, so wait for it to record its arguments."""
        log = self.case / "editor.log"
        deadline = time.monotonic() + 10
        while time.monotonic() < deadline:
            calls = (
                [json.loads(line) for line in log.read_text().splitlines()]
                if log.exists()
                else []
            )
            if len(calls) >= expected:
                return calls
            time.sleep(0.05)
        return []

    def assert_no_editor(self) -> None:
        time.sleep(0.3)
        self.assertFalse((self.case / "editor.log").exists())

    def test_open_selection_opens_zed_at_the_definition(self) -> None:
        self.run_entry(
            "open-selection", self.roots["primary"], selected="FEAT-001/T-001"
        )
        tasks = self.roots["primary"] / "specs/001-alpha/tasks.md"
        self.assertEqual(self.editor_calls(), [[str(self.editor), f"{tasks}:14:1"]])
        self.assertEqual(self.messages(), [])

    def test_vscode_adapter_changes_only_the_argument_vector(self) -> None:
        self.write_overlay("vscode", str(self.editor))
        self.run_entry(
            "open-selection", self.roots["primary"], selected="FEAT-001/T-001"
        )
        tasks = self.roots["primary"] / "specs/001-alpha/tasks.md"
        self.assertEqual(
            self.editor_calls(), [[str(self.editor), "--goto", f"{tasks}:14:1"]]
        )

    def test_file_reference_resolves_against_the_pane_directory(self) -> None:
        self.run_entry(
            "open-selection", self.roots["primary"] / "src", selected="app/page.tsx:3:2"
        )
        page = self.roots["primary"] / "src/app/page.tsx"
        self.assertEqual(self.editor_calls(), [[str(self.editor), f"{page}:3:2"]])

    def test_ambiguous_selection_opens_the_picker_with_every_candidate(self) -> None:
        self.run_entry("open-selection", self.roots["primary"], selected="T-001")
        opens = [
            call
            for call in self.herdr_calls()
            if call[:3] == ["plugin", "pane", "open"]
        ]
        self.assertEqual(len(opens), 1)
        environment = opens[0][opens[0].index("--env") + 1]
        name = environment.split("=", 1)[1]
        self.assertTrue(name.startswith("candidates-"))
        candidates = json.loads((self.state / name).read_text())
        self.assertEqual(
            [candidate["identity"] for candidate in candidates],
            ["FEAT-001/T-001", "FEAT-002/T-001", "FEAT-003/T-001"],
        )
        self.assert_no_editor()

    def test_missing_selection_names_the_pane_picker(self) -> None:
        self.run_entry("open-selection", self.roots["primary"])
        self.assertEqual(len(self.messages()), 1)
        self.assertIn("valcraft-navigation.pick", self.messages()[0])
        self.assert_no_editor()

    def test_failures_notify_and_open_nothing(self) -> None:
        for selection in (
            "hello world",
            "T-01",
            "FEAT-999/T-001",
            "T-004",
            "src/app/missing.tsx",
        ):
            with self.subTest(selection):
                self.setUp()
                self.run_entry(
                    "open-selection", self.roots["primary"], selected=selection
                )
                self.assertEqual(len(self.messages()), 1)
                self.assert_no_editor()

    def test_failure_message_opens_the_plugin_popup(self) -> None:
        self.run_entry("open-selection", self.roots["primary"], selected="T-01")
        self.assertEqual([call[:3] for call in self.herdr_calls()], [["plugin", "pane", "open"]])
        self.assertIn("malformed", self.messages()[0])
        self.assert_no_editor()

    def test_disabled_without_an_editor_record(self) -> None:
        self.overlay.unlink()
        self.run_entry("open-selection", self.roots["primary"], selected="T-002")
        self.assertIn("Editor navigation is off", self.messages()[0])
        self.assertIn("Editor navigation section", self.messages()[0])
        self.assert_no_editor()

    def test_non_valcraft_pane_is_refused(self) -> None:
        self.run_entry("open-selection", self.roots["outside"], selected="T-002")
        self.assertIn("not in a Valcraft project", self.messages()[0])
        self.assert_no_editor()

    def test_missing_editor_executable_is_refused(self) -> None:
        self.write_overlay("zed", str(self.case / "no-such-editor"))
        self.run_entry("open-selection", self.roots["primary"], selected="T-002")
        self.assertIn("missing or not executable", self.messages()[0])
        self.assert_no_editor()

    def test_unreadable_record_is_refused(self) -> None:
        self.overlay.write_text("editor: {adapter: zed}\n", encoding="utf-8")
        self.run_entry("open-selection", self.roots["primary"], selected="T-002")
        self.assertIn("Cannot read the editor record", self.messages()[0])
        self.assert_no_editor()

    def test_record_from_repository_content_is_refused(self) -> None:
        primary = self.roots["primary"]
        with self.subTest("symbolic link"):
            target = self.case / "record.yaml"
            target.write_text(f"editor:\n  adapter: zed\n  executable: {self.editor}\n", encoding="utf-8")
            self.overlay.unlink()
            self.overlay.symlink_to(target)
            self.run_entry("open-selection", primary, selected="T-002")
            self.assertIn("Refusing", self.messages()[0])
            self.assert_no_editor()
        with self.subTest("not ignored"):
            self.setUp()
            ignore = primary / ".gitignore"
            original = ignore.read_text(encoding="utf-8")
            ignore.write_text("", encoding="utf-8")
            try:
                self.run_entry("open-selection", primary, selected="T-002")
            finally:
                ignore.write_text(original, encoding="utf-8")
            self.assertIn("Refusing", self.messages()[0])
            self.assert_no_editor()
        with self.subTest("tracked under another case or normalization"):
            # A repository built on a case-sensitive filesystem tracks a variant
            # spelling; a case-insensitive clone opens it as the overlay.
            self.setUp()
            variant = ".valcraft/CONFIG.LOCAL.YAML"
            probe = primary / variant
            if probe.exists() and os.path.samefile(probe, self.overlay):
                self.overlay.unlink()
                (primary / variant).write_text(
                    f"editor:\n  adapter: zed\n  executable: {self.editor}\n", encoding="utf-8"
                )
                git(primary, "add", "--force", variant)
                try:
                    self.run_entry("open-selection", primary, selected="T-002")
                finally:
                    git(primary, "rm", "--cached", "--quiet", variant)
                    (primary / variant).unlink()
                self.assertIn("Refusing", self.messages()[0])
                self.assert_no_editor()
        with self.subTest("tracked"):
            self.setUp()
            git(primary, "add", "--force", ".valcraft/config.local.yaml")
            try:
                self.run_entry("open-selection", primary, selected="T-002")
            finally:
                git(primary, "rm", "--cached", "--quiet", ".valcraft/config.local.yaml")
            self.assertIn("Refusing", self.messages()[0])
            self.assert_no_editor()

    def test_worktree_reads_the_record_from_the_primary_checkout(self) -> None:
        worktree = self.roots["worktree"]
        self.assertFalse((worktree / ".valcraft" / "config.local.yaml").exists())
        self.run_entry("open-selection", worktree, selected="T-011")
        self.assertEqual(
            self.editor_calls(),
            [[str(self.editor), f"{worktree / 'specs/001-alpha/tasks.md'}:12:1"]],
        )

    def test_newer_repository_warns_and_still_opens(self) -> None:
        base = self.roots["primary"] / ".valcraft" / "config.yaml"
        original = base.read_text(encoding="utf-8")
        self.addCleanup(base.write_text, original, encoding="utf-8")
        base.write_text(original.replace('"0.12.2"', '"99.0.0"'), encoding="utf-8")
        self.run_entry("open-selection", self.roots["primary"], selected="T-002")
        self.assertIn("newer than this plugin's release", self.messages()[0])
        self.assertEqual(len(self.editor_calls()), 1)

    def test_older_repository_does_not_warn(self) -> None:
        base = self.roots["primary"] / ".valcraft" / "config.yaml"
        original = base.read_text(encoding="utf-8")
        self.addCleanup(base.write_text, original, encoding="utf-8")
        base.write_text(original.replace('"0.12.2"', '"0.1.0"'), encoding="utf-8")
        self.run_entry("open-selection", self.roots["primary"], selected="T-002")
        self.assertEqual(self.messages(), [])

    def test_open_link_opens_file_and_editor_links(self) -> None:
        page = self.roots["primary"] / "src/app/page.tsx"
        for url in (
            f"file://{page}#L3C2",
            f"vscode://file{page}:3:2",
            f"cursor://file{page}:3:2",
        ):
            with self.subTest(url):
                self.setUp()
                self.run_entry(
                    "open-link",
                    self.roots["primary"],
                    url=url,
                )
                self.assertEqual(
                    self.editor_calls(), [[str(self.editor), f"{page}:3:2"]]
                )

    def test_malformed_link_notifies_and_opens_nothing(self) -> None:
        self.run_entry(
            "open-link", self.roots["primary"], url="file://elsewhere.example/etc/hosts"
        )
        self.assertIn("not a supported file link", self.messages()[0])
        self.assert_no_editor()

    def test_pick_opens_the_popup(self) -> None:
        self.run_entry("pick", self.roots["primary"])
        opens = [
            call
            for call in self.herdr_calls()
            if call[:3] == ["plugin", "pane", "open"]
        ]
        self.assertEqual(
            opens,
            [
                [
                    "plugin",
                    "pane",
                    "open",
                    "--plugin",
                    "valcraft-navigation",
                    "--entrypoint",
                    "picker",
                    "--focus",
                ]
            ],
        )

    def test_picker_lists_identities_and_only_resolvable_paths(self) -> None:
        session = actions.Session(
            {}, self.roots["primary"], config.EditorRecord("zed", str(self.editor))
        )
        text = "see FEAT-001/T-002 in src/app/page.tsx:3 and src/app/missing.tsx:1\nthen T-001."
        self.assertEqual(
            picker.reference_entries(session, text),
            ["T-001", "src/app/page.tsx:3", "FEAT-001/T-002"],
        )

    def test_manifest_version_matches_the_plugin_version(self) -> None:
        manifest = (PLUGIN / "herdr-plugin.toml").read_text(encoding="utf-8")
        self.assertEqual(
            re.search(r'^version = "([^"]+)"$', manifest, re.MULTILINE).group(1),
            actions.PLUGIN_VERSION,
        )


class LinkTests(unittest.TestCase):
    def test_accepted_links(self) -> None:
        accepted = {
            "file:///a/b.py": ("/a/b.py", 1, 1),
            "file://localhost/a/b.py#L7": ("/a/b.py", 7, 1),
            f"file://{socket.gethostname()}/a/b.py#L7C3": ("/a/b.py", 7, 3),
            "file:///a/b.py#L7-L9": ("/a/b.py", 7, 1),
            "file:///a/my%20file.py": ("/a/my file.py", 1, 1),
            "vscode://file/a/b.py:7:3": ("/a/b.py", 7, 3),
            "vscode://file/a/b.py": ("/a/b.py", 1, 1),
            "cursor://file/a/b.py:7": ("/a/b.py", 7, 1),
        }
        for url, (path, line, column) in accepted.items():
            with self.subTest(url):
                self.assertEqual(links.parse(url), links.LinkTarget(path, line, column))

    def test_rejected_links(self) -> None:
        for url in (
            "https://example.com/a",
            "file://other.example/a/b.py",
            "file:///a/b.py?x=1",
            "file:///a/b.py#section",
            "file:///a/%00b.py",
            "file:///a/%ff.py",
            "file:relative.py",
            "vscode://file",
            "vscode://settings/a",
            "vscode://file/a/b.py#L3",
            "javascript:alert(1)",
        ):
            with self.subTest(url):
                self.assertIsNone(links.parse(url))


class ConfigTests(unittest.TestCase):
    def read(self, text: str):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / ".valcraft").mkdir()
            (root / ".valcraft" / "config.local.yaml").write_text(
                text, encoding="utf-8"
            )
            return config.read_editor_record(root)

    def test_reads_the_record_beside_other_overlay_keys(self) -> None:
        text = (
            "foreman:\n  backend: herdr\n  herdr:\n    session: null\n"
            'editor:\n  adapter: vscode\n  executable: "/usr/local/bin/code"\n'
            "browser:\n  codex:\n    tool: agent-browser\n"
        )
        self.assertEqual(
            self.read(text), config.EditorRecord("vscode", "/usr/local/bin/code")
        )

    def test_absent_record(self) -> None:
        self.assertIsNone(self.read("foreman:\n  approval_mode: attended\n"))
        with tempfile.TemporaryDirectory() as directory:
            self.assertIsNone(config.read_editor_record(Path(directory)))

    def test_unreadable_records(self) -> None:
        for text in (
            "editor: {adapter: zed, executable: /x}\n",
            "editor:\n  adapter: zed\n",
            "editor:\n  adapter: zed\n  executable: /x\n  extra: 1\n",
            "editor:\n  adapter: zed\n  adapter: vscode\n  executable: /x\n",
            "editor:\n  adapter: zed\n  executable: /x\neditor:\n  adapter: zed\n",
            "editor:\n  adapter: zed\n  executable: &anchor /x\n",
            "editor:\n    adapter: zed\n    executable: /x\n",
        ):
            with self.subTest(text), self.assertRaises(config.Unreadable):
                self.read(text)

    def test_valcraft_version(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / ".valcraft").mkdir()
            base = root / ".valcraft" / "config.yaml"
            base.write_text(
                'valcraft_version: "0.12.2"\n\ntracker:\n  mode: local\n',
                encoding="utf-8",
            )
            self.assertEqual(config.read_valcraft_version(root), (0, 12, 2))
            base.write_text("valcraft_version: 1.2\n", encoding="utf-8")
            self.assertIsNone(config.read_valcraft_version(root))


class ScanTests(unittest.TestCase):
    def test_scan(self) -> None:
        text = (
            "see FEAT-023/T-001 and src/app/page.tsx:42.\n"
            "then Q-004 QT-001, bare T-003 (and `README.md`) https://github.com/a/b.git\n"
            "again FEAT-023/T-001 x FEAT-1 T-001x .env ~/x/y.md:3:4"
        )
        self.assertEqual(
            scan(text),
            [
                "~/x/y.md:3:4",
                "FEAT-023/T-001",
                "README.md",
                "T-003",
                "Q-004 QT-001",
                "src/app/page.tsx:42",
            ],
        )


if __name__ == "__main__":
    unittest.main()
