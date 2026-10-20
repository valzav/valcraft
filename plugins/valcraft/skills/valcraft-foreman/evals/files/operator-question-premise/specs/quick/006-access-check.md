---
status: active
---

# Q-006 Shared access check

## Requirements

- FR-001: `can_open(user, transcript)` returns whether the user may open the transcript under its access level.

## Acceptance criteria

- AC-001: A records-team member can open a `restricted` transcript; any other user cannot.

## Tasks

- [ ] QT-001 Add `can_open` and its tests; verifies FR-001, AC-001.
