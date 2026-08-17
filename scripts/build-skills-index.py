#!/usr/bin/env python3
"""Write plugins/valcraft/skills/index.json — the OpenCode remote skills index.

OpenCode's `skills.urls` (v1 config) / `skills` (v2 config) fetches `<url>/index.json`,
then `<url>/<name>/<file>` for every listed file, and refreshes a cached skill when its
`version` changes. This script lists each skill's shipped files (SKILL.md, references/,
templates/, agents/ — never evals/) and sets `version` to a content hash of those files,
so a change to any shipped file is a new version and an unchanged skill is not re-pulled.

Run from the repository root:

    python3 scripts/build-skills-index.py            # write index.json
    python3 scripts/build-skills-index.py --check    # exit 1 if index.json is stale
"""

from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKILLS = ROOT / "plugins" / "valcraft" / "skills"
INDEX = SKILLS / "index.json"
SHIPPED_DIRS = ("references", "templates", "agents")


def skill_files(skill_dir: Path) -> list[str]:
    files = ["SKILL.md"]
    for sub in SHIPPED_DIRS:
        base = skill_dir / sub
        if not base.is_dir():
            continue
        for path in sorted(base.rglob("*")):
            if path.is_file():
                files.append(path.relative_to(skill_dir).as_posix())
    return files


def content_version(skill_dir: Path, files: list[str]) -> str:
    digest = hashlib.sha256()
    for rel in files:
        digest.update(rel.encode())
        digest.update(b"\0")
        digest.update((skill_dir / rel).read_bytes())
        digest.update(b"\0")
    return digest.hexdigest()[:16]


def build() -> dict:
    skills = []
    for skill_dir in sorted(p for p in SKILLS.iterdir() if p.is_dir()):
        if not (skill_dir / "SKILL.md").is_file():
            continue
        files = skill_files(skill_dir)
        skills.append(
            {
                "name": skill_dir.name,
                "version": content_version(skill_dir, files),
                "files": files,
            }
        )
    return {"skills": skills}


def render(index: dict) -> str:
    return json.dumps(index, indent=2, ensure_ascii=False) + "\n"


def main(argv: list[str]) -> int:
    text = render(build())
    if "--check" in argv:
        current = INDEX.read_text() if INDEX.exists() else ""
        if current != text:
            print(
                f"{INDEX.relative_to(ROOT)} is stale; run scripts/build-skills-index.py",
                file=sys.stderr,
            )
            return 1
        print(f"{INDEX.relative_to(ROOT)} is current")
        return 0
    INDEX.write_text(text)
    print(f"wrote {INDEX.relative_to(ROOT)} ({len(json.loads(text)['skills'])} skills)")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
