#!/usr/bin/env python3
"""Compare jev-grading.json with grading.json; write the calibration report and the flagged set.

Usage: jev-compare.py --runs <dir>

Offline. Writes <dir>/_harness/jev-calibration.md, jev-calibration.csv, and jev-flagged.json.
States counts and disagreements only: no verdict on Jev, no recommended threshold. The flagged
set is the input to the blind re-grade described in docs/evals.md.
"""

from __future__ import annotations

import argparse
import collections
import csv
import glob
import json
import os

# Selection band for the blind re-grade. 0.9 is the only band with measured yield: 4 label
# changes from 25 flagged on the first audit (docs/evals.md). Widening it needs the same
# measurement first.
FLAG_BAND = 0.9

HEAD = (
    "| assertions | agree | LLM pass, Jev yes | LLM pass, Jev no | LLM fail, Jev yes | LLM fail, Jev no |\n"
    "| --- | --- | --- | --- | --- | --- |"
)


def expectations(grading: dict) -> list:
    return grading.get("expectations") or grading.get("assertions") or []


def collect(runs: str) -> tuple[list, list, collections.Counter]:
    rows, unusable, counts = [], [], collections.Counter()
    for path in sorted(glob.glob(f"{runs}/*/eval-*/*/grading.json")):
        case = os.path.dirname(path)
        name = os.path.relpath(case, runs)
        skill, eval_dir, config = name.split(os.sep)
        grading = json.load(open(path))
        if grading.get("run_status") == "missing":
            counts["skipped: run missing"] += 1
            continue
        if not os.path.isfile(f"{case}/jev-grading.json"):
            counts["no jev-grading.json"] += 1
            continue
        jev = json.load(open(f"{case}/jev-grading.json"))
        labelled = expectations(grading)
        # The label belongs to the text Jev was asked; a difference means grading.json was rewritten since.
        if jev["assertions"] != [e["text"] for e in labelled]:
            unusable.append(f"{name}: assertion texts differ from jev-grading.json")
            continue
        counts["compared"] += 1
        tokens = (jev.get("usage") or {}).get("input_tokens")
        for i, e in enumerate(labelled):
            rows.append(
                {
                    "skill": skill,
                    "eval_id": eval_dir.removeprefix("eval-"),
                    "config": config,
                    "index": i,
                    "llm_passed": e["passed"],
                    "noul": jev["answers"][f"a{i}"]["noul"],
                    "input_tokens": tokens,
                    "evidence": e.get("evidence", ""),
                    "text": e["text"],
                }
            )
    return rows, unusable, counts


def table(subset: list) -> str:
    """Four cells, taking noul > 0.5 as yes: the decision boundary of a binary probability."""
    cell = collections.Counter((r["llm_passed"], r["noul"] > 0.5) for r in subset)
    agree = cell[True, True] + cell[False, False]
    return (
        f"| {len(subset)} | {agree} | {cell[True, True]} | {cell[True, False]} "
        f"| {cell[False, True]} | {cell[False, False]} |"
    )


def flagged_set(rows: list) -> dict:
    """Index and verbatim text only: no label, no noul, no evidence, so the re-grader stays blind.

    An assertion whose label an audit already corrected is not flagged again.
    """
    flagged = collections.defaultdict(list)
    for r in rows:
        if abs(r["noul"] - r["llm_passed"]) > FLAG_BAND and not r["evidence"].startswith("Corrected"):
            flagged[f"{r['skill']}/eval-{r['eval_id']}/{r['config']}"].append({"index": r["index"], "text": r["text"]})
    return dict(sorted(flagged.items()))


def report(rows: list, unusable: list, counts: collections.Counter) -> str:
    lines = [
        "# Jev calibration against existing gradings",
        "",
        "Jev yes means `noul > 0.5`. The LLM gradings are judgments, not ground truth.",
        "",
        "## Cases",
        "",
    ]
    lines += [f"- {k}: {v}" for k, v in sorted(counts.items())]
    lines += [f"- unusable: {len(unusable)}"] + [f"  - {u}" for u in unusable]
    lines += ["", "## All assertions", "", HEAD, table(rows), "", "## Per skill", ""]
    for skill in sorted({r["skill"] for r in rows}):
        lines += [f"### {skill}", "", HEAD, table([r for r in rows if r["skill"] == skill]), ""]
    disagreements = [r for r in rows if r["llm_passed"] != (r["noul"] > 0.5)]
    disagreements.sort(key=lambda r: abs(r["noul"] - r["llm_passed"]), reverse=True)
    lines += ["## Disagreements, strongest first", ""]
    for r in disagreements:
        lines += [
            f"- `{r['skill']}/eval-{r['eval_id']}/{r['config']}` a{r['index']}: "
            f"LLM {'pass' if r['llm_passed'] else 'fail'}, noul {r['noul']:.2f}, "
            f"{r['input_tokens']} input tokens",
            f"  - Assertion: {r['text']}",
            f"  - LLM evidence: {r['evidence']}",
        ]
    return "\n".join(lines) + "\n"


def write(path: str, text: str) -> None:
    with open(path + ".tmp", "w", newline="") as f:
        f.write(text)
    os.rename(path + ".tmp", path)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--runs", required=True, help="eval-runs directory")
    runs = os.path.abspath(parser.parse_args().runs)
    out = f"{runs}/_harness"
    os.makedirs(out, exist_ok=True)
    rows, unusable, counts = collect(runs)

    fields = list(rows[0]) if rows else ["skill"]
    with open(f"{out}/jev-calibration.csv.tmp", "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)
    os.rename(f"{out}/jev-calibration.csv.tmp", f"{out}/jev-calibration.csv")
    write(f"{out}/jev-calibration.md", report(rows, unusable, counts))
    flagged = flagged_set(rows)
    write(f"{out}/jev-flagged.json", json.dumps(flagged, indent=2) + "\n")

    disagreements = sum(1 for r in rows if r["llm_passed"] != (r["noul"] > 0.5))
    print(f"cases: {dict(counts)} unusable={len(unusable)}")
    print(f"assertions={len(rows)} disagreements={disagreements}")
    print(f"flagged={sum(map(len, flagged.values()))} in {len(flagged)} cases (band {FLAG_BAND})")
    return 0


if __name__ == "__main__":
    main()
