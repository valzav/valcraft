# Forge handoff

Changed: src/invites.py (use_link, ExpiredInvite), tests/test_invites.py — T-002, FR-002, FR-003, AC-002.
Verification: `PYTHONPATH=src python3 -m unittest discover -s tests` → Ran 5 tests, OK. Mutation check: reverted the use_link expiry compare, test_expired_rejects went red, restored, green.
Scope: touched src/invites.py, tests/test_invites.py; untouched src/cli.py (T-003).
Open questions: none.
Pinned review target: branch feat/f001-t002-use-link, base origin/dev.
PR: https://example.invalid/loop-local/pull/15 (base: dev)
Status: done

# Step 10 close prep

Ticked `- [x] T-002` in specs/001-invite-links/tasks.md, commit `T-002: mark complete`, pushed.
Status: done
