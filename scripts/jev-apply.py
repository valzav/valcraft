#!/usr/bin/env python3
"""Apply operator-approved conflicts from jev-review.md to grading.json files.

Usage: jev-apply.py --runs <dir> <case>:<index> ...   e.g. valcraft-spec/eval-18/with_skill:4

For each argument, the current label must still be the one jev-review.md showed, that is, the
opposite of the re-grader's verdict; otherwise the script refuses that argument and writes
nothing for it. It sets passed to the re-grader's verdict, prefixes the evidence with the prior
value, recomputes the case summary at the file's existing pass_rate precision, and writes by
temporary file and rename. It then names every summary.json, aggregate.json, and SUMMARY.md in
the skill's run directory as stale; reconciling those is a manual step (docs/evals.md).
"""

from __future__ import annotations

import argparse
import datetime
import glob
import json
import os
import re
import sys


def verdict(passed) -> str:
    return "pass" if passed else "fail"


def pass_rate_like(old, passed: int, total: int) -> float:
    """Recompute pass_rate at the file's precision: unrounded stays unrounded, else the grader's 4 decimals."""
    exact = passed / total if total else 0.0
    if isinstance(old, (int, float)) and old != round(old, 4):
        return exact
    return round(exact, 4)


def apply(runs: str, arg: str, today: str) -> tuple[bool, str]:
    case, _, index = arg.rpartition(":")
    i = int(index)
    path = f"{runs}/{case}/grading.json"
    raw = open(path, encoding="utf-8").read()
    grading = json.loads(raw)
    key = "expectations" if "expectations" in grading else "assertions"
    label = grading[key][i]
    regraded = {r["index"]: r for r in json.load(open(f"{runs}/{case}/regrade.json"))["regraded"]}
    if i not in regraded:
        return False, f"{arg}: refused, a{i} is not in regrade.json"
    if regraded[i]["text"] != label["text"]:
        return False, f"{arg}: refused, assertion text differs between regrade.json and grading.json"
    if bool(label["passed"]) == bool(regraded[i]["passed"]):
        return False, f"{arg}: refused, current label is {verdict(label['passed'])}, not the one jev-review.md showed"
    label["passed"] = bool(regraded[i]["passed"])
    label["evidence"] = f"Corrected {today}, was {verdict(not label['passed'])}. {regraded[i]['evidence']}"
    if "summary" in grading:
        s = grading["summary"]
        passed = sum(1 for e in grading[key] if e.get("passed"))
        total = len(grading[key])
        s.update(passed=passed, failed=total - passed, total=total)
        s["pass_rate"] = pass_rate_like(s.get("pass_rate"), passed, total)
    if "passed" in grading and key == "assertions":
        grading["passed"] = all(e.get("passed") for e in grading[key])
    indent = len(re.match(r"\s*", raw.split("\n")[1]).group()) if "\n" in raw else 2
    text = json.dumps(grading, indent=indent, ensure_ascii=raw.isascii())
    with open(path + ".tmp", "w", encoding="utf-8") as f:
        f.write(text + ("\n" if raw.endswith("\n") else ""))
    os.rename(path + ".tmp", path)
    return True, f"{arg}: {verdict(not label['passed'])} -> {verdict(label['passed'])}"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--runs", required=True, help="eval-runs directory")
    parser.add_argument("targets", nargs="+", metavar="CASE:INDEX", help="approved conflicts, e.g. valcraft-spec/eval-18/with_skill:4")
    args = parser.parse_args()
    runs = os.path.abspath(args.runs)
    today = datetime.date.today().isoformat()
    skills, refused = set(), 0
    for arg in args.targets:
        applied, line = apply(runs, arg, today)
        print(line)
        refused += not applied
        if applied:
            skills.add(arg.split("/")[0])
    stale = [
        p
        for s in sorted(skills)
        for pattern in ("summary.json", "aggregate.json", "SUMMARY.md")
        for p in glob.glob(f"{runs}/{s}/{pattern}")
    ]
    if stale:
        print("stale, reconcile from disk:")
        print("\n".join(f"  {os.path.relpath(p, runs)}" for p in stale))
    return 1 if refused else 0


if __name__ == "__main__":
    sys.exit(main())
