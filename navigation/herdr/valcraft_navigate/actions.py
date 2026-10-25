"""The plugin's entry points: open-selection, pick, open-link, and the picker pane."""

from __future__ import annotations

import json
import uuid
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Dict, List, Optional

from . import checkout, config, editors, herdr, links
from .resolve import (
    Ambiguous,
    Candidate,
    Failure,
    Result,
    Target,
    resolve,
    resolve_path,
)

# The Valcraft release this plugin belongs to. It equals the manifest version.
PLUGIN_VERSION = "0.12.2"
CANDIDATES_ENV = "VALCRAFT_NAVIGATION_CANDIDATES"
TUNE_SECTION = "Valcraft Tune's Editor navigation section"


@dataclass(frozen=True)
class Session:
    environ: Dict[str, str]
    base: Path
    record: config.EditorRecord


def enable(environ: Dict[str, str], invocation: herdr.Invocation) -> Optional[Session]:
    """Check that editor navigation is on for the invoking pane's repository."""
    base = invocation.pane_cwd
    if base is None or not base.is_dir():
        herdr.notify(environ, "Herdr did not report a working directory for this pane.")
        return None
    root = checkout.checkout_root(base)
    if root is None or not checkout.is_valcraft_project(root):
        herdr.notify(
            environ,
            f"{base} is not in a Valcraft project: no committed .valcraft/config.yaml in its checkout.",
        )
        return None
    primary = checkout.primary_checkout(base) or root
    overlay = ".valcraft/config.local.yaml"
    if not checkout.is_user_local(primary, overlay):
        herdr.notify(
            environ,
            f"Refusing {primary}/{overlay}: it must be an ignored, untracked regular file, because it names a program to run.",
        )
        return None
    try:
        record = config.read_editor_record(primary)
    except config.Unreadable as error:
        herdr.notify(
            environ,
            f"Cannot read the editor record in {primary}/.valcraft/config.local.yaml ({error}). Repair it in {TUNE_SECTION}.",
        )
        return None
    if record is None:
        herdr.notify(
            environ,
            f"Editor navigation is off in {primary}. Turn it on in {TUNE_SECTION}.",
        )
        return None
    if record.adapter not in editors.ADAPTERS:
        herdr.notify(
            environ,
            f"Unknown editor adapter {record.adapter!r}. Repair it in {TUNE_SECTION}.",
        )
        return None
    problem = config.executable_problem(record)
    if problem:
        herdr.notify(
            environ, f"{problem[0].upper()}{problem[1:]}. Repair it in {TUNE_SECTION}."
        )
        return None
    repository_version = config.read_valcraft_version(root)
    if repository_version and repository_version > config.parse_version(PLUGIN_VERSION):
        herdr.notify(
            environ,
            f"This repository uses Valcraft {'.'.join(map(str, repository_version))}, newer than this plugin's"
            f" release {PLUGIN_VERSION}. Update the plugin in {TUNE_SECTION}.",
        )
    return Session(environ, base, record)


def open_target(session: Session, target: Target) -> None:
    try:
        editors.launch(session.record.adapter, session.record.executable, target)
    except OSError as error:
        herdr.notify(
            session.environ,
            f"Could not start {session.record.executable}: {error.strerror or error}. Repair it in {TUNE_SECTION}.",
        )


_FAILURES = {
    "unrecognized": "{reference!r} is not a Valcraft identity or a file reference.",
    "malformed_identity": "{reference!r} looks like a Valcraft identity but is malformed.",
    "not_valcraft_checkout": "{reference!r} needs a Valcraft project checkout.",
    "unknown_qualifier": "{reference!r}: no such feature or quick file in this checkout.",
    "not_found": "{reference!r}: no definition or file found.",
    "not_regular_file": "{reference!r} is not a regular file.",
}


def report_failure(environ: Dict[str, str], failure: Failure, reference: str) -> None:
    herdr.notify(environ, _FAILURES[failure.failure].format(reference=reference))


def _open_candidates_picker(session: Session, candidates: List[Candidate]) -> None:
    directory = herdr.state_dir(session.environ)
    if directory is None:
        herdr.notify(
            session.environ,
            "Herdr did not provide a plugin state directory for the picker.",
        )
        return
    directory.mkdir(parents=True, exist_ok=True)
    name = f"candidates-{uuid.uuid4().hex}.json"
    (directory / name).write_text(
        json.dumps([asdict(candidate) for candidate in candidates]), encoding="utf-8"
    )
    if not herdr.open_picker(session.environ, {CANDIDATES_ENV: name}):
        (directory / name).unlink(missing_ok=True)
        herdr.notify(session.environ, "Could not open the picker popup.")


def act_on(session: Session, result: Result, reference: str) -> None:
    if isinstance(result, Target):
        open_target(session, result)
    elif isinstance(result, Ambiguous):
        _open_candidates_picker(session, list(result.candidates))
    else:
        report_failure(session.environ, result, reference)


def open_selection(environ: Dict[str, str]) -> None:
    invocation = herdr.invocation(environ)
    session = enable(environ, invocation)
    if session is None:
        return
    if not invocation.selected_text:
        herdr.notify(
            environ,
            "No text is selected. Select a reference in copy mode, or use the pane picker"
            f" ({herdr.PLUGIN_ID}.pick) to choose from the pane's output.",
        )
        return
    act_on(
        session,
        resolve(session.base, invocation.selected_text),
        invocation.selected_text,
    )


def pick(environ: Dict[str, str]) -> None:
    session = enable(environ, herdr.invocation(environ))
    if session is not None and not herdr.open_picker(environ, {}):
        herdr.notify(environ, "Could not open the picker popup.")


def open_link(environ: Dict[str, str]) -> None:
    invocation = herdr.invocation(environ)
    url = invocation.clicked_url or ""
    session = enable(environ, invocation)
    if session is None:
        return
    target = links.parse(url)
    if target is None:
        herdr.notify(environ, f"Cannot open {url!r}: not a supported file link.")
        return
    act_on(
        session,
        resolve_path(session.base, target.path, target.line, target.column),
        url,
    )
