#!/usr/bin/env python3
"""Join the flagged set, each regrade.json, and each grading.json; write jev-review.md.

Usage: jev-review.py --runs <dir>

Offline. Reads <dir>/_harness/jev-flagged.json. Three sections. Conflicts: the re-grader's
verdict differs from the label. Confirmed: the re-grader agrees with the label, so the flag was
a Jev error. Assertion problems: every non-empty assertion_problem, as input for evals.json
fixes. Nothing here changes a label; the operator decides each conflict (docs/evals.md).
"""

from __future__ import annotations

import argparse
import json
import os


def expectations(grading: dict) -> list:
    return grading.get("expectations") or grading.get("assertions") or []


def verdict(passed) -> str:
    return "pass" if passed else "fail"


def review(runs: str, flagged: dict) -> dict:
    conflicts, confirmed, problems, pending, unusable = [], [], [], [], []
    for case, items in flagged.items():
        regrade_path = f"{runs}/{case}/regrade.json"
        if not os.path.isfile(regrade_path):
            pending.append(case)
            continue
        labelled = expectations(json.load(open(f"{runs}/{case}/grading.json")))
        regraded = {r["index"]: r for r in json.load(open(regrade_path))["regraded"]}
        for item in items:
            i = item["index"]
            r = regraded.get(i)
            if r is None:
                unusable.append(f"{case} a{i}: not in regrade.json")
                continue
            if r["text"] != item["text"] or labelled[i]["text"] != item["text"]:
                unusable.append(f"{case} a{i}: assertion text differs between flagged, regrade, and grading")
                continue
            entry = {"case": case, "index": i, "text": item["text"], "label": labelled[i], "regrade": r}
            (conflicts if bool(r["passed"]) != bool(labelled[i]["passed"]) else confirmed).append(entry)
            if r.get("assertion_problem"):
                problems.append(entry)
    return {
        "conflicts": conflicts,
        "confirmed": confirmed,
        "problems": problems,
        "pending": pending,
        "unusable": unusable,
    }


def render(flagged: dict, r: dict) -> str:
    summary = (
        f"Flagged: {sum(map(len, flagged.values()))} assertions in {len(flagged)} cases. "
        f"Re-graded: {len(flagged) - len(r['pending'])} cases. Conflicts: {len(r['conflicts'])}. "
        f"Confirmed: {len(r['confirmed'])}. Assertion problems: {len(r['problems'])}."
    )
    lines = ["# Jev audit review", "", summary, ""]
    if r["pending"]:
        lines += ["Cases with no regrade.json yet:", ""] + [f"- `{c}`" for c in r["pending"]] + [""]
    if r["unusable"]:
        lines += ["Unusable:", ""] + [f"- {u}" for u in r["unusable"]] + [""]
    lines += ["## Conflicts", "", "The operator decides each one from the run itself. Apply with `jev-apply.py <case>:<index>`.", ""]
    for e in r["conflicts"]:
        lines += [
            f"- `{e['case']}` a{e['index']}: label {verdict(e['label']['passed'])}, re-grade {verdict(e['regrade']['passed'])}",
            f"  - Assertion: {e['text']}",
            f"  - Label evidence: {e['label'].get('evidence', '')}",
            f"  - Re-grade evidence: {e['regrade'].get('evidence', '')}",
        ]
    lines += ["", "## Confirmed", "", "The re-grader agrees with the label. These flags were Jev errors and need no action.", ""]
    lines += [f"- `{e['case']}` a{e['index']}: {verdict(e['label']['passed'])}. {e['text']}" for e in r["confirmed"]]
    lines += ["", "## Assertion problems", "", "Input for `evals.json` fixes.", ""]
    for e in r["problems"]:
        lines += [f"- `{e['case']}` a{e['index']}: {e['text']}", f"  - {e['regrade']['assertion_problem']}"]
    return "\n".join(lines) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--runs", required=True, help="eval-runs directory")
    runs = os.path.abspath(parser.parse_args().runs)
    out = f"{runs}/_harness"
    flagged = json.load(open(f"{out}/jev-flagged.json"))
    text = render(flagged, review(runs, flagged))
    with open(f"{out}/jev-review.md.tmp", "w") as f:
        f.write(text)
    os.rename(f"{out}/jev-review.md.tmp", f"{out}/jev-review.md")
    print(text.split("\n")[2])
    return 0


if __name__ == "__main__":
    main()
