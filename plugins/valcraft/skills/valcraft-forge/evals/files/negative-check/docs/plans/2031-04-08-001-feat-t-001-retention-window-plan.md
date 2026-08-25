# T-001: Parse retention windows

## Contract

Implement T-001 from `specs/001-retention-windows/tasks.md`. Preserve the exact input grammar in FR-001, AC-001, and AC-002, and the no-warning requirement in NFR-001 and AC-004. Do not implement the T-002 sweep.

## Implementation

- Add `parse_window(value: str) -> int` in `src/retention.py`.
- Accept a positive whole number followed by exactly `h` or `d`.
- Return seconds.
- Raise `ValueError` for every rejected form named by AC-002.
- Never call `warnings.warn` from the parser.
- Add focused `unittest` coverage in `tests/test_retention.py`, including a test that parses every AC-001 form under `warnings.catch_warnings(record=True)` and asserts the recorded list is empty (AC-004).

## Verification

Run `PYTHONPATH=src python3 -m unittest discover -s tests`. Mutation-check the parser by temporarily accepting one rejected form and observing its focused test fail before restoring the implementation.
