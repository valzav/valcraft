#!/usr/bin/env python3
"""Discriminating tests for the controller Stop hook shipped to Claude Code."""

from __future__ import annotations

import json
import os
import subprocess
import tempfile
import unittest
from pathlib import Path

REPOSITORY = Path(__file__).resolve().parents[2]
HOOK = REPOSITORY / "plugins" / "valcraft" / "scripts" / "controller-stop.sh"
MANIFEST = REPOSITORY / "plugins" / "valcraft" / ".claude-plugin" / "plugin.json"

CONTROLLER = "11111111-2222-4333-8444-555555555555"
WORKER = "66666666-7777-4888-9999-aaaaaaaaaaaa"
AWAIT = {
    "id": "b1example",
    "type": "shell",
    "status": "running",
    "description": "Await the forge worker",
    "command": "herdr agent wait forge-f001-t002-d000 --until idle --until done",
}
CLAIM_TIME = 1_000_000_000


def payload(session: str = CONTROLLER, **fields: object) -> str:
    body: dict[str, object] = {
        "session_id": session,
        "hook_event_name": "Stop",
        "stop_hook_active": False,
        "last_assistant_message": "T-001 landed. Now starting T-002.",
        "background_tasks": [],
        "session_crons": [],
    }
    body.update(fields)
    # Claude Code emits compact JSON, and the hook's patterns rely on it.
    return json.dumps(
        {k: v for k, v in body.items() if v is not None}, separators=(",", ":")
    )


class ControllerStopHookTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary_directory = tempfile.TemporaryDirectory()
        self.root = Path(self.temporary_directory.name).resolve()
        self.git("init", "-q")
        self.foreman = self.root / ".valcraft" / "foreman"

    def tearDown(self) -> None:
        self.temporary_directory.cleanup()

    def git(self, *arguments: str) -> None:
        subprocess.run(
            [
                "git",
                "-c",
                "user.name=t",
                "-c",
                "user.email=t@example.invalid",
                *arguments,
            ],
            cwd=self.root,
            check=True,
            capture_output=True,
        )

    def claim(self, session: str = CONTROLLER, generation: int = 1) -> None:
        self.foreman.mkdir(parents=True, exist_ok=True)
        lock = self.foreman / f"controller.lock.{generation}"
        lock.write_text(
            f"session demo, workspace w3, pane w3:p1, agent_session {session}\n"
        )
        os.utime(lock, (CLAIM_TIME, CLAIM_TIME))

    def checkpoints(self, text: str, age: int = 60) -> None:
        state = self.foreman / "2026-09-20-001" / "state.md"
        state.parent.mkdir(parents=True, exist_ok=True)
        state.write_text(text)
        os.utime(state, (CLAIM_TIME + age, CLAIM_TIME + age))

    def run_hook(self, stdin: str) -> str:
        result = subprocess.run(
            ["sh", str(HOOK)],
            input=stdin,
            capture_output=True,
            text=True,
            env={**os.environ, "CLAUDE_PROJECT_DIR": str(self.root)},
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(result.stderr, "")
        return result.stdout

    def assert_blocks(self, stdin: str, mentions: str) -> None:
        decision = json.loads(self.run_hook(stdin))
        self.assertEqual(decision["decision"], "block")
        self.assertIn(mentions, decision["reason"])

    def assert_allows(self, stdin: str) -> None:
        self.assertEqual(self.run_hook(stdin), "")

    def test_manifest_runs_this_script_on_stop(self) -> None:
        hooks = json.loads(MANIFEST.read_text())["hooks"]["Stop"][0]["hooks"]
        self.assertEqual(
            [(hook["command"], hook["args"]) for hook in hooks],
            [("sh", ["${CLAUDE_PLUGIN_ROOT}/scripts/controller-stop.sh"])],
        )

    def test_repository_without_valcraft_may_stop(self) -> None:
        self.assert_allows(payload())

    def test_controller_with_nothing_armed_is_blocked(self) -> None:
        self.claim()
        self.checkpoints("## CP-027 T-001 LANDED; -> Ready\n\nNamed state: Ready\n")
        self.assert_blocks(payload(), "next transition")

    def test_second_stop_after_a_block_may_stop(self) -> None:
        self.claim()
        self.checkpoints("## CP-027 T-001 LANDED; -> Ready\n")
        self.assert_allows(payload(stop_hook_active=True))

    def test_worker_session_may_stop(self) -> None:
        self.claim()
        self.checkpoints("## CP-027 T-001 LANDED; -> Ready\n")
        self.assert_allows(payload(session=WORKER))

    def test_highest_lease_generation_names_the_owner(self) -> None:
        self.claim(generation=1)
        self.claim(session=WORKER, generation=2)
        self.checkpoints("## CP-027 T-001 LANDED; -> Ready\n")
        self.assert_allows(payload())

    def test_armed_await_may_stop_without_a_turn_end_line(self) -> None:
        self.claim()
        self.checkpoints("## CP-028 Dispatch forge; await armed\n")
        self.assert_allows(payload(background_tasks=[AWAIT]))

    def test_prose_about_an_await_does_not_count_as_one(self) -> None:
        self.claim()
        self.checkpoints("## CP-027 T-001 LANDED; -> Ready\n")
        message = (
            'I armed "herdr agent wait forge-f001-t002-d000" and will report again.'
        )
        self.assert_blocks(payload(last_assistant_message=message), "next transition")

    def test_task_description_naming_the_wait_does_not_count_as_one(self) -> None:
        self.claim()
        self.checkpoints("## CP-027 T-001 LANDED; -> Ready\n")
        follower = {
            "id": "log-follower",
            "type": "shell",
            "status": "running",
            "description": "Follow diagnostic output for herdr agent wait",
            "command": "tail -f /tmp/worker.log",
        }
        self.assert_blocks(payload(background_tasks=[follower]), "next transition")
        self.assert_allows(payload(background_tasks=[follower, AWAIT]))

    def test_gate_and_completion_may_stop(self) -> None:
        self.claim()
        for line in (
            "Turn end: gate FeatureClose confirmation",
            "- `Turn end: complete`",
        ):
            with self.subTest(line=line):
                self.checkpoints(f"## CP-150 All tasks landed\n\n{line}\n")
                self.assert_allows(payload())

    def test_turn_end_line_of_an_earlier_checkpoint_is_stale(self) -> None:
        self.claim()
        self.checkpoints(
            "## CP-026 Pick gate\n\nTurn end: gate Ready pick\n\n## CP-027 T-001 LANDED; -> Ready\n"
        )
        self.assert_blocks(payload(), "next transition")

    def test_recorded_await_is_checked_against_the_task_list(self) -> None:
        self.claim()
        self.checkpoints("## CP-028 Dispatch forge\n\nTurn end: await b1example\n")
        self.assert_blocks(payload(), "next transition")
        self.assert_allows(payload(background_tasks=None))

    def test_unreadable_checkpoint_may_stop(self) -> None:
        self.claim()
        self.checkpoints("## CP-027 T-001 LANDED; -> Ready\n")
        self.assert_blocks(payload(), "next transition")
        state = self.foreman / "2026-09-20-001" / "state.md"
        state.chmod(0)
        if os.access(state, os.R_OK):
            self.skipTest("this user reads a mode-000 file")
        self.assert_allows(payload())

    def test_unreadable_lease_may_stop(self) -> None:
        self.claim(session=WORKER)
        config = self.root / ".valcraft" / "config.yaml"
        config.write_text("valcraft_version: 0.8.3\n")
        self.assert_blocks(
            payload(last_assistant_message="Status: done"), "continue the Cast run"
        )
        lease = self.foreman / "controller.lock.1"
        lease.chmod(0)
        if os.access(lease, os.R_OK):
            self.skipTest("this user reads a mode-000 file")
        self.assert_allows(payload(last_assistant_message="Status: done"))

    def test_controller_before_its_first_checkpoint_may_stop(self) -> None:
        self.claim()
        self.assert_allows(payload())
        self.checkpoints("## CP-150 Earlier run, no turn-end line\n", age=-60)
        self.assert_allows(payload())

    def test_cast_stopped_on_nested_tune_report_is_blocked(self) -> None:
        config = self.root / ".valcraft" / "config.yaml"
        config.parent.mkdir()
        config.write_text("valcraft_version: 0.8.2\n")
        for ending in (
            "Status: done",
            "Commit: none.\n```text\nStatus: done\n```\n",
            "**Status: done**",
        ):
            with self.subTest(ending=ending):
                self.assert_blocks(
                    payload(last_assistant_message=ending), "continue the Cast run"
                )
        self.assert_allows(
            payload(last_assistant_message="Which tracker mode do you want?")
        )

    def test_cast_beside_a_retained_dead_lease_is_blocked(self) -> None:
        # An interrupted Foreman run left its lease; this session never owned it.
        self.claim(session=WORKER)
        config = self.root / ".valcraft" / "config.yaml"
        config.write_text("valcraft_version: 0.8.3\n")
        self.assert_blocks(
            payload(last_assistant_message="Status: done"), "continue the Cast run"
        )

    def test_committed_base_under_status_done_may_stop(self) -> None:
        config = self.root / ".valcraft" / "config.yaml"
        config.parent.mkdir()
        config.write_text("valcraft_version: 0.8.2\n")
        self.git("add", ".valcraft/config.yaml")
        self.git("commit", "-q", "-m", "base")
        self.assert_allows(payload(last_assistant_message="Status: done"))


if __name__ == "__main__":
    unittest.main()
