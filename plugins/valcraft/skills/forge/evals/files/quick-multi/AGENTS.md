# Agent instructions

project_tracker: github github_repository: github.example.test/acme/ledger

## Orientation

- `docs/` contains product context, working plans, and architecture decisions.
- `specs/` contains canonical feature specifications; `specs/quick/` holds quick tasks.
- `src/` contains application code. `tests/` contains automated tests.

## Commands

- Test: `PYTHONPATH=src python3 -m unittest discover -s tests`

## Change discipline

- Reference requirement and task IDs (`FR-`, `AC-`, `Q-NNN QT-XXX`) from commits and tests.
- Update affected specs, ADRs, and docs in the same change as the code.
