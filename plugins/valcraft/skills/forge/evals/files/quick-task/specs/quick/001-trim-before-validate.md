---
id: Q-001
created: 2026-08-12
---

# `require_non_empty` rejects whitespace-only values

## Sources

- operator request, 2026-08-12

## Requirements

- FR-001: `require_non_empty` MUST treat a value made only of whitespace as empty.
- AC-001: `require_non_empty("   ", "name")` raises `ValueError` naming `name`.
- AC-002: `require_non_empty(" a ", "name")` returns `" a "` unchanged — the helper
  validates, it does not trim.

## Approach

In `src/validation.py`, test `value.strip() == ""` instead of `value == ""`; keep the
return value untouched. Add the two cases to `tests/test_validation.py` in the existing
`unittest` style. Nothing else changes.

## Tasks

- [ ] T-001 Reject whitespace-only values in `require_non_empty`; verifies AC-001 and
      AC-002.
