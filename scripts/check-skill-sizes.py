#!/usr/bin/env python3
"""Enforce the Codex model-visible skill-size ceiling.

Codex 0.149.1 truncates each SKILL.md beyond 8,000 UTF-8 bytes (docs/development.md),
silently cutting whatever contract text follows the cutoff.
"""

from __future__ import annotations

import sys
from pathlib import Path

LIMIT = 8000
ROOT = Path(__file__).resolve().parents[1]
SKILLS = ROOT / "plugins" / "valcraft" / "skills"


def main() -> int:
    failures = []
    for path in sorted(SKILLS.glob("*/SKILL.md")):
        size = path.stat().st_size
        if size > LIMIT:
            failures.append(
                f"{path.relative_to(ROOT)}: {size} bytes exceeds the {LIMIT}-byte Codex ceiling"
            )
    if failures:
        print("\n".join(failures), file=sys.stderr)
        return 1
    print(f"all SKILL.md files fit the {LIMIT}-byte Codex ceiling")
    return 0


if __name__ == "__main__":
    sys.exit(main())
