# Agent instructions

project_tracker: local

## Orientation

- `docs/` contains product context, working plans, and architecture decisions.
- `specs/` contains canonical feature specifications.
- `src/` contains application code. `tests/` contains automated tests.

## Commands

- Test: `PYTHONPATH=src python3 -m unittest discover -s tests`

## Change discipline

- Reference requirement and task IDs (`FR-`, `AC-`, `T-`) from commits and tests.
- Non-trivial work starts with a plan in `docs/plans/YYYY-MM-DD-NNN-<type>-<slug>-plan.md`.
