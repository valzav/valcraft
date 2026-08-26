#!/usr/bin/env python3
"""Discriminating tests for the coordination-contract drift checker."""

from __future__ import annotations

import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

REPOSITORY = Path(__file__).resolve().parents[2]
CHECKER = REPOSITORY / "scripts" / "check-coordination-contracts.py"
PRODUCERS = (
    "valcraft-cast",
    "valcraft-draft",
    "valcraft-forge",
    "valcraft-review",
    "valcraft-land",
    "valcraft-spec",
    "valcraft-temper",
)
CONTRACTS = "plugins/valcraft/skills/valcraft-foreman/references/contracts.md"
DRAFT_CONTRACT = "plugins/valcraft/skills/valcraft-draft/references/plan-contract.md"
BACKENDS = "plugins/valcraft/skills/valcraft-foreman/references/backends/README.md"
SUBAGENTS = "plugins/valcraft/skills/valcraft-foreman/references/backends/subagents.md"
FOREMAN_EVALS = "plugins/valcraft/skills/valcraft-foreman/evals/evals.json"
FOREMAN_SKILL = "plugins/valcraft/skills/valcraft-foreman/SKILL.md"
PRIOR_STATE_PRESENTATION_CONTRACT = (
    "Never replay another Valcraft skill's report. Omit unrelated prior state. "
    "When relevant prior state is necessary, summarize it in one prose paragraph "
    "containing only the prior outcome, exact target, relevant blocker or handoff, "
    "and one suggested next action. The suggested action is advisory and grants no "
    "authority."
)
FORGE_MESSAGE_ROW = (
    "| Task implementation and PR | Forge | Foreman, Review | "
    "[`../../valcraft-forge/references/verification-and-handoff.md#forge-report`]"
    "(../../valcraft-forge/references/verification-and-handoff.md#forge-report) | "
    "Implementing | `ForgeResult` |\n"
)


class CoordinationContractCheckTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary_directory = tempfile.TemporaryDirectory()
        self.root = Path(self.temporary_directory.name)
        source = REPOSITORY / "plugins" / "valcraft" / "skills"
        target = self.root / "plugins" / "valcraft" / "skills"
        target.mkdir(parents=True)
        for skill in ("valcraft-foreman", *PRODUCERS):
            shutil.copytree(source / skill, target / skill)

    def tearDown(self) -> None:
        self.temporary_directory.cleanup()

    def run_check(self) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [sys.executable, str(CHECKER), str(self.root)],
            capture_output=True,
            text=True,
        )

    def replace(self, relative_path: str, old: str, new: str) -> None:
        path = self.root / relative_path
        text = path.read_text()
        self.assertIn(old, text)
        path.write_text(text.replace(old, new, 1))

    def assert_check_fails(self, expected: str) -> None:
        result = self.run_check()
        self.assertNotEqual(result.returncode, 0, result.stdout)
        self.assertIn(expected, result.stderr)

    def test_shipped_contracts_are_consistent(self) -> None:
        result = self.run_check()
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("static coordination contracts are consistent", result.stdout)
        self.assertIn("does not prove runtime behavior", result.stdout)

    def test_broken_registry_contract_link_fails(self) -> None:
        self.replace(
            CONTRACTS,
            "](../../valcraft-draft/references/plan-contract.md#report)",
            "](../../valcraft-draft/references/missing.md#report)",
        )
        self.assert_check_fails("contract link does not resolve")

    def test_broken_registry_contract_anchor_fails(self) -> None:
        self.replace(
            CONTRACTS,
            "](../../valcraft-draft/references/plan-contract.md#report)",
            "](../../valcraft-draft/references/plan-contract.md#missing-anchor)",
        )
        self.assert_check_fails("contract anchor does not resolve")

    def test_report_heading_order_drift_fails(self) -> None:
        self.replace(
            DRAFT_CONTRACT,
            "### Plan\n\n<!-- plan path; canonical branch; physical branch or none -->",
            "### MSW\n\n<!-- plan path; canonical branch; physical branch or none -->",
        )
        self.assert_check_fails("report heading order drift")

    def test_producer_code_missing_from_registry_fails(self) -> None:
        self.replace(
            DRAFT_CONTRACT,
            "Use these blocked-status routing codes:\n",
            "Use these blocked-status routing codes:\n\n"
            "- `new_contract_blocker` — a fixture-only declared outcome.\n",
        )
        self.assert_check_fails("producer codes absent from registry")

    def test_registry_code_missing_from_producer_fails(self) -> None:
        self.replace(
            CONTRACTS,
            "`assignment_invalid`, `workspace_not_ready`",
            "`registry_only_code`, `assignment_invalid`, `workspace_not_ready`",
        )
        self.assert_check_fails("registry codes absent from producer")

    def test_deleted_message_registry_row_fails(self) -> None:
        self.replace(
            CONTRACTS,
            FORGE_MESSAGE_ROW,
            "",
        )
        self.assert_check_fails("message registry entries differ")

    def test_missing_prior_state_presentation_contract_fails(self) -> None:
        self.replace(FOREMAN_SKILL, PRIOR_STATE_PRESENTATION_CONTRACT, "")
        self.assert_check_fails(
            "prior-state presentation contract must appear exactly once in "
            f"{FOREMAN_SKILL}; observed=0"
        )

    def test_drifted_prior_state_presentation_contract_fails(self) -> None:
        self.replace(
            FOREMAN_SKILL,
            PRIOR_STATE_PRESENTATION_CONTRACT,
            PRIOR_STATE_PRESENTATION_CONTRACT.replace(
                "one suggested next action", "a suggested next action"
            ),
        )
        self.assert_check_fails(
            "prior-state presentation contract must appear exactly once in "
            f"{FOREMAN_SKILL}; observed=0"
        )

    def test_duplicate_message_registry_row_fails(self) -> None:
        self.replace(CONTRACTS, FORGE_MESSAGE_ROW, FORGE_MESSAGE_ROW * 2)
        self.assert_check_fails("duplicate message registry entry")

    def test_routing_code_without_transition_fails(self) -> None:
        self.replace(
            CONTRACTS,
            "| `assignment_invalid`, `workspace_not_ready`, `review_target_mismatch`, `msw_failed`, `git_write_failed`, `authority_drift`, `push_failed` | `Blocked` |",
            "| `assignment_invalid`, `workspace_not_ready`, `review_target_mismatch`, `msw_failed`, `git_write_failed`, `authority_drift`, `push_failed` |  |",
        )
        self.assert_check_fails("routing codes have no transition")

    def test_routing_code_with_conflicting_transition_fails(self) -> None:
        row = "| `draft_required` | `Drafting` |\n"
        self.replace(CONTRACTS, row, row + "| `draft_required` | `Blocked` |\n")
        self.assert_check_fails("maps to both Drafting and Blocked")

    def test_missing_backend_return_fails(self) -> None:
        self.replace(
            CONTRACTS,
            "| `dead` | terminal | `DeadWorkerRecovery` |\n",
            "",
        )
        self.assert_check_fails("backend returns differ")

    def test_duplicate_backend_return_fails(self) -> None:
        row = "| `dead` | terminal | `DeadWorkerRecovery` |\n"
        self.replace(CONTRACTS, row, row + row)
        self.assert_check_fails("duplicate backend return")

    def test_conflicting_backend_return_fails(self) -> None:
        row = "| `dead` | terminal | `DeadWorkerRecovery` |\n"
        self.replace(
            CONTRACTS,
            row,
            row + "| `dead` | nonterminal | `ReportValidation` |\n",
        )
        self.assert_check_fails("duplicate backend return")

    def test_backend_await_effect_drift_fails(self) -> None:
        self.replace(
            CONTRACTS,
            "| `dead` | terminal | `DeadWorkerRecovery` |",
            "| `dead` | nonterminal | `DeadWorkerRecovery` |",
        )
        self.assert_check_fails("backend return dead differs")

    def test_backend_transition_drift_fails(self) -> None:
        self.replace(
            CONTRACTS,
            "| `dead` | terminal | `DeadWorkerRecovery` |",
            "| `dead` | terminal | `ReportValidation` |",
        )
        self.assert_check_fails("backend return dead differs")

    def test_unexpected_backend_return_fails(self) -> None:
        row = "| `dead` | terminal | `DeadWorkerRecovery` |\n"
        self.replace(
            CONTRACTS,
            row,
            row + "| `surprise` | terminal | `ReportValidation` |\n",
        )
        self.assert_check_fails("unexpected=['surprise']")

    def test_unregistered_concrete_backend_fails(self) -> None:
        source = self.root / SUBAGENTS
        source.with_name("future.md").write_text(source.read_text())
        self.assert_check_fails("backend conformance registry differs")

    def test_backend_without_land_execution_contract_fails(self) -> None:
        self.replace(SUBAGENTS, "## Land execution", "## Landing")
        self.assert_check_fails("backend lacks Land execution contract")

    def test_backend_name_must_match_reference_and_heading(self) -> None:
        self.replace(
            BACKENDS,
            "| `subagents` | [`subagents.md`](subagents.md) | Foreman eval 68 |",
            "| `native` | [`subagents.md`](subagents.md) | Foreman eval 68 |",
        )
        self.assert_check_fails("backend conformance name differs")

    def test_backend_land_execution_mapping_must_be_complete(self) -> None:
        self.replace(
            SUBAGENTS,
            "| Permission return | `permission_blocked` |",
            "| Permission return | none |",
        )
        self.assert_check_fails("backend permission mapping is incomplete")

    def test_backend_land_execution_capability_must_be_shared(self) -> None:
        self.replace(
            SUBAGENTS,
            "| Execution capability | `shared backend permission` |",
            "| Execution capability | `dispatch-scoped permission` |",
        )
        self.assert_check_fails("backend execution capability is invalid")

    def test_backend_land_execution_signal_must_be_concrete(self) -> None:
        self.replace(
            SUBAGENTS,
            "| Permission signal | native host permission prompt or host-enforced denial |",
            "| Permission signal | none |",
        )
        self.assert_check_fails("backend permission signal is incomplete")

    def test_backend_conformance_with_unrelated_eval_fails(self) -> None:
        self.replace(
            BACKENDS,
            "| `subagents` | [`subagents.md`](subagents.md) | Foreman eval 68 |",
            "| `subagents` | [`subagents.md`](subagents.md) | Foreman eval 8 |",
        )
        self.assert_check_fails("does not load backend conformance reference")

    def test_backend_conformance_eval_metadata_is_reciprocal(self) -> None:
        path = self.root / FOREMAN_EVALS
        text = path.read_text()
        self.assertIn('"backend_conformance": [\n        "subagents"', text)
        path.write_text(
            text.replace(
                '"backend_conformance": [\n        "subagents"',
                '"backend_conformance": [\n        "native"',
                1,
            )
        )
        self.assert_check_fails("does not reciprocally name backend")

    def test_backend_conformance_eval_cannot_be_reused(self) -> None:
        self.replace(
            BACKENDS,
            "| `subagents` | [`subagents.md`](subagents.md) | Foreman eval 68 |",
            "| `subagents` | [`subagents.md`](subagents.md) | Foreman eval 69 |",
        )
        self.assert_check_fails("backend conformance reuses Foreman eval")

    def test_transport_deviation_without_eval_reference_fails(self) -> None:
        self.replace(
            BACKENDS,
            "| Claude Code native | completion event wakes the parent after it ends the turn | wake/await | `transport:claude-event-wake` | Foreman eval 7 |",
            "| Claude Code native | completion event wakes the parent after it ends the turn | wake/await | `transport:claude-event-wake` | none |",
        )
        self.assert_check_fails("active transport deviation has no named eval")

    def test_transport_deviation_with_unknown_eval_fails(self) -> None:
        # Anchor on the whole row: "Foreman eval 7" is a prefix of every 7x id, and
        # replace() takes the first occurrence, so a bare-substring anchor silently
        # retargets whichever table happens to mention such an id first.
        self.replace(
            BACKENDS,
            "| Claude Code native | completion event wakes the parent after it ends the turn | wake/await | `transport:claude-event-wake` | Foreman eval 7 |",
            "| Claude Code native | completion event wakes the parent after it ends the turn | wake/await | `transport:claude-event-wake` | Foreman eval 999 |",
        )
        self.assert_check_fails("active transport deviation names missing eval")

    def test_transport_deviation_with_unrelated_eval_fails(self) -> None:
        self.replace(
            BACKENDS,
            "| Claude Code native | completion event wakes the parent after it ends the turn | wake/await | `transport:claude-event-wake` | Foreman eval 7 |",
            "| Claude Code native | completion event wakes the parent after it ends the turn | wake/await | `transport:claude-event-wake` | Foreman eval 8 |",
        )
        self.assert_check_fails("does not reciprocally name coverage key")

    def test_transport_eval_with_unregistered_coverage_key_fails(self) -> None:
        path = self.root / FOREMAN_EVALS
        text = path.read_text()
        self.assertIn('"coordination_coverage": "transport:claude-event-wake"', text)
        path.write_text(
            text.replace(
                '"coordination_coverage": "transport:claude-event-wake"',
                '"coordination_coverage": "transport:unregistered"',
                1,
            )
        )
        self.assert_check_fails("coverage has no active deviation")

    def test_transport_deviation_cursor_row_requires_eval(self) -> None:
        self.replace(
            BACKENDS,
            "| Cursor native | parent remains active; the Task tool call holds the turn until the worker returns | wake/await | `transport:cursor-foreground-task` | Foreman eval 91 |",
            "| Cursor native | parent remains active; the Task tool call holds the turn until the worker returns | wake/await | `transport:cursor-foreground-task` | none |",
        )
        self.assert_check_fails("active transport deviation has no named eval")


if __name__ == "__main__":
    unittest.main()
