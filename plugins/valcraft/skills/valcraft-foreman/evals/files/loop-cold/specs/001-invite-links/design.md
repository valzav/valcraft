---
feature: FEAT-001
status: draft
created: 2026-08-16
updated: 2026-08-16
---

# Design: Invite links

## Summary

`src/invites.py` holds `Link(id, workspace_id, token, expires_at)` records in `_links`, keyed by token. `create_link(workspace_id, now) -> Link` sets `expires_at = now + LINK_LIFETIME`, where `LINK_LIFETIME` is 7 days (FR-001, FR-003, AC-001; VB-001). `use_link(token, member_id, now) -> Membership` looks up `_links[token]`, raises `UnknownInvite` for a missing token, raises `ExpiredInvite` when `now >= expires_at`, and only then records `Membership(workspace_id, member_id)` in a set, so a repeated use keeps one membership (FR-002, FR-003, AC-002, AC-003). `src/invite_cli.py create <workspace_id>` calls `create_link` with the current time and prints the token (FR-001, AC-004).

## Interfaces

- `create_link(workspace_id, now) -> Link` in `src/invites.py` (T-001).
- `use_link(token, member_id, now) -> Membership`, `UnknownInvite`, and `ExpiredInvite` in `src/invites.py` (T-002).
- `python3 src/invite_cli.py create <workspace_id>` (T-003).

## Failure handling

- An unknown token raises `UnknownInvite` before any write (AC-003).
- An expired token raises `ExpiredInvite` before any write (AC-002).

## Verified baseline assumptions

- VB-001: At baseline `c2585740b55c613149294af38eaf089d03637409`, `src/invites.py` defines `Link(id, workspace_id, token, expires_at)`, `LINK_LIFETIME = timedelta(days=7)`, `create_link(workspace_id, now)`, and the `_links` store keyed by token. Check: `git show c2585740b55c613149294af38eaf089d03637409:src/invites.py | grep -c "class Link\|LINK_LIFETIME = timedelta(days=7)\|def create_link\|_links\[link.token\]"` printed `4`, and `PYTHONPATH=src python3 -m unittest discover -s tests` printed `OK`. Supports the `_links[token]` lookup in `use_link`.

## Test strategy

- TS-001 (AC-001): Observation: `tests/test_invites.py` calls `create_link("w1", now)` 100 times and asserts `expires_at == now + timedelta(days=7)` and a token matching `^[A-Za-z0-9_-]+$`. Guarded defect: a changed lifetime or a token built from a URL-unsafe alphabet. Failing input: set `LINK_LIFETIME = timedelta(days=6)`, or append `"/"` to the generated token. Positive control: the baseline `create_link` passes. Domain: the lifetime is one constant, so one `now` covers it; every token comes from the same generator, so a defective alphabet appears in every call.
- TS-002 (AC-002, FR-003): Observation: a unit test uses one link at `expires_at - 1 second`, `expires_at`, and `expires_at + 1 second`, and asserts success, `ExpiredInvite`, and `ExpiredInvite` with the membership set unchanged. Guarded defect: `now > expires_at` in place of `>=`, or the membership write placed before the expiry check. Failing input: the `>` comparison fails the `expires_at` case; the early write fails the unchanged-set assertion. Positive control: the T-002 `use_link` passes all three cases. Domain: expiry is one threshold on `now`, compared exactly, so the three cases bracket the only boundary.
- TS-003 (AC-003, FR-002): Observation: a unit test uses a valid token twice for member `m1` and asserts one `Membership("w1", "m1")`, then uses an unknown token and asserts `UnknownInvite` with the set unchanged. Guarded defect: a list that appends a duplicate membership, or an unknown token that writes before failing. Failing input: store memberships in a list; the repeated use then yields two entries. Positive control: the T-002 `use_link` passes. Domain: the token states are valid, repeated, and unknown, and the test enumerates all three.
- TS-004 (AC-004): Observation: a unit test runs `python3 src/invite_cli.py create w1` with `subprocess.run` and asserts exit code 0 and one output line that matches `^[A-Za-z0-9_-]+$` and names a stored link. Guarded defect: the CLI prints a repr or exits non-zero. Failing input: print the `Link` object instead of its token. Positive control: the T-003 CLI passes. Domain: the CLI has one subcommand and one argument, and the test drives it.
