#!/usr/bin/env python3
"""Keep the shipped migration ledger and the release manifests in step.

The newest `## vX.Y.Z` heading in valcraft-tune/references/migrations.md is the
plugin version Tune compares against `valcraft_version`, so it must equal the
version in the portable, Codex, and Cursor manifests, and every change under a
release must carry the three labels the migration procedure reads.
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PLUGIN = ROOT / "plugins" / "valcraft"
LEDGER = PLUGIN / "skills" / "valcraft-tune" / "references" / "migrations.md"
MANIFESTS = [
    PLUGIN / "plugin.json",
    PLUGIN / ".codex-plugin" / "plugin.json",
    PLUGIN / ".cursor-plugin" / "plugin.json",
]
RELEASE = re.compile(r"^## v(\d+\.\d+\.\d+)$")
LABELS = ("- Applies when:", "- Tune performs:", "- Operator:")


def main() -> int:
    failures: list[str] = []
    text = LEDGER.read_text(encoding="utf-8")
    releases = [m.group(1) for m in (RELEASE.match(line) for line in text.splitlines()) if m]
    if not releases:
        failures.append(f"{LEDGER.relative_to(ROOT)}: no `## vX.Y.Z` heading")
    else:
        newest = releases[0]
        as_tuple = lambda v: tuple(int(part) for part in v.split("."))
        if releases != sorted(releases, key=as_tuple, reverse=True):
            failures.append(f"{LEDGER.relative_to(ROOT)}: release headings are not newest first")
        for manifest in MANIFESTS:
            version = json.loads(manifest.read_text(encoding="utf-8")).get("version")
            if version != newest:
                failures.append(
                    f"{manifest.relative_to(ROOT)}: version {version!r} differs from newest ledger heading {newest!r}"
                )
    # every change under a release carries the three labels
    sections = re.split(r"^## ", text, flags=re.M)[1:]
    for section in sections:
        heading = section.splitlines()[0]
        if not RELEASE.match("## " + heading):
            continue
        for change in re.split(r"^### ", section, flags=re.M)[1:]:
            title = change.splitlines()[0]
            for label in LABELS:
                if not any(line.startswith(label) for line in change.splitlines()):
                    failures.append(f"{LEDGER.relative_to(ROOT)}: v{heading[1:]} / {title!r} lacks `{label}`")
    if failures:
        print("\n".join(failures), file=sys.stderr)
        return 1
    print(f"migration ledger is at v{releases[0]} and matches every manifest")
    return 0


if __name__ == "__main__":
    sys.exit(main())
