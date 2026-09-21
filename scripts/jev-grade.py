#!/usr/bin/env python3
"""Ask Jev one Noul per graded assertion; write jev-grading.json beside each grading.json.

Usage: jev-grade.py --runs <dir>                   grade every pending case under <dir>
       jev-grade.py --runs <dir> <case>...         grade only these case directories, if pending
       jev-grade.py --runs <dir> --dry-run <case>  print one case's request body, send nothing

A case directory is <dir>/<skill>/eval-<id>/<config>. Pending means it holds a grading.json
whose run_status is not "missing" and no jev-grading.json yet. The key comes from
OPENROUTER_API_KEY; nothing is read or written outside <dir>. See docs/evals.md.
"""

from __future__ import annotations

import argparse
import glob
import json
import os
import sys
import urllib.error
import urllib.request

URL = "https://openrouter.ai/api/v1/systemone"
MODEL = "typesafe/jev-1.13"  # pinned: the ~typesafe/jev-latest alias moves

# The grader's verdict rule, restated as the meaning of yes and no.
CRITERIA = {
    "true": "The transcript or outputs contain clear, citable evidence that the assertion holds, "
    "and that evidence reflects genuine task completion rather than surface compliance.",
    "false": "There is no evidence, the evidence is contradicted or superficial, "
    "or the assertion cannot be verified from the transcript and outputs.",
}


def expectations(grading: dict) -> list:
    return grading.get("expectations") or grading.get("assertions") or []


def outputs(case: str) -> dict:
    """Every UTF-8 text file under outputs/, except repository internals."""
    root, found = f"{case}/outputs", {}
    for path in sorted(glob.glob(f"{root}/**/*", recursive=True, include_hidden=True)):
        rel = os.path.relpath(path, root)
        if not os.path.isfile(path) or ".git" in rel.split(os.sep):
            continue
        try:
            found[rel] = open(path, encoding="utf-8").read()
        except UnicodeDecodeError:
            pass
    return found


def request_body(case: str) -> dict:
    grading = json.load(open(f"{case}/grading.json"))
    transcript = f"{case}/transcript.md"
    return {
        "model": MODEL,
        "state": {
            "transcript": open(transcript, encoding="utf-8").read() if os.path.isfile(transcript) else "",
            "outputs": outputs(case),
        },
        "questions": {
            f"a{i}": {"type": "noul", "instructions": e["text"], "criteria": CRITERIA}
            for i, e in enumerate(expectations(grading))
        },
    }


def pending(runs: str):
    for path in sorted(glob.glob(f"{runs}/*/eval-*/*/grading.json")):
        case = os.path.dirname(path)
        if os.path.isfile(f"{case}/jev-grading.json"):
            continue
        if json.load(open(path)).get("run_status") == "missing":
            continue
        yield case


def grade(case: str, key: str) -> str | None:
    sent = request_body(case)
    req = urllib.request.Request(
        URL,
        json.dumps(sent).encode(),
        {"Authorization": f"Bearer {key}", "Content-Type": "application/json"},
    )
    try:
        with urllib.request.urlopen(req) as resp:
            body = json.load(resp)
    except urllib.error.HTTPError as err:
        return f"HTTP {err.code}: {err.read().decode(errors='replace')}"
    except urllib.error.URLError as err:
        return f"connection failed: {err.reason}"
    if "answers" not in body:
        return f"no answers in response: {json.dumps(body)}"
    skill, eval_dir, config = case.split(os.sep)[-3:]
    result = {
        "skill": skill,
        "eval_id": int(eval_dir.removeprefix("eval-")),
        "config": config,
        "model": body.get("model"),
        "usage": body.get("usage"),
        "assertions": [q["instructions"] for q in sent["questions"].values()],
        "answers": body["answers"],
    }
    tmp = f"{case}/jev-grading.json.tmp"
    json.dump(result, open(tmp, "w"), indent=2)
    os.rename(tmp, f"{case}/jev-grading.json")
    return None


def case_path(runs: str, case: str) -> str:
    return os.path.abspath(case if os.path.isabs(case) else os.path.join(runs, case))


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--runs", required=True, help="eval-runs directory")
    parser.add_argument("--dry-run", metavar="CASE", help="print this case's request body and send nothing")
    parser.add_argument("cases", nargs="*", help="case directories to grade; default every pending case")
    args = parser.parse_args()
    runs = os.path.abspath(args.runs)
    if args.dry_run:
        print(json.dumps(request_body(case_path(runs, args.dry_run)), indent=2))
        return 0
    key = os.environ.get("OPENROUTER_API_KEY")
    if not key:
        print("OPENROUTER_API_KEY is not set", file=sys.stderr)
        return 1
    only = {case_path(runs, c) for c in args.cases}
    graded = failed = 0
    for case in pending(runs):
        if only and case not in only:
            continue
        error = grade(case, key)
        failed += bool(error)
        graded += not error
        print(f"{os.path.relpath(case, runs)}: {error or 'graded'}", flush=True)
    print(f"graded={graded} failed={failed}")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
