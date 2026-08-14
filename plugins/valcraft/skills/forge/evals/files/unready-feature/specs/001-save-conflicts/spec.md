---
id: FEAT-001
title: Save conflict detection
status: draft
spec_issue: null
created: 2026-08-06
updated: 2026-08-06
---

# Save conflict detection

## Sources

- `docs/save-conflicts-prd.md`

## Summary

Detect that a document changed since the editor loaded it, and tell the member instead of
overwriting.

## Functional requirements

- FR-001: The system MUST detect that a document changed between load and save.
- FR-002: The system MUST tell the member their save was refused because of a conflict.

## Acceptance criteria

- [ ] AC-001: Saving a document that another member changed since load is refused with a
      conflict message.
- [ ] AC-002: Saving a document nobody else changed succeeds.

## Open questions

- When a save is refused, do we keep the member's unsaved text for them to re-apply, or
  discard it and reload the current version?
