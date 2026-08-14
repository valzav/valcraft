---
feature: FEAT-001
status: draft
created: 2026-08-05
updated: 2026-08-05
---

# Design: Workspace invitations

## Summary

An `Invitation` record holds the target email address, the workspace id, a single-use
token, and a status of pending or used. Creation writes the record and returns the token
(FR-001). Acceptance looks the token up, adds the membership, and flips the status
(FR-002).

## Data model

`invitations(id, workspace_id, email, token, status)` where `status` is `pending` or
`used`. The token is a URL-safe random string generated with `secrets.token_urlsafe`.

## Interfaces

- `create_invitation(workspace_id, email) -> Invitation` in `src/invitations.py`.
- `accept_invitation(token) -> Membership` in `src/invitations.py`.

## Failure handling

Accepting an unknown or already-used token raises `InvalidInvitation`. Creation with a
malformed email address raises `ValueError` before any record is written.

## Test strategy

Unit tests cover token generation, creation validation, and the accept path, including
the already-used token case.
