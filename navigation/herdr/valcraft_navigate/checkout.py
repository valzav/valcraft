"""Checkout discovery (contract: Checkout)."""

from __future__ import annotations

import os
import stat
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


def _on_disk_name(directory: Path, name: str) -> str | None:
    """The entry's real spelling in directory, or None when it is missing, a symlink, or ambiguous.

    A case-insensitive or normalization-insensitive filesystem opens
    .valcraft/CONFIG.LOCAL.YAML for .valcraft/config.local.yaml, but git
    records the spelling it checked out, so tracked checks must use that.
    """
    try:
        wanted = os.lstat(directory / name)
        entries = os.listdir(directory)
    except OSError:
        return None
    if stat.S_ISLNK(wanted.st_mode):
        return None
    matches = []
    for entry in entries:
        try:
            found = os.lstat(directory / entry)
        except OSError:
            continue
        if (found.st_dev, found.st_ino) == (wanted.st_dev, wanted.st_ino):
            matches.append(entry)
    return matches[0] if len(matches) == 1 else None


def is_user_local(root: Path, relative: str) -> bool:
    """True when the file is absent, or a regular file that git ignores and does not track.

    The editor record names a program to launch, so it must come from the user,
    never from repository content a clone can deliver. A symlink anywhere on
    the path is refused.
    """
    if not os.path.lexists(root / relative):
        return True
    directory, spelled = root, []
    for part in relative.split("/"):
        name = _on_disk_name(directory, part)
        if name is None:
            return False
        spelled.append(name)
        directory = directory / name
    if not stat.S_ISREG(os.lstat(directory).st_mode):
        return False
    real = "/".join(spelled)
    if _git(root, "ls-files", "--error-unmatch", "--", real) is not None:
        return False
    return _git(root, "check-ignore", "--quiet", "--", real) is not None
