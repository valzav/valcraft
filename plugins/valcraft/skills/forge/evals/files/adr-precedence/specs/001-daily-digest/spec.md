---
id: FEAT-001
title: Daily activity digest
status: draft
spec_issue: null
created: 2026-08-09
updated: 2026-08-09
---

# Daily activity digest

## Sources

- `docs/daily-digest-prd.md`

## Summary

A workspace picks a daily send time, and each member receives one digest of workspace
activity at that time.

## Functional requirements

- FR-001: An admin MUST be able to set the workspace's daily digest send time.
- FR-002: The system MUST send each member one digest per day at the configured time.

## Acceptance criteria

- [ ] AC-001: Setting the send time to 09:00 stores that send time for the workspace.
- [ ] AC-002: A member receives exactly one digest per day, at the configured send time
      in the workspace's timezone.
