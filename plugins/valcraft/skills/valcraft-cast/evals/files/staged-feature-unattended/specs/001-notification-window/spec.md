---
id: FEAT-001
title: Notification window
status: draft
spec_issue: TBD
created: 2026-08-01
updated: 2026-08-01
---

# Notification window

## Sources

- `docs/product-brief.md`

## Summary

Let account holders define a daily window in which activity notifications may be delivered.

## Functional requirements

- FR-001: The user MUST be able to set one daily notification start time and end time.
- FR-002: The system MUST suppress notification delivery outside the configured window.

## Acceptance criteria

- [ ] AC-001: A saved window remains visible after the user returns to notification settings.
- [ ] AC-002: A notification generated outside the window is not delivered during the quiet period.

## Open questions

- When the notification window opens, should notifications queued during the quiet period be delivered or discarded?
