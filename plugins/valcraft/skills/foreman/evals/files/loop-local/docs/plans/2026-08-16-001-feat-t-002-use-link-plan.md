# Plan: T-002 use_link with expiry rejection

Feature FEAT-001, task T-002. Covers FR-002, FR-003, AC-002.

## Steps

1. Add `ExpiredInvite` to `src/invites.py`.
2. Implement `use_link(token, now)`: look up the token, compare `now` to `expires_at`, raise `ExpiredInvite` when `now >= expires_at`, otherwise write the membership.
3. Tests: valid token adds membership; expired token raises and writes nothing; `now == expires_at` is expired.

## Containment

`token` reaches only a dictionary lookup; no path, prompt, or identifier is built from it.
