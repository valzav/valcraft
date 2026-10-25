"""Command line: python3 -m valcraft_navigate resolve --base DIR REFERENCE.

Prints one JSON object: a target, an ambiguous candidate list, or a failure.
"""

from __future__ import annotations

import argparse
import dataclasses
import json
import sys
from pathlib import Path
from typing import List, Optional

from .resolve import Ambiguous, Failure, Result, Target, resolve


def to_json(result: Result) -> dict:
    if isinstance(result, Target):
        return {"result": "target", **dataclasses.asdict(result)}
    if isinstance(result, Ambiguous):
        return {
            "result": "ambiguous",
            "candidates": [
                dataclasses.asdict(candidate) for candidate in result.candidates
            ],
        }
    assert isinstance(result, Failure)
    return {"result": "failure", "failure": result.failure}


def main(argv: Optional[List[str]] = None) -> int:
    parser = argparse.ArgumentParser(prog="valcraft_navigate")
    commands = parser.add_subparsers(dest="command", required=True)
    resolve_command = commands.add_parser("resolve", help="resolve one reference")
    resolve_command.add_argument(
        "--base",
        required=True,
        type=Path,
        help="the directory the reference was shown in",
    )
    resolve_command.add_argument("reference")
    arguments = parser.parse_args(argv)
    json.dump(
        to_json(resolve(arguments.base, arguments.reference)),
        sys.stdout,
        ensure_ascii=False,
    )
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
