"""References in terminal output (contract: Recognition, References in terminal output)."""

from __future__ import annotations

import re
from typing import Dict, List, Tuple

_NUM = "[0-9]{3,}"
# Longest forms first, so FEAT-001/T-002 is one reference.
_IDENTITY = re.compile(
    rf"(?<![A-Za-z0-9/-])"
    rf"(?:FEAT-{_NUM}/T-{_NUM}|FEAT-{_NUM}|Q-{_NUM}[/ ]QT-{_NUM}|Q-{_NUM}|QT-{_NUM}|T-{_NUM})"
    rf"(?![A-Za-z0-9/-])"
)
_PATH_TOKEN = re.compile(
    r"(?<![A-Za-z0-9_.+@/:~-])(?:~/)?[A-Za-z0-9_.+@/-]+(?::[0-9]+)*"
)
_SUFFIX = re.compile(r"(?P<path>.*?)(?P<suffix>(?::[1-9][0-9]*){0,2})")


def _is_path_like(path: str) -> bool:
    if "/" in path:
        return True
    return "." in path[1:-1]


def _paths(line: str, taken: List[Tuple[int, int]]) -> List[Tuple[int, str]]:
    found = []
    for match in _PATH_TOKEN.finditer(line):
        start, end = match.span()
        if any(
            start < taken_end and taken_start < end for taken_start, taken_end in taken
        ):
            continue
        token = match.group(0).rstrip(
            "."
        )  # a sentence-ending period is not part of the path
        parts = _SUFFIX.fullmatch(token)
        if parts and ":" not in parts["path"] and _is_path_like(parts["path"]):
            found.append((start, token))
    return found


def scan(text: str) -> List[str]:
    """Return the distinct references in text, ordered by most recent occurrence first."""
    occurrences: List[Tuple[int, int, str]] = []
    for line_number, line in enumerate(text.splitlines()):
        identities = list(_IDENTITY.finditer(line))
        occurrences.extend(
            (line_number, match.start(), match.group(0)) for match in identities
        )
        taken = [match.span() for match in identities]
        occurrences.extend(
            (line_number, column, token) for column, token in _paths(line, taken)
        )
    last: Dict[str, Tuple[int, int]] = {}
    for line_number, column, reference in occurrences:
        last[reference] = max(
            last.get(reference, (line_number, column)), (line_number, column)
        )
    return sorted(last, key=lambda reference: last[reference], reverse=True)
