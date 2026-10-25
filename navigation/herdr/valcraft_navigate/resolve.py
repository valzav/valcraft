"""Resolution of identities and file references (contract: Artifacts, Resolution)."""

from __future__ import annotations

import os
import re
from collections.abc import Iterator
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Union

from . import checkout
from .recognize import FileReference, Identity, Unrecognized, recognize

_NAME = re.compile(r"(?P<number>[0-9]{3,})-[a-z0-9]+(?:-[a-z0-9]+)*")
_FEATURE_TASK = re.compile(
    r"- (?:\[[ xX]\] (?P<checked>T-[0-9]{3,})(?= |$)"
    r"|(?P<mapped>T-[0-9]{3,}) .*→ (?:TBD|#[1-9][0-9]*)\s*$)"
)
_QUICK_TASK = re.compile(r"- \[[ xX]\] (?P<quick>QT-[0-9]{3,})(?= |$)")
_FENCE_OPEN = re.compile(r" {0,3}(?P<fence>`{3,}|~{3,})")


@dataclass(frozen=True)
class Target:
    path: str
    line: int
    column: int


@dataclass(frozen=True)
class Candidate:
    path: str
    line: int
    column: int
    identity: str
    title: str
    text: str


@dataclass(frozen=True)
class Ambiguous:
    candidates: Tuple[Candidate, ...]


@dataclass(frozen=True)
class Failure:
    failure: str


Result = Union[Target, Ambiguous, Failure]


@dataclass(frozen=True)
class _Artifact:
    qualifier: str  # FEAT-NNN or Q-NNN
    entry: Path  # spec.md for a feature, the quick file itself
    tasks: Optional[Path]  # where task definitions live, if anywhere
    title: str


def _read_lines(path: Path) -> List[str]:
    try:
        return path.read_text(encoding="utf-8").splitlines()
    except (OSError, UnicodeDecodeError):
        return []


def _frontmatter(lines: List[str]) -> Dict[str, List[str]]:
    if not lines or lines[0] != "---":
        return {}
    fields: Dict[str, List[str]] = {}
    for line in lines[1:]:
        if line == "---":
            return fields
        key, separator, value = line.partition(": ")
        if separator and key and not key[0].isspace():
            fields.setdefault(key, []).append(value.strip())
    return {}  # an unclosed block is not frontmatter


def _definition_lines(lines: List[str]) -> Iterator[Tuple[int, str]]:
    """Yield (1-based number, line) for each line outside comments and fenced blocks."""
    in_comment = False
    closing: Optional[re.Pattern] = None
    for number, line in enumerate(lines, start=1):
        if closing is not None:
            if closing.fullmatch(line):
                closing = None
            continue
        if not in_comment:
            opening = _FENCE_OPEN.match(line)
            if opening:
                fence = opening["fence"]
                closing = re.compile(
                    rf" {{0,3}}{re.escape(fence[0])}{{{len(fence)},}}\s*"
                )
                continue
            yield number, line
        in_comment = _comment_open_after(line, in_comment)


def _comment_open_after(line: str, in_comment: bool) -> bool:
    position = 0
    while True:
        marker = "-->" if in_comment else "<!--"
        found = line.find(marker, position)
        if found < 0:
            return in_comment
        position = found + len(marker)
        in_comment = not in_comment


def _definitions(
    lines: List[str], pattern: re.Pattern
) -> Iterator[Tuple[int, str, str]]:
    """Yield (line number, task identity, task text) for each defining entry."""
    for number, line in _definition_lines(lines):
        match = pattern.match(line)
        if match and match.lastgroup is not None:
            yield number, match[match.lastgroup], line[
                match.end(match.lastgroup) :
            ].strip()


def _number(name: str) -> Optional[str]:
    match = _NAME.fullmatch(name)
    return match["number"] if match else None


def _single(fields: Dict[str, List[str]], key: str, value: str) -> bool:
    return fields.get(key) == [value]


def _keep_unique(
    candidates: List[Tuple[Optional[str], Optional[_Artifact]]],
) -> Dict[str, _Artifact]:
    """Keep valid artifacts whose number no other candidate claims, valid or not."""
    claims: Dict[str, int] = {}
    for number, _ in candidates:
        if number is not None:
            claims[number] = claims.get(number, 0) + 1
    return {
        number: artifact
        for number, artifact in candidates
        if number is not None and artifact is not None and claims[number] == 1
    }


