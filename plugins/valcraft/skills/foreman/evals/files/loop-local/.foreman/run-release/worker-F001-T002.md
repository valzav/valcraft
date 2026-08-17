## Forge handoff

### Changed (IDs)

src/invites.py (`use_link`, `ExpiredInvite`), tests/test_invites.py — T-002, FR-002, FR-003, AC-002.

### Verification evidence

`PYTHONPATH=src python3 -m unittest discover -s tests` → Ran 5 tests, OK. Mutation check: reverted the `use_link` expiry compare, `test_expired_rejects` went red, restored, green. A bug that slips past: none of the tests exercise a link used at exactly `expires_at` (spec settles it as expired; covered by `test_boundary_expired`).

### Scope: touched / untouched

touched src/invites.py, tests/test_invites.py; untouched src/cli.py (T-003).

### Open questions and deferred findings

none

### Review target

branch feat/f001-t002-use-link, base origin/main. PR: https://example.invalid/repo/pull/14 (base: main)
Status: done
