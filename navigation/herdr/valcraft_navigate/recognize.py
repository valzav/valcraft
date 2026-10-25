"""Reference recognition: trimming and form matching (contract: Recognition)."""

from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Union

# Characters a double-click or a copied citation can carry around a reference.
_ENCLOSING = "`'\"‘’“”()[]{}<>"
_TRAILING = ".,;:!?"

# [0-9], not \d: \d also matches non-ASCII digits.
_NUM = "[0-9]{3,}"
_IDENTITY_FORMS = (
    ("feature", re.compile(rf"FEAT-(?P<feature>{_NUM})")),
    ("feature_task", re.compile(rf"FEAT-(?P<feature>{_NUM})/T-(?P<task>{_NUM})")),
    ("quick", re.compile(rf"Q-(?P<quick>{_NUM})")),
    ("quick_task", re.compile(rf"Q-(?P<quick>{_NUM})[/ ]QT-(?P<task>{_NUM})")),
    ("task", re.compile(rf"T-(?P<task>{_NUM})")),
    ("quick_bare_task", re.compile(rf"QT-(?P<task>{_NUM})")),
)
_IDENTITY_PREFIXES = ("FEAT-", "Q-", "T-", "QT-")
_FILE_REFERENCE = re.compile(
    r"(?P<path>.+?)(?::(?P<line>[1-9][0-9]*)(?::(?P<column>[1-9][0-9]*))?)?"
)


@dataclass(frozen=True)
class Identity:
    form: str
    feature: str | None = None
    quick: str | None = None
    task: str | None = None


@dataclass(frozen=True)
class FileReference:
    path: str
    line: int = 1
    column: int = 1


@dataclass(frozen=True)
class Unrecognized:
    failure: str


Recognized = Union[Identity, FileReference, Unrecognized]


def trim(reference: str) -> str:
    previous = None
    while previous != reference:
        previous = reference
        reference = reference.strip().strip(_ENCLOSING)
        reference = reference.rstrip(_TRAILING)
    return reference


def recognize(reference: str) -> Recognized:
    text = trim(reference)
    if not text:
        return Unrecognized("unrecognized")
    for form, pattern in _IDENTITY_FORMS:
        match = pattern.fullmatch(text)
        if match:
            return Identity(form=form, **match.groupdict())
    if text.startswith(_IDENTITY_PREFIXES):
        return Unrecognized("malformed_identity")
    if any(character.isspace() for character in text):
        return Unrecognized("unrecognized")
    match = _FILE_REFERENCE.fullmatch(text)
    assert match is not None  # ".+?" matches any nonempty text
    return FileReference(
        path=match["path"],
        line=int(match["line"] or 1),
        column=int(match["column"] or 1),
    )
