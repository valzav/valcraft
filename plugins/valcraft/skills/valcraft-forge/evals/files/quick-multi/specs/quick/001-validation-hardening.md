---
id: Q-001
created: 2026-08-12
---

# `require_non_empty` hardening

## Sources

- operator request, 2026-08-12

## Requirements

- FR-001: `require_non_empty` MUST treat a value made only of whitespace as empty.
- FR-002: `require_non_empty` MUST reject `None` the same way it rejects an empty string.
- AC-001: `require_non_empty("   ", "name")` raises `ValueError` naming `name`.
- AC-002: `require_non_empty(None, "name")` raises `ValueError` naming `name`; the message is the same one an empty string produces.
- AC-003: `require_non_empty(" a ", "name")` still returns `" a "` unchanged.

## Approach

In `src/validation.py`: QT-001 tests `value.strip() == ""` (done). QT-002 treats `None` as empty before the strip check so `None.strip()` is never called; the signature widens to `Optional[str]` and the docstring says so. Tests for each criterion go in `tests/test_validation.py` in the existing `unittest` style. Nothing else changes.

## Verification

- TS-001 (AC-001): Observation: a `unittest` case in `tests/test_validation.py`, run with `PYTHONPATH=src python3 -m unittest discover -s tests`, asserts that `require_non_empty("   ", "name")` raises `ValueError` and that the message contains `name`. Guarded defect: the helper keeps comparing `value == ""`, so a whitespace-only value passes validation. Failing input: `"   "` at the QT-001 head, where the unchanged `value == ""` comparison returns `"   "` instead of raising. Positive control: the case passes once the helper tests `value.strip() == ""`. Domain: whitespace-only strings; `str.strip()` removes every whitespace character alike, so the outcome depends only on whether the stripped value is empty, and the three-space case plus the existing empty-string case `test_rejects_empty_value` cover both outcomes of that test.
- TS-002 (AC-002): Observation: a `unittest` case in `tests/test_validation.py`, run with `PYTHONPATH=src python3 -m unittest discover -s tests`, asserts that `require_non_empty(None, "name")` raises `ValueError` and that its message equals the message `require_non_empty("", "name")` raises. Guarded defect: `None` reaches `value.strip()` and raises `AttributeError`, or a separate `None` branch raises a different message. Failing input: `None` at the QT-002 head, where `None.strip()` raises `AttributeError` instead of `ValueError`. Positive control: the case passes once the helper treats `None` as empty before the strip check. Domain: the single value `None`, enumerated completely, with its message compared against the empty-string message.
- TS-003 (AC-003): Observation: a `unittest` case in `tests/test_validation.py`, run with `PYTHONPATH=src python3 -m unittest discover -s tests`, asserts that `require_non_empty(" a ", "name")` returns exactly `" a "`. Guarded defect: the whitespace or `None` handling returns a stripped or normalized value instead of `value`, so the helper trims what it only validates. Failing input: `" a "` against a temporary edit at the QT-001 head that returns `value.strip()`, which yields `"a"`. Positive control: the case passes on the implemented helper, which returns `value` unchanged. Domain: values with non-whitespace content and surrounding whitespace; `" a "` carries whitespace on both sides, so a trim on either side changes the result.

## Tasks

- [x] QT-001 Reject whitespace-only values; verifies AC-001 and AC-003.
- [ ] QT-002 Reject `None`; verifies AC-002 and keeps AC-003; blocked by QT-001.
