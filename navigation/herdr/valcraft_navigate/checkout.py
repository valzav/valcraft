"""Checkout discovery (contract: Checkout)."""

from __future__ import annotations

import os
import subprocess
from pathlib import Path

# Variables that would point git at some other repository than the base directory's.
_GIT_REDIRECTS = (
    "GIT_DIR",
    "GIT_WORK_TREE",
    "GIT_COMMON_DIR",
    "GIT_INDEX_FILE",
    "GIT_CEILING_DIRECTORIES",
)


def _git(base: Path, *args: str) -> str | None:
    env = {key: value for key, value in os.environ.items() if key not in _GIT_REDIRECTS}
    try:
        completed = subprocess.run(
            ["git", "-C", str(base), *args],
            capture_output=True,
            text=True,
            env=env,
            stdin=subprocess.DEVNULL,
        )
    except OSError:
        return None
    if completed.returncode != 0:
        return None
    return completed.stdout.strip()


def checkout_root(base: Path) -> Path | None:
    """The working tree that contains base, or None outside any working tree."""
    if not base.is_dir():
        return None
    top = _git(base, "rev-parse", "--show-toplevel")
    return Path(top) if top else None


def primary_checkout(base: Path) -> Path | None:
    """The working tree that owns the git common directory."""
    if not base.is_dir():
        return None
    common = _git(base, "rev-parse", "--path-format=absolute", "--git-common-dir")
    return Path(common).parent if common else None


def is_valcraft_project(root: Path) -> bool:
    config = root / ".valcraft" / "config.yaml"
    if config.is_symlink() or not config.is_file():
        return False
    return (
        _git(root, "ls-files", "--error-unmatch", "--", ".valcraft/config.yaml")
        is not None
    )
