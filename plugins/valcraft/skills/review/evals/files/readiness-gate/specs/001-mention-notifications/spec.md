---
id: FEAT-001
title: Mention notifications
status: draft
spec_issue: null
created: 2026-08-06
updated: 2026-08-06
---

# Mention notifications

## Sources

- `docs/mention-notifications-prd.md`

## Summary

Notify a member when another member mentions them in a comment.

## Functional requirements

- FR-001: The system MUST notify a mentioned member when a comment mentioning them is published.
- FR-002: A member MUST be able to open the mentioning comment from the notification.

## Acceptance criteria

- [ ] AC-001: Publishing a comment that mentions a member produces one notification for that member.
- [ ] AC-002: Opening the notification shows the mentioning comment in context.

## Open questions

- Does editing a published comment to add a new mention notify the newly mentioned member, or do we only notify on first publish?
