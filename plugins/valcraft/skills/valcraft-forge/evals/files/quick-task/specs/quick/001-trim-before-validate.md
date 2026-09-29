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
- AC-002: `require_non_empty(" a ", "name")` returns `" a "` unchanged — the helper validates, it does not trim.

## Approach

In `src/validation.py`, test `value.strip() == ""` instead of `value == ""`; keep the return value untouched. Add the two cases to `tests/test_validation.py` in the existing `unittest` style. Nothing else changes.

## Verification

- TS-001 (AC-001): Observation: a `unittest` case in `tests/test_validation.py`, run with `PYTHONPATH=src python3 -m unittest discover -s tests`, asserts that `require_non_empty("   ", "name")` raises `ValueError` and that the message contains `name`. Guarded defect: the helper keeps comparing `value == ""`, so a whitespace-only value passes validation. Failing input: `"   "` at the QT-001 head, where the unchanged `value == ""` comparison returns `"   "` instead of raising. Positive control: the case passes once the helper tests `value.strip() == ""`. Domain: whitespace-only strings; `str.strip()` removes every whitespace character alike, so the outcome depends only on whether the stripped value is empty, and the three-space case plus the existing empty-string case `test_rejects_empty_value` cover both outcomes of that test.
- TS-002 (AC-002): Observation: a `unittest` case in `tests/test_validation.py`, run with `PYTHONPATH=src python3 -m unittest discover -s tests`, asserts that `require_non_empty(" a ", "name")` returns exactly `" a "`. Guarded defect: the fix returns `value.strip()` instead of `value`, so the helper trims what it only validates. Failing input: `" a "` against a temporary edit at the QT-001 head that returns `value.strip()`, which yields `"a"`. Positive control: the case passes on the implemented helper, which returns `value` unchanged. Domain: values with non-whitespace content and surrounding whitespace; `" a "` carries whitespace on both sides, so a trim on either side changes the result.

## Tasks

- [ ] QT-001 Reject whitespace-only values in `require_non_empty`; verifies AC-001 and AC-002.
