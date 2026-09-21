#!/usr/bin/env python3
"""Discriminating tests for the Jev audit scripts. Static: no network, no key."""

from __future__ import annotations

import hashlib
import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parents[1]
GRADE, COMPARE, REVIEW, APPLY = (SCRIPTS / f"jev-{n}.py" for n in ("grade", "compare", "review", "apply"))
FORBIDDEN_IN_FLAGGED = ("passed", "noul", "evidence")
TEXTS = ["The report names the target", "No push occurs", "The branch is canonical", "Status line is present"]


def grading(passed: list[bool], evidence: str = "quoted") -> dict:
    total = len(passed)
    return {
        "expectations": [{"text": t, "passed": p, "evidence": evidence} for t, p in zip(TEXTS, passed)],
        "summary": {"passed": sum(passed), "failed": total - sum(passed), "total": total, "pass_rate": round(sum(passed) / total, 4)},
    }


def jev(nouls: list[float], n: int) -> dict:
    return {"assertions": TEXTS[:n], "answers": {f"a{i}": {"type": "noul", "noul": v} for i, v in enumerate(nouls)}, "usage": {"input_tokens": 100}}


class JevAuditTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary_directory = tempfile.TemporaryDirectory()
        self.runs = Path(self.temporary_directory.name)
        self.env = {k: v for k, v in os.environ.items() if k != "OPENROUTER_API_KEY"}

    def tearDown(self) -> None:
        self.temporary_directory.cleanup()

    def case(self, name: str, passed: list[bool], nouls: list[float] | None = None, evidence: str = "quoted") -> Path:
        directory = self.runs / name
        directory.mkdir(parents=True)
        (directory / "grading.json").write_text(json.dumps(grading(passed, evidence), indent=2) + "\n")
        if nouls is not None:
            (directory / "jev-grading.json").write_text(json.dumps(jev(nouls, len(passed))))
        return directory

    def run_script(self, script: Path, *args: str) -> subprocess.CompletedProcess[str]:
        return subprocess.run([sys.executable, str(script), "--runs", str(self.runs), *args], capture_output=True, text=True, env=self.env)

    def regrade(self, directory: Path, entries: list[dict]) -> None:
        (directory / "regrade.json").write_text(json.dumps({"regraded": entries}))

    def checksums(self) -> dict[str, str]:
        return {str(p): hashlib.sha256(p.read_bytes()).hexdigest() for p in self.runs.rglob("grading.json")}

    # jev-grade: request building, no network

    def test_request_body_from_fixture_case(self) -> None:
        case = self.case("valcraft-spec/eval-1/with_skill", [True, False])
        (case / "transcript.md").write_text("the transcript")
        (case / "outputs" / "specs").mkdir(parents=True)
        (case / "outputs" / "specs" / "spec.md").write_text("# Spec")
        (case / "outputs" / ".git").mkdir()
        (case / "outputs" / ".git" / "HEAD").write_text("ref: refs/heads/main")
        (case / "outputs" / "blob.bin").write_bytes(b"\xff\xfe\x00binary")
        result = self.run_script(GRADE, "--dry-run", "valcraft-spec/eval-1/with_skill")
        self.assertEqual(result.returncode, 0, result.stderr)
        body = json.loads(result.stdout)
        self.assertEqual(body["state"]["transcript"], "the transcript")
        self.assertEqual(body["state"]["outputs"], {"specs/spec.md": "# Spec"})
        self.assertEqual([q["instructions"] for q in body["questions"].values()], TEXTS[:2])
        self.assertEqual(list(body["questions"]), ["a0", "a1"])
        for q in body["questions"].values():
            self.assertEqual(q["type"], "noul")
            self.assertEqual(set(q["criteria"]), {"true", "false"})

    def test_grade_without_key_sends_nothing(self) -> None:
        self.case("valcraft-spec/eval-1/with_skill", [True])
        result = self.run_script(GRADE)
        self.assertEqual(result.returncode, 1)
        self.assertIn("OPENROUTER_API_KEY", result.stderr)
        self.assertFalse((self.runs / "valcraft-spec/eval-1/with_skill/jev-grading.json").exists())

    # jev-compare: selection rule and blindness

    def test_flag_selection_rule(self) -> None:
        # a0: pass vs 0.05 -> 0.95 apart, flagged. a1: fail vs 0.90 -> exactly 0.9, not flagged.
        # a2: pass vs 0.20 -> 0.8 apart, not flagged. a3: fail vs 0.99 but already corrected -> not flagged.
        case = self.case("valcraft-spec/eval-1/baseline", [True, False, True, False], [0.05, 0.90, 0.20, 0.99])
        g = json.loads((case / "grading.json").read_text())
        g["expectations"][3]["evidence"] = "Corrected 2026-09-21, was pass. reason"
        (case / "grading.json").write_text(json.dumps(g))
        self.case("valcraft-spec/eval-2/baseline", [True, True], [0.97, 0.99])
        self.case("valcraft-spec/eval-3/baseline", [True], None)  # no jev-grading.json: skipped
        result = self.run_script(COMPARE)
        self.assertEqual(result.returncode, 0, result.stderr)
        flagged = json.loads((self.runs / "_harness/jev-flagged.json").read_text())
        self.assertEqual(flagged, {"valcraft-spec/eval-1/baseline": [{"index": 0, "text": TEXTS[0]}]})
        self.assertIn("flagged=1 in 1 cases", result.stdout)
        calibration = (self.runs / "_harness/jev-calibration.md").read_text()
        self.assertIn("- compared: 2", calibration)
        self.assertIn("- no jev-grading.json: 1", calibration)

    def test_flagged_set_is_blind(self) -> None:
        self.case("valcraft-spec/eval-1/baseline", [True, False], [0.01, 0.99], evidence="the label's evidence")
        self.run_script(COMPARE)
        raw = (self.runs / "_harness/jev-flagged.json").read_text()
        flagged = json.loads(raw)
        for key in FORBIDDEN_IN_FLAGGED:
            self.assertNotIn(f'"{key}"', raw, f"flagged set leaks {key}")
        self.assertNotIn("the label's evidence", raw)
        for item in flagged["valcraft-spec/eval-1/baseline"]:
            self.assertEqual(set(item), {"index", "text"})

    def test_rewritten_grading_is_unusable(self) -> None:
        case = self.case("valcraft-spec/eval-1/baseline", [True], [0.5])
        g = json.loads((case / "grading.json").read_text())
        g["expectations"][0]["text"] = "rewritten"
        (case / "grading.json").write_text(json.dumps(g))
        result = self.run_script(COMPARE)
        self.assertIn("unusable=1", result.stdout)

    # jev-review: sectioning

    def test_review_sections(self) -> None:
        conflict = self.case("valcraft-spec/eval-1/baseline", [False, True], [0.99, 0.01])
        confirmed = self.case("valcraft-spec/eval-2/baseline", [True], [0.02])
        self.case("valcraft-spec/eval-3/baseline", [False], [0.98])  # flagged, no regrade.json yet
        self.regrade(conflict, [
            {"index": 0, "text": TEXTS[0], "passed": True, "evidence": "re-grade sees it", "assertion_problem": ""},
            {"index": 1, "text": TEXTS[1], "passed": True, "evidence": "agrees", "assertion_problem": "two readings"},
        ])
        self.regrade(confirmed, [{"index": 0, "text": TEXTS[0], "passed": True, "evidence": "agrees", "assertion_problem": ""}])
        self.run_script(COMPARE)
        result = self.run_script(REVIEW)
        self.assertEqual(result.returncode, 0, result.stderr)
        text = (self.runs / "_harness/jev-review.md").read_text()
        conflicts, rest = text.split("## Confirmed")
        confirmed_section, problems = rest.split("## Assertion problems")
        self.assertIn("`valcraft-spec/eval-1/baseline` a0: label fail, re-grade pass", conflicts)
        self.assertIn("re-grade sees it", conflicts)
        self.assertNotIn("eval-2", conflicts)
        self.assertIn("`valcraft-spec/eval-1/baseline` a1: pass.", confirmed_section)
        self.assertIn("`valcraft-spec/eval-2/baseline` a0: pass.", confirmed_section)
        self.assertIn("- two readings", problems)
        self.assertIn("`valcraft-spec/eval-3/baseline`", text.split("## Conflicts")[0])
        self.assertIn("Conflicts: 1. Confirmed: 2. Assertion problems: 1.", text)

    # jev-apply: exact change and refusals

    def test_apply_changes_only_the_approved_assertion(self) -> None:
        target = self.case("valcraft-spec/eval-1/baseline", [False, True, True], [0.99, 0.9, 0.9])
        self.case("valcraft-spec/eval-1/with_skill", [True], [0.9])
        self.case("valcraft-spec/eval-2/baseline", [False], [0.99])
        (self.runs / "valcraft-spec/summary.json").write_text("{}")
        self.regrade(target, [{"index": 0, "text": TEXTS[0], "passed": True, "evidence": "re-grade sees it", "assertion_problem": ""}])
        before = self.checksums()
        result = self.run_script(APPLY, "valcraft-spec/eval-1/baseline:0")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("fail -> pass", result.stdout)
        self.assertIn("valcraft-spec/summary.json", result.stdout)
        after = self.checksums()
        changed = [p for p in before if before[p] != after[p]]
        self.assertEqual(changed, [str(target / "grading.json")])
        g = json.loads((target / "grading.json").read_text())
        self.assertTrue(g["expectations"][0]["passed"])
        self.assertTrue(g["expectations"][0]["evidence"].startswith("Corrected "))
        self.assertIn(", was fail. re-grade sees it", g["expectations"][0]["evidence"])
        self.assertEqual(g["expectations"][1], {"text": TEXTS[1], "passed": True, "evidence": "quoted"})
        self.assertEqual(g["summary"], {"passed": 3, "failed": 0, "total": 3, "pass_rate": 1.0})

    def test_apply_refuses_when_label_changed_since_review(self) -> None:
        target = self.case("valcraft-spec/eval-1/baseline", [True], [0.01])
        self.regrade(target, [{"index": 0, "text": TEXTS[0], "passed": True, "evidence": "agrees", "assertion_problem": ""}])
        before = self.checksums()
        result = self.run_script(APPLY, "valcraft-spec/eval-1/baseline:0")
        self.assertEqual(result.returncode, 1)
        self.assertIn("refused, current label is pass", result.stdout)
        self.assertEqual(self.checksums(), before)

    def test_apply_refuses_on_text_mismatch(self) -> None:
        target = self.case("valcraft-spec/eval-1/baseline", [False], [0.99])
        self.regrade(target, [{"index": 0, "text": "another assertion", "passed": True, "evidence": "x", "assertion_problem": ""}])
        before = self.checksums()
        result = self.run_script(APPLY, "valcraft-spec/eval-1/baseline:0")
        self.assertEqual(result.returncode, 1)
        self.assertIn("assertion text differs", result.stdout)
        self.assertEqual(self.checksums(), before)

    def test_apply_pass_rate_precision(self) -> None:
        unrounded = self.case("valcraft-spec/eval-1/baseline", [False, False, True], [0.99, 0.9, 0.9])
        g = json.loads((unrounded / "grading.json").read_text())
        g["summary"]["pass_rate"] = 1 / 3
        (unrounded / "grading.json").write_text(json.dumps(g, indent=2) + "\n")
        self.regrade(unrounded, [{"index": 0, "text": TEXTS[0], "passed": True, "evidence": "x", "assertion_problem": ""}])
        self.run_script(APPLY, "valcraft-spec/eval-1/baseline:0")
        self.assertEqual(json.loads((unrounded / "grading.json").read_text())["summary"]["pass_rate"], 2 / 3)
        rounded = self.case("valcraft-spec/eval-2/baseline", [False, True, True, False], [0.99, 0.9, 0.9, 0.9])
        self.regrade(rounded, [{"index": 0, "text": TEXTS[0], "passed": True, "evidence": "x", "assertion_problem": ""}])
        self.run_script(APPLY, "valcraft-spec/eval-2/baseline:0")
        self.assertEqual(json.loads((rounded / "grading.json").read_text())["summary"]["pass_rate"], 0.75)

if __name__ == "__main__":
    unittest.main()
