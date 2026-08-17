---
id: FEAT-001
title: Workspace invitations
status: draft
spec_issue: null
created: 2026-08-05
updated: 2026-08-05
---

# Workspace invitations

## Sources

- `docs/workspace-invites-prd.md`

## Summary

An admin invites a teammate by email address. The teammate accepts and joins the
workspace.

## Functional requirements

- FR-001: An admin MUST be able to create an invitation for an email address.
- FR-002: An invited person MUST be able to accept an invitation and join the workspace.

## Acceptance criteria

- [ ] AC-001: Creating an invitation for a valid email address produces a pending
      invitation with a single-use token.
- [ ] AC-002: Accepting a pending invitation adds the person to the workspace and marks
      the invitation used.
