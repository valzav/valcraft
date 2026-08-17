## Forge handoff

### Changed (IDs)

src/invites.py (`use_link`, `ExpiredInvite`), tests/test_invites.py — T-002, FR-002, FR-003, AC-002.

### Verification evidence

unittest → Ran 5 tests, OK. Mutation check performed (`test_expired_rejects` red on unfixed code).

### Scope: touched / untouched

touched src/invites.py, tests/test_invites.py; untouched src/cli.py (T-003).

### Open questions and deferred findings

none

### Review target

branch feat/f001-t002-use-link, base origin/dev. PR: https://github.com/example/loop-github/pull/15 (base: dev)
Status: done
