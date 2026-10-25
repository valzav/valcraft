#!/usr/bin/env python3
"""End-to-end check of the Herdr plugin in a disposable Herdr session.

Run it from a shell inside a Herdr pane:

    python3 navigation/tests/herdr_e2e.py

It splits the current pane, starts an isolated named Herdr session there
(its own XDG_CONFIG_HOME, XDG_STATE_HOME, and config file under /var/tmp),
links navigation/herdr into it, and drives the session's keyboard and mouse
through the outer pane. A fake editor records each launch. The script stops
and deletes the session and closes the outer pane when it ends, pass or fail.
It never addresses the caller's own session except to split and close the
outer pane it created.
"""

from __future__ import annotations

import json
import os
import shutil
import subprocess
import sys
import time
from pathlib import Path
from typing import Callable, List, Optional

NAVIGATION = Path(__file__).resolve().parents[1]
PLUGIN = NAVIGATION / "herdr"
# Bounds for waiting on a live terminal. The 2026-10-25 trial session was
# ready within 4 s and every UI reaction within 2 s; these leave headroom.
STARTUP_SECONDS = 30
REACTION_SECONDS = 10
ESC = "\x1b"

FAKE_EDITOR = """#!{python}
import json, sys
with open({log!r}, "a") as log:
    log.write(json.dumps(sys.argv[1:]) + "\\n")
"""
NESTED_CONFIG = """onboarding = false

[experimental]
allow_nested = true

[ui]
copy_on_select = false

# Herdr shows no notification while toast delivery is off, its default.
[ui.toast]
delivery = "herdr"

[[keys.command]]
key = "prefix+u"
type = "plugin_action"
command = "valcraft-navigation.pick"

[[keys.command]]
key = "prefix+y"
type = "plugin_action"
command = "valcraft-navigation.open-selection"
"""
# Printed by `cat refs`, oldest first. The picker lists them newest first.
REFERENCES = (
    "one src/app/page.tsx:3:2\ntwo Q-001 QT-002 and FEAT-001/T-001\nthree T-001\n"
)
EXPECTED_MENU = ["T-001", "FEAT-001/T-001", "Q-001 QT-002", "src/app/page.tsx:3:2"]


def wait_for(
    description: str,
    probe: Callable[[], Optional[object]],
    seconds: float = REACTION_SECONDS,
):
    deadline = time.monotonic() + seconds
    while time.monotonic() < deadline:
        value = probe()
        if value:
            return value
        time.sleep(0.2)
    raise AssertionError(f"timed out waiting for {description}")


