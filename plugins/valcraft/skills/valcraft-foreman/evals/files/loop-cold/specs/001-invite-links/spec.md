---
id: FEAT-001
title: Invite links
status: draft
spec_issue: null
created: 2026-08-16
updated: 2026-08-16
---

# Invite links

## Sources

- `docs/product-brief.md`

## Problem

Workspace admins need to add members without sending email invitations.

## Goals and non-goals

- Goal: an admin shares one link that adds whoever uses it before it expires.
- Non-goal: revoking a link before it expires.
- Non-goal: limiting how many callers may use one link.

## User scenarios

- An admin runs the CLI, receives a token, and shares it. A colleague uses the token within 7 days and becomes a workspace member.
- A colleague uses a token after 7 days and is rejected without becoming a member.

## Functional requirements

- FR-001: An admin MUST be able to create an invite link for a workspace from the command line.
- FR-002: Using a valid invite link MUST make the caller a member of the link's workspace exactly once; using an unknown token MUST be rejected without a write.
- FR-003: An invite link MUST expire 7 days after creation; using an expired link MUST be rejected.

## Edge behavior

- A link is expired from the instant `now` equals its expiry onward.
- A caller who is already a member and uses a valid link keeps exactly one membership.

## Acceptance criteria

- [ ] AC-001: Creating a link returns a URL-safe token and an expiry exactly 7 days after creation.
- [ ] AC-002: Using a token at or after its expiry raises `ExpiredInvite` and writes no membership.
- [ ] AC-003: Using a valid token makes the caller a member of the link's workspace exactly once, including on a repeated use; an unknown token raises `UnknownInvite` and writes no membership.
- [ ] AC-004: `python3 src/invite_cli.py create <workspace_id>` prints the new link's token on one line and exits 0.

## Assumptions

none

## Open questions

none