def _feature(directory: Path, number: Optional[str]) -> Optional[_Artifact]:
    spec = directory / "spec.md"
    if number is None or not spec.is_file():
        return None
    fields = _frontmatter(_read_lines(spec))
    if not _single(fields, "id", f"FEAT-{number}"):
        return None
    tasks = directory / "tasks.md"
    if tasks.exists():
        if not tasks.is_file() or not _single(
            _frontmatter(_read_lines(tasks)), "feature", f"FEAT-{number}"
        ):
            return None
    title = fields["title"][0] if len(fields.get("title", [])) == 1 else ""
    return _Artifact(f"FEAT-{number}", spec, tasks if tasks.is_file() else None, title)


def _features(root: Path) -> Dict[str, _Artifact]:
    specs = root / "specs"
    if not specs.is_dir():
        return {}
    candidates = []
    for directory in sorted(specs.iterdir()):
        if directory.is_dir() and directory.name[:1].isdigit():
            number = _number(directory.name)
            candidates.append((number, _feature(directory, number)))
    return _keep_unique(candidates)


def _quick_file(path: Path, number: Optional[str]) -> Optional[_Artifact]:
    lines = _read_lines(path)
    if number is None or not _single(_frontmatter(lines), "id", f"Q-{number}"):
        return None
    if any(True for _ in _definitions(lines, _FEATURE_TASK)):
        return None
    title = next((line[2:].strip() for line in lines if line.startswith("# ")), "")
    return _Artifact(f"Q-{number}", path, path, title)


def _quick_files(root: Path) -> Dict[str, _Artifact]:
    quick = root / "specs" / "quick"
    if not quick.is_dir():
        return {}
    candidates = []
    for path in sorted(quick.iterdir()):
        if path.is_file() and path.name.endswith(".md"):
            number = _number(path.name[: -len(".md")])
            candidates.append((number, _quick_file(path, number)))
    return _keep_unique(candidates)


def _gather(
    artifacts: List[_Artifact], task: str, pattern: re.Pattern, root: Path
) -> Result:
    candidates = []
    for artifact in artifacts:
        if artifact.tasks is None:
            continue
        for number, defined, text in _definitions(_read_lines(artifact.tasks), pattern):
            if defined == task:
                candidates.append(
                    Candidate(
                        str(artifact.tasks),
                        number,
                        1,
                        f"{artifact.qualifier}/{defined}",
                        artifact.title,
                        text,
                    )
                )
    if not candidates:
        return Failure("not_found")
    if len(candidates) == 1:
        return Target(candidates[0].path, candidates[0].line, 1)
    candidates.sort(
        key=lambda candidate: (
            Path(candidate.path).relative_to(root).as_posix(),
            candidate.line,
        )
    )
    return Ambiguous(tuple(candidates))


def _resolve_identity(base: Path, identity: Identity) -> Result:
    root = checkout.checkout_root(base)
    if root is None or not checkout.is_valcraft_project(root):
        return Failure("not_valcraft_checkout")
    feature_side = identity.form in ("feature", "feature_task", "task")
    artifacts = _features(root) if feature_side else _quick_files(root)
    qualifier = identity.feature if feature_side else identity.quick
    if identity.form in ("task", "quick_bare_task"):
        selected = [artifacts[number] for number in sorted(artifacts)]
    elif qualifier not in artifacts:
        return Failure("unknown_qualifier")
    elif identity.form in ("feature", "quick"):
        return Target(str(artifacts[qualifier].entry), 1, 1)
    else:
        selected = [artifacts[qualifier]]
    prefix, pattern = ("T", _FEATURE_TASK) if feature_side else ("QT", _QUICK_TASK)
    return _gather(selected, f"{prefix}-{identity.task}", pattern, root)


def _resolve_file(base: Path, reference: FileReference) -> Result:
    if reference.path.startswith("~/"):
        path = Path.home() / reference.path[2:]
    else:
        path = base / reference.path  # an absolute path replaces base
    resolved = Path(os.path.realpath(path))
    if not resolved.exists():
        return Failure("not_found")
    if not resolved.is_file():
        return Failure("not_regular_file")
    return Target(str(resolved), reference.line, reference.column)


def resolve(base: Path, reference: str) -> Result:
    recognized = recognize(reference)
    if isinstance(recognized, Unrecognized):
        return Failure(recognized.failure)
    if isinstance(recognized, Identity):
        return _resolve_identity(base, recognized)
    return _resolve_file(base, recognized)
