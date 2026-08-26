# Agent instructions

## Orientation

- `docs/` contains product context, working plans, and architecture decisions.
- `specs/` contains canonical feature specifications.
- `src/` contains application code. `tests/` contains automated tests.

On conflict, accepted ADRs prevail, then `specs/`, then derived `docs/`.

## Commands

- Test: `PYTHONPATH=src python3 -m unittest discover -s tests`
