---
id: FEAT-001
title: Invite links
status: draft
spec_issue: 40
created: 2026-08-16
updated: 2026-08-16
---

# Invite links

## Sources

- `docs/product-brief.md`

## Summary

An admin creates an invite link for a workspace. The link expires; an expired link is
rejected on use.

## Functional requirements

- FR-001: An admin MUST be able to create an invite link for a workspace.
- FR-002: Using a valid invite link MUST add the caller to the workspace.
- FR-003: An invite link MUST expire 7 days after creation; using an expired link MUST
  be rejected.

## Acceptance criteria

- [ ] AC-001: Creating a link returns a URL-safe token and an expiry exactly 7 days after
      creation.
- [ ] AC-002: Using an expired token raises `ExpiredInvite` and writes no membership.
