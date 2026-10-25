"""The Herdr surfaces the plugin uses: invocation context, notifications, panes."""

from __future__ import annotations

import json
import os
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Optional

PLUGIN_ID = "valcraft-navigation"
PICKER_ENTRYPOINT = "picker"
NOTIFICATION_TITLE = "Valcraft navigation"


@dataclass(frozen=True)
class Invocation:
    pane_id: Optional[str]
    pane_cwd: Optional[Path]
    selected_text: Optional[str]
    clicked_url: Optional[str]


def invocation(environ: Dict[str, str]) -> Invocation:
    try:
        context = json.loads(environ.get("HERDR_PLUGIN_CONTEXT_JSON", "{}"))
    except json.JSONDecodeError:
        context = {}
    if not isinstance(context, dict):
        context = {}
    cwd = context.get("focused_pane_cwd")
    return Invocation(
        pane_id=context.get("focused_pane_id") or None,
        pane_cwd=Path(cwd) if isinstance(cwd, str) and cwd else None,
        selected_text=context.get("selected_text") or None,
        clicked_url=environ.get("HERDR_PLUGIN_CLICKED_URL")
        or context.get("clicked_url")
        or None,
    )


def _herdr(environ: Dict[str, str]) -> str:
    return environ.get("HERDR_BIN_PATH") or "herdr"


def _run(environ: Dict[str, str], arguments: List[str]) -> subprocess.CompletedProcess:
    return subprocess.run(
        [_herdr(environ), *arguments],
        capture_output=True,
        text=True,
        stdin=subprocess.DEVNULL,
        env=environ,
    )


def notify(environ: Dict[str, str], message: str) -> None:
    """Show a Herdr notification; also log it, since a notification can fail too."""
    print(f"{NOTIFICATION_TITLE}: {message}", file=sys.stderr)
    try:
        _run(environ, ["notification", "show", NOTIFICATION_TITLE, "--body", message])
    except OSError as error:
        print(f"notification failed: {error}", file=sys.stderr)


def read_pane(environ: Dict[str, str], pane_id: str) -> Optional[str]:
    try:
        completed = _run(
            environ, ["pane", "read", pane_id, "--source", "recent-unwrapped"]
        )
    except OSError:
        return None
    return completed.stdout if completed.returncode == 0 else None


def open_picker(environ: Dict[str, str], extra_env: Dict[str, str]) -> bool:
    arguments = [
        "plugin",
        "pane",
        "open",
        "--plugin",
        PLUGIN_ID,
        "--entrypoint",
        PICKER_ENTRYPOINT,
        "--focus",
    ]
    for key, value in extra_env.items():
        arguments += ["--env", f"{key}={value}"]
    try:
        completed = _run(environ, arguments)
    except OSError:
        return False
    if completed.returncode != 0:
        print(completed.stderr, file=sys.stderr)
    return completed.returncode == 0


def state_dir(environ: Dict[str, str]) -> Optional[Path]:
    value = environ.get("HERDR_PLUGIN_STATE_DIR")
    return Path(value) if value and os.path.isabs(value) else None
