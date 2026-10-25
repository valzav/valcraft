"""Reads the editor record and valcraft_version from Valcraft configuration.

Standard-library Python has no YAML parser, so this reads only the exact
shapes Valcraft Tune writes and treats anything else as unreadable.
"""

from __future__ import annotations

import os
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Optional, Tuple

_KEY_VALUE = re.compile(r"(?P<key>[a-z_]+):(?: (?P<value>.*))?")
# YAML plain scalars cannot start with these; quoted scalars hold only the
# escapes a path needs, so a value this reader cannot interpret is refused.
_INDICATORS = "-?:,[]{}#&*!|>'\"%@`"
_SINGLE = re.compile(r"'((?:[^']|'')*)'")
_DOUBLE = re.compile(r'"((?:[^"\\\x00-\x1f]|\\["\\/])*)"')
_VERSION = re.compile(
    r"(?P<major>0|[1-9][0-9]*)\.(?P<minor>0|[1-9][0-9]*)\.(?P<patch>0|[1-9][0-9]*)"
)


class Unreadable(Exception):
    """The file exists but does not hold the shape this module reads."""


@dataclass(frozen=True)
class EditorRecord:
    adapter: str
    executable: str


def _scalar(raw: str) -> str:
    """One YAML scalar: plain, single-quoted, or double-quoted.

    A plain scalar may contain spaces, as in
    /Applications/Visual Studio Code.app/Contents/Resources/app/bin/code.
    Anything this reader cannot interpret exactly is Unreadable.
    """
    raw = raw.strip()
    if raw.startswith("'"):
        match = _SINGLE.fullmatch(raw)
        if not match:
            raise Unreadable(f"unsupported single-quoted value: {raw!r}")
        return match.group(1).replace("''", "'")
    if raw.startswith('"'):
        match = _DOUBLE.fullmatch(raw)
        if not match:
            raise Unreadable(f"unsupported double-quoted value: {raw!r}")
        return re.sub(r'\\(["\\/])', r"\1", match.group(1))
    if not raw or raw[0] in _INDICATORS or ": " in raw or " #" in raw or any(c < " " for c in raw):
        raise Unreadable(f"unsupported plain value: {raw!r}")
    return raw


def _top_level(lines: List[str]) -> Dict[str, Tuple[Optional[str], List[str]]]:
    """Map each top-level key to its inline value and its indented child lines."""
    blocks: Dict[str, Tuple[Optional[str], List[str]]] = {}
    current: Optional[str] = None
    for line in lines:
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        if line[0] == " ":
            if current is None:
                raise Unreadable("indented line before any key")
            blocks[current][1].append(line)
            continue
        match = _KEY_VALUE.fullmatch(line.rstrip())
        if not match:
            raise Unreadable(f"unsupported line: {line!r}")
        current = str(match["key"])
        if current in blocks:
            raise Unreadable(f"duplicate key {current}")
        blocks[current] = (match["value"], [])
    return blocks


def _read(path: Path) -> Optional[List[str]]:
    try:
        return path.read_text(encoding="utf-8").splitlines()
    except FileNotFoundError:
        return None
    except (OSError, UnicodeDecodeError) as error:
        raise Unreadable(str(error)) from error


def read_editor_record(primary: Path) -> Optional[EditorRecord]:
    """The overlay's editor record, or None when the overlay or the record is absent."""
    lines = _read(primary / ".valcraft" / "config.local.yaml")
    if lines is None:
        return None
    block = _top_level(lines).get("editor")
    if block is None:
        return None
    inline, children = block
    if inline is not None and inline.strip():
        raise Unreadable("editor must be a block mapping")
    fields: Dict[str, str] = {}
    for child in children:
        match = (
            _KEY_VALUE.fullmatch(child.rstrip()[2:])
            if child.startswith("  ") and child[2] != " "
            else None
        )
        if not match or match["value"] is None or match["key"] in fields:
            raise Unreadable(f"unsupported editor line: {child!r}")
        fields[match["key"]] = _scalar(match["value"])
    if set(fields) != {"adapter", "executable"}:
        raise Unreadable("editor needs exactly adapter and executable")
    return EditorRecord(fields["adapter"], fields["executable"])


def read_valcraft_version(checkout: Path) -> Optional[Tuple[int, int, int]]:
    """The base's valcraft_version, or None when it is absent or unreadable."""
    try:
        lines = _read(checkout / ".valcraft" / "config.yaml")
        block = _top_level(lines or []).get("valcraft_version")
        if block is None or block[0] is None:
            return None
        match = _VERSION.fullmatch(_scalar(block[0]))
    except Unreadable:
        return None
    return (
        (int(match["major"]), int(match["minor"]), int(match["patch"]))
        if match
        else None
    )


def parse_version(text: str) -> Tuple[int, int, int]:
    match = _VERSION.fullmatch(text)
    if not match:
        raise ValueError(text)
    return (int(match["major"]), int(match["minor"]), int(match["patch"]))


def executable_problem(record: EditorRecord) -> Optional[str]:
    """Why the recorded executable cannot be launched, or None when it can."""
    if not os.path.isabs(record.executable):
        return "the recorded editor executable is not an absolute path"
    resolved = os.path.realpath(record.executable)
    if not os.path.isfile(resolved) or not os.access(resolved, os.X_OK):
        return f"the recorded editor executable {record.executable} is missing or not executable"
    return None
