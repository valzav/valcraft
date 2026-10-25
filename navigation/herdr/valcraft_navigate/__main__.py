"""Command line for the Herdr plugin and for direct resolution.

- resolve --base DIR REFERENCE: print one JSON result.
- open-selection, pick, open-link, picker: the Herdr entry points, which read
  their input from the environment Herdr provides.
"""

from __future__ import annotations

import argparse
import dataclasses
import json
import os
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
    for name in ("open-selection", "pick", "open-link", "picker"):
        commands.add_parser(name, help=f"Herdr entry point: {name}")
    arguments = parser.parse_args(argv)
    if arguments.command == "resolve":
        json.dump(
            to_json(resolve(arguments.base, arguments.reference)),
            sys.stdout,
            ensure_ascii=False,
        )
        sys.stdout.write("\n")
        return 0
    from . import actions, picker  # curses loads only for the Herdr entry points

    environ = dict(os.environ)
    entry_points = {
        "open-selection": actions.open_selection,
        "pick": actions.pick,
        "open-link": actions.open_link,
        "picker": picker.main,
    }
    entry_points[arguments.command](environ)
    return 0  # failures reach the user as Herdr notifications


if __name__ == "__main__":
    sys.exit(main())
