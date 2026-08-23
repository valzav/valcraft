# Plan: T-001 request timeout

Implements T-001 (verifies FR-001, FR-002; AC-001, AC-002, AC-003) for FEAT-002.

## Scope

Touched, exclusively:

- `src/config/model_ref.py` — add the optional `timeout_seconds` field to `ModelRef`, default 30.
- `src/config/loader.py` — parse `timeout_seconds` as a positive integer when present; reject anything else with a message naming the field.
- `src/providers/client.py` — pass `ModelRef.timeout_seconds` to the HTTP session.
- `tests/test_model_ref.py` — loader and client tests.
- `docs/configuration.md` — document the new key.

Deliberately untouched: every other path in the repository.

## Approach

Extend the `ModelRef` dataclass with `timeout_seconds: int = 30`. The loader accepts the key when present and rejects a non-positive or non-integer value with a message naming `timeout_seconds`. The provider client reads the field and sets the session timeout.

## Verification

- Unit test: a reference without `timeout_seconds` loads with the value 30 (FR-002).
- Unit test: a reference with `timeout_seconds: 5` loads with the value 5 (FR-001).
- Unit test: `timeout_seconds: 0`, `timeout_seconds: -1`, `timeout_seconds: 2.5`, and `timeout_seconds: "5"` each fail with a message naming the field (AC-003).
- Integration test: with `timeout_seconds: 5` and a provider stub that never answers, the call aborts after 5 seconds (AC-001); without the field, after 30 seconds (AC-002).

## Open decisions

None.
