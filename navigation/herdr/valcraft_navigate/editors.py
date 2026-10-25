"""Editor adapters: map a target to one editor launcher's argument vector."""

from __future__ import annotations

import subprocess
from typing import Callable, Dict, List

from .resolve import Target


def _zed(executable: str, target: Target) -> List[str]:
    return [executable, f"{target.path}:{target.line}:{target.column}"]


def _vscode(executable: str, target: Target) -> List[str]:
    return [executable, "--goto", f"{target.path}:{target.line}:{target.column}"]


# Adding an editor means adding one entry here and its test.
ADAPTERS: Dict[str, Callable[[str, Target], List[str]]] = {
    "zed": _zed,
    "vscode": _vscode,
}


def launch(adapter: str, executable: str, target: Target) -> None:
    """Start the editor without a shell and without waiting for it.

    Raises KeyError for an unknown adapter and OSError when the executable cannot start.
    """
    argv = ADAPTERS[adapter](executable, target)
    subprocess.Popen(
        argv,
        stdin=subprocess.DEVNULL,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        start_new_session=True,
    )
