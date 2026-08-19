---
feature: FEAT-001
status: draft
created: 2026-08-07
updated: 2026-08-07
---

# Design: Activity retention windows

## Summary

`parse_window` converts a retention window string into a whole number of seconds, so the rest of the system works in one unit (FR-001). The sweep job compares a record's age in seconds against that value (FR-002).

## Interfaces

`parse_window(value: str) -> int` in `src/retention.py`.

Accepted input is exactly a positive whole number followed by a single unit character: `h` for hours, `d` for days. `30d` returns 2592000. `12h` returns 43200.

The function raises `ValueError` for every other input, including an empty string, a value with leading or trailing whitespace, a zero or negative count, a non-integer count, a missing unit, and an unknown unit. Rejection happens before any conversion, and the message names the offending value.

## Failure handling

`parse_window` never returns a default. A caller that cannot parse a configured window leaves the previous window in place.

## Test strategy

Unit tests cover each accepted unit and every rejection case listed above. They follow the `unittest` style already used in `tests/test_validation.py`.