class Harness:
    def __init__(self) -> None:
        stamp = time.strftime("%Y%m%d%H%M%S")
        # Short names: macOS limits a Unix socket path to 104 bytes, and the
        # session socket lives under XDG_CONFIG_HOME/herdr/sessions/<session>/.
        self.root = Path(os.path.realpath(f"/var/tmp/vne-{stamp}"))
        self.session = f"vne-{stamp}"
        self.outer: Optional[str] = None
        self.editor_log = self.root / "editor.log"
        self.checkout = self.root / "checkout"

    # The caller's session: used only to create, drive, and close the outer pane.
    def parent(self, *arguments: str) -> str:
        return subprocess.run(
            ["herdr", *arguments], check=True, capture_output=True, text=True
        ).stdout

    # The disposable session.
    def nested(self, *arguments: str, check: bool = True) -> str:
        environ = {
            key: value
            for key, value in os.environ.items()
            if key
            not in (
                "HERDR_SOCKET_PATH",
                "HERDR_CLIENT_SOCKET_PATH",
                "HERDR_WORKSPACE_ID",
                "HERDR_TAB_ID",
                "HERDR_PANE_ID",
            )
        }
        environ.update(self.isolation(), HERDR_SESSION=self.session)
        return subprocess.run(
            ["herdr", *arguments],
            check=check,
            capture_output=True,
            text=True,
            env=environ,
        ).stdout

    def isolation(self) -> dict:
        return {
            "HERDR_CONFIG_PATH": str(self.root / "config.toml"),
            "XDG_CONFIG_HOME": str(self.root / "c"),
            "XDG_STATE_HOME": str(self.root / "s"),
        }

    def keys(self, *keys: str) -> None:
        self.parent("pane", "send-keys", self.outer, *keys)

    def text(self, text: str) -> None:
        self.parent("pane", "send-text", self.outer, text)

    def screen(self) -> List[str]:
        return self.parent(
            "pane", "read", self.outer, "--source", "visible"
        ).splitlines()

    def editor_calls(self) -> List[List[str]]:
        if not self.editor_log.exists():
            return []
        return [json.loads(line) for line in self.editor_log.read_text().splitlines()]

    def expect_editor(self, count: int, arguments: List[str], what: str) -> None:
        calls = wait_for(
            f"editor launch for {what}",
            lambda: (lambda calls: calls if len(calls) >= count else None)(
                self.editor_calls()
            ),
        )
        assert (
            calls[count - 1] == arguments
        ), f"{what}: editor got {calls[count - 1]}, expected {arguments}"
        print(f"ok  {what}: {' '.join(arguments)}")

    def prepare(self) -> None:
        self.root.mkdir(parents=True)
        (self.root / "config.toml").write_text(NESTED_CONFIG, encoding="utf-8")
        editor = self.root / "editor"
        editor.write_text(
            FAKE_EDITOR.format(python=sys.executable, log=str(self.editor_log)),
            encoding="utf-8",
        )
        editor.chmod(0o755)
        shutil.copytree(NAVIGATION / "fixtures" / "checkout", self.checkout)
        git = [
            "git",
            "-c",
            "user.name=Fixture",
            "-c",
            "user.email=fixture@example.invalid",
        ]
        subprocess.run([*git, "init", "--quiet"], cwd=self.checkout, check=True)
        subprocess.run([*git, "add", "--all"], cwd=self.checkout, check=True)
        subprocess.run(
            [*git, "commit", "--quiet", "-m", "fixture"], cwd=self.checkout, check=True
        )
        (self.checkout / ".valcraft" / "config.local.yaml").write_text(
            f"editor:\n  adapter: zed\n  executable: {editor}\n", encoding="utf-8"
        )
        (self.checkout / "refs").write_text(REFERENCES, encoding="utf-8")
        page = self.checkout / "src/app/page.tsx"
        (self.checkout / "link").write_text(
            f"{ESC}]8;;file://{page}#L4C1{ESC}\\E2ELINK{ESC}]8;;{ESC}\\\n",
            encoding="utf-8",
        )

    def start(self) -> None:
        split = json.loads(
            self.parent(
                "pane",
                "split",
                "--pane",
                os.environ["HERDR_PANE_ID"],
                "--direction",
                "down",
                "--cwd",
                str(self.root),
                "--no-focus",
            )
        )
        self.outer = split["result"]["pane"]["pane_id"]
        unset = "-u HERDR_SOCKET_PATH -u HERDR_CLIENT_SOCKET_PATH -u HERDR_SESSION -u HERDR_WORKSPACE_ID -u HERDR_TAB_ID -u HERDR_PANE_ID"
        isolation = " ".join(
            f"{key}={value}" for key, value in self.isolation().items()
        )
        self.parent(
            "pane",
            "run",
            self.outer,
            f"env {unset} {isolation} herdr --session {self.session}",
        )
        wait_for(
            "the disposable session", lambda: self.session_running(), STARTUP_SECONDS
        )
        print(f"ok  session {self.session} started in pane {self.outer}")
        linked = json.loads(self.nested("plugin", "link", str(PLUGIN)))
        assert linked["result"]["plugin"]["plugin_id"] == "valcraft-navigation", linked
        panes = json.loads(self.nested("pane", "list"))["result"]["panes"]
        self.inner = panes[0]["pane_id"]
        self.nested(
            "pane", "run", self.inner, f"cd {self.checkout} && clear && cat refs"
        )
        wait_for(
            "the printed references",
            lambda: any("three T-001" in line for line in self.screen()),
        )

    def session_running(self) -> bool:
        listing = self.nested("session", "list", check=False)
        return any(
            line.split()[:2] == [self.session, "running"]
            for line in listing.splitlines()
        )

    def menu_labels(self, title: str) -> List[str]:
        def labels() -> Optional[List[str]]:
            lines = self.screen()
            for index, line in enumerate(lines):
                if title in line:
                    found = []
                    for below in lines[index + 1 :]:
                        if "Enter open" in below:
                            return found
                        cell = below.split("│")
                        text = cell[2].strip() if len(cell) > 2 else ""
                        if text:
                            found.append(text)
            return None

        return wait_for(f"menu {title!r}", labels)

    def run(self) -> None:
        tasks = str(self.checkout / "specs/001-alpha/tasks.md")
        quick = str(self.checkout / "specs/quick/001-first.md")
        page = str(self.checkout / "src/app/page.tsx")

        # Pane picker: every listed reference, newest first.
        self.keys("ctrl+b", "u")
        labels = self.menu_labels("Open in editor:")
        assert labels == EXPECTED_MENU, f"picker listed {labels}"
        print(f"ok  pane picker lists {labels}")
        self.keys("esc")
        wait_for(
            "the picker to close",
            lambda: not any("Open in editor:" in line for line in self.screen()),
        )
        assert self.editor_calls() == [], "Escape opened something"
        print("ok  Escape closes the picker and opens nothing")

        # A failure reaches the user as a Herdr notification.
        self.keys("ctrl+b", "y")
        wait_for("the no-selection notification", lambda: any("No text is selected" in line for line in self.screen()))
        assert self.editor_calls() == [], "an empty selection opened something"
        print("ok  open key without a selection shows a notification")

        expected = {
            "FEAT-001/T-001": [f"{tasks}:14:1"],
            "Q-001 QT-002": [f"{quick}:11:1"],
            "src/app/page.tsx:3:2": [f"{page}:3:2"],
        }
        count = 0
        for position, label in enumerate(EXPECTED_MENU):
            if label not in expected:
                continue
            self.keys("ctrl+b", "u")
            self.menu_labels("Open in editor:")
            if position:
                self.keys(*(["j"] * position))
            self.keys("enter")
            count += 1
            self.expect_editor(count, expected[label], f"picker choice {label}")

        # An ambiguous bare identity opens the second-level picker.
        self.keys("ctrl+b", "u")
        self.menu_labels("Open in editor:")
        self.keys("enter")
        candidates = self.menu_labels("Several definitions match")
        assert [label.split()[0] for label in candidates] == [
            "FEAT-001/T-001",
            "FEAT-002/T-001",
            "FEAT-003/T-001",
        ], candidates
        self.keys("j", "enter")
        count += 1
        self.expect_editor(
            count,
            [f"{self.checkout / 'specs/002-beta/tasks.md'}:10:1"],
            "ambiguous T-001, second candidate",
        )

        # Open-selection with a copy-mode selection.
        self.keys("ctrl+b", "[", "?")
        self.text("FEAT-001/T-001")
        self.keys("enter", "v", "E")
        self.keys("ctrl+b", "y")
        count += 1
        self.expect_editor(
            count, [f"{tasks}:14:1"], "copy-mode selection FEAT-001/T-001"
        )
        self.keys("q")  # leave copy mode so the pane shows new output

        # Control-click on an OSC 8 file link.
        self.nested("pane", "run", self.inner, "clear && cat link")
        row, column = wait_for("the link", lambda: self.find("E2ELINK"))
        self.text(f"{ESC}[<16;{column + 3};{row}M{ESC}[<16;{column + 3};{row}m")
        count += 1
        self.expect_editor(count, [f"{page}:4:1"], "Control-click on a file:// link")

    def find(self, text: str):
        for index, line in enumerate(self.screen()):
            if text in line:
                return index + 1, line.index(text) + 1
        return None

    def cleanup(self) -> None:
        if self.outer is None:
            return
        self.nested("session", "stop", self.session, check=False)
        self.nested("session", "delete", self.session, check=False)
        time.sleep(1)
        self.parent("pane", "close", self.outer)
        print(f"ok  cleaned up session {self.session} and pane {self.outer}")


def main() -> int:
    if os.environ.get("HERDR_ENV") != "1" or "HERDR_PANE_ID" not in os.environ:
        print("Run this from a shell inside a Herdr pane.", file=sys.stderr)
        return 2
    harness = Harness()
    try:
        harness.prepare()
        harness.start()
        harness.run()
    except Exception:
        if harness.outer is not None:
            print(
                "--- outer pane at failure:",
                *harness.screen(),
                sep="\n",
                file=sys.stderr,
            )
        raise
    finally:
        harness.cleanup()
    print(f"PASS  evidence kept in {harness.root}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
