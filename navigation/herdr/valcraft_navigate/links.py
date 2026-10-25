"""Strict parsing of clicked hyperlinks into a file path, line, and column.

The clicked URL comes from terminal output and is untrusted.
"""

from __future__ import annotations

import re
import socket
from dataclasses import dataclass
from typing import Optional
from urllib.parse import unquote, urlsplit

_POSITION = re.compile(
    r"(?P<path>.+?)(?::(?P<line>[1-9][0-9]*)(?::(?P<column>[1-9][0-9]*))?)?"
)
_FRAGMENT = re.compile(
    r"L(?P<line>[1-9][0-9]*)(?:C(?P<column>[1-9][0-9]*))?(?:-L[1-9][0-9]*(?:C[1-9][0-9]*)?)?"
)
EDITOR_SCHEMES = ("vscode", "cursor")


@dataclass(frozen=True)
class LinkTarget:
    path: str
    line: int
    column: int


def _clean_path(raw: str) -> Optional[str]:
    path = unquote(raw, errors="strict")
    if not path.startswith("/") or any(
        ord(character) < 32 or ord(character) == 127 for character in path
    ):
        return None
    return path


def parse(url: str) -> Optional[LinkTarget]:
    """Return the link's target, or None when the URL is not one this plugin accepts."""
    try:
        parts = urlsplit(url)
    except ValueError:
        return None
    if parts.query:
        return None
    if parts.scheme == "file":
        if parts.netloc not in ("", "localhost", socket.gethostname()):
            return None
        try:
            path = _clean_path(parts.path)
        except UnicodeDecodeError:
            return None
        if path is None:
            return None
        if not parts.fragment:
            return LinkTarget(path, 1, 1)
        fragment = _FRAGMENT.fullmatch(parts.fragment)
        if not fragment:
            return None
        return LinkTarget(path, int(fragment["line"]), int(fragment["column"] or 1))
    if parts.scheme in EDITOR_SCHEMES and parts.netloc == "file" and not parts.fragment:
        position = _POSITION.fullmatch(parts.path)
        if not position:
            return None
        try:
            path = _clean_path(position["path"])
        except UnicodeDecodeError:
            return None
        if path is None:
            return None
        return LinkTarget(
            path, int(position["line"] or 1), int(position["column"] or 1)
        )
    return None
