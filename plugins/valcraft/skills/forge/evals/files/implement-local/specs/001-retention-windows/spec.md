---
id: FEAT-001
title: Activity retention windows
status: draft
spec_issue: null
created: 2026-08-07
updated: 2026-08-07
---

# Activity retention windows

## Sources

- `docs/retention-windows-prd.md`

## Summary

An admin sets how long the workspace keeps activity records, expressed as a retention
window such as `30d` or `12h`.

## Functional requirements

- FR-001: The system MUST accept a retention window written as a positive whole number
  followed by `h` for hours or `d` for days, and MUST reject any other value.
- FR-002: The system MUST remove activity records older than the configured window.

## Acceptance criteria

- [ ] AC-001: `30d` and `12h` are accepted and understood as 30 days and 12 hours.
- [ ] AC-002: An empty value, a zero or negative count, an unknown unit, and a value with
      surrounding whitespace are each rejected.
- [ ] AC-003: An activity record older than the configured window is removed.
