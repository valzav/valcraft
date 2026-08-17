---
id: FEAT-001
title: Support email routing
status: draft
spec_issue: null
created: 2026-08-09
updated: 2026-08-09
---

# Support email routing

## Sources

- `docs/email-routing-prd.md`

## Summary

Route an incoming support email to the workspace that owns the sender's domain.

## Functional requirements

- FR-001: The system MUST route an incoming email to the workspace that owns the
  sender's domain.
- FR-002: The system MUST place an email with no matching domain in an unrouted queue.

## Acceptance criteria

- [ ] AC-001: An email from a claimed domain appears in that workspace's inbox.
- [ ] AC-002: An email from an unclaimed domain appears in the unrouted queue.
