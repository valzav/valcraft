# Agent instructions

## Project metadata

```yaml
project_tracker: github
github_repository: github.example.test/acme/ledger
foreman_backend: subagents
foreman_approval_mode: unattended
foreman_default_branch: dev
foreman_release_branch: main
```

## Orientation

- `docs/` contains product context, working plans, and architecture decisions.
- `specs/` contains canonical feature specifications; `specs/quick/` holds quick tasks.
- `src/` contains application code. `tests/` contains automated tests.

## Commands

- Test: `PYTHONPATH=src python3 -m unittest discover -s tests`

## Change discipline

- Reference requirement and task IDs (`FR-`, `AC-`, `Q-NNN QT-XXX`) from commits and tests.
- Non-trivial work starts with a plan in `docs/plans/YYYY-MM-DD-NNN-<type>-<slug>-plan.md`.
