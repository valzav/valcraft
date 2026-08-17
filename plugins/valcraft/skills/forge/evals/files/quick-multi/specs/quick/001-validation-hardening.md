---
id: Q-001
created: 2026-08-12
---

# `require_non_empty` hardening

## Sources

- operator request, 2026-08-12

## Requirements

- FR-001: `require_non_empty` MUST treat a value made only of whitespace as empty.
- FR-002: `require_non_empty` MUST reject `None` the same way it rejects an empty
  string.
- AC-001: `require_non_empty("   ", "name")` raises `ValueError` naming `name`.
- AC-002: `require_non_empty(None, "name")` raises `ValueError` naming `name`; the
  message is the same one an empty string produces.
- AC-003: `require_non_empty(" a ", "name")` still returns `" a "` unchanged.

## Approach

In `src/validation.py`: T-001 tests `value.strip() == ""` (done). T-002 treats `None`
as empty before the strip check so `None.strip()` is never called; the signature widens
to `Optional[str]` and the docstring says so. Tests for each criterion go in
`tests/test_validation.py` in the existing `unittest` style. Nothing else changes.

## Tasks

- [x] T-001 Reject whitespace-only values; verifies AC-001 and AC-003.
- [ ] T-002 Reject `None`; verifies AC-002 and keeps AC-003; blocked by T-001.
