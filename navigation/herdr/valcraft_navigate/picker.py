"""The picker that runs in the Herdr popup pane.

Menu holds the list logic; run_menu draws it with curses.
"""

from __future__ import annotations

import curses
import json
import os
from dataclasses import dataclass
from typing import Dict, List, Optional, Union

from . import actions, herdr
from .recognize import Identity, recognize
from .resolve import Ambiguous, Candidate, Target, resolve
from .scan import scan

_UP = {curses.KEY_UP, ord("k")}
_DOWN = {curses.KEY_DOWN, ord("j")}
_CHOOSE = {curses.KEY_ENTER, 10, 13}
_CANCEL = {27, ord("q")}


@dataclass
class Menu:
    title: str
    labels: List[str]
    index: int = 0

    def handle(self, key: int) -> Union[None, int, bool]:
        """Return the chosen index, False when cancelled, or None to keep going."""
        if key in _UP:
            self.index = max(0, self.index - 1)
        elif key in _DOWN:
            self.index = min(len(self.labels) - 1, self.index + 1)
        elif key in _CHOOSE:
            return self.index
        elif key in _CANCEL:
            return False
        return None


def run_menu(menu: Menu) -> Optional[int]:
    os.environ.setdefault("ESCDELAY", "25")  # Escape should cancel at once

    def loop(screen) -> Optional[int]:
        curses.curs_set(0)
        while True:
            height, width = screen.getmaxyx()
            rows = max(1, height - 2)
            top = min(max(0, menu.index - rows + 1), max(0, len(menu.labels) - rows))
            screen.erase()
            screen.addnstr(0, 0, menu.title, width - 1, curses.A_BOLD)
            for row, label in enumerate(menu.labels[top : top + rows]):
                attribute = (
                    curses.A_REVERSE if top + row == menu.index else curses.A_NORMAL
                )
                screen.addnstr(row + 1, 0, label, width - 1, attribute)
            screen.addnstr(
                height - 1,
                0,
                "Enter open · Esc cancel · ↑/↓ or j/k move",
                width - 1,
                curses.A_DIM,
            )
            screen.refresh()
            outcome = menu.handle(screen.getch())
            if outcome is False:
                return None
            if outcome is not None:
                return outcome

    return curses.wrapper(loop)


def candidate_label(candidate: Candidate) -> str:
    return f"{candidate.identity}  {candidate.title} · {candidate.text}"


def reference_entries(session: actions.Session, text: str) -> List[str]:
    """References from pane output; file references only when they resolve."""
    entries = []
    for reference in scan(text):
        if isinstance(recognize(reference), Identity) or isinstance(resolve(session.base, reference), Target):
            entries.append(reference)
    return entries


def _choose_candidate(session: actions.Session, candidates: List[Candidate]) -> None:
    chosen = run_menu(
        Menu(
            "Several definitions match. Pick one:",
            [candidate_label(c) for c in candidates],
        )
    )
    if chosen is not None:
        candidate = candidates[chosen]
        actions.open_target(
            session, Target(candidate.path, candidate.line, candidate.column)
        )


def _load_candidates(environ: Dict[str, str], name: str) -> Optional[List[Candidate]]:
    directory = herdr.state_dir(environ)
    if directory is None or "/" in name or not name.startswith("candidates-"):
        return None
    path = directory / name
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
        return [Candidate(**item) for item in data]
    except (OSError, ValueError, TypeError):
        return None
    finally:
        path.unlink(missing_ok=True)


def main(environ: Dict[str, str]) -> None:
    invocation = herdr.invocation(environ)
    session = actions.enable(environ, invocation)
    if session is None:
        return
    candidates_name = environ.get(actions.CANDIDATES_ENV)
    if candidates_name:
        candidates = _load_candidates(environ, candidates_name)
        if candidates is None:
            herdr.notify(
                environ, "The picker's candidate list is missing or unreadable."
            )
            return
        _choose_candidate(session, candidates)
        return
    text = herdr.read_pane(environ, invocation.pane_id) if invocation.pane_id else None
    if text is None:
        herdr.notify(environ, "Could not read the pane's output.")
        return
    entries = reference_entries(session, text)
    if not entries:
        herdr.notify(
            environ,
            "No Valcraft identities or file references in this pane's recent output.",
        )
        return
    chosen = run_menu(Menu("Open in editor:", entries))
    if chosen is None:
        return
    reference = entries[chosen]
    result = resolve(session.base, reference)
    if isinstance(result, Ambiguous):
        _choose_candidate(session, list(result.candidates))
    else:
        actions.act_on(session, result, reference)
