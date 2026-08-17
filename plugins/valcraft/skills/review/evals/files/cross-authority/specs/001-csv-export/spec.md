---
id: FEAT-001
title: Bounded CSV export
status: draft
spec_issue: null
created: 2026-08-03
updated: 2026-08-03
---

# Bounded CSV export

## Sources

- `docs/csv-export-prd.md`

## Summary

An analyst exports a report to CSV. The export is bounded so one export cannot degrade
the shared reporting database.

## Functional requirements

- FR-001: An analyst MUST be able to export a report to CSV.
- FR-002: The system MUST cap a single export at 500 rows and tell the analyst when the
  cap truncated the result.

## Acceptance criteria

- [ ] AC-001: Exporting a 400-row report produces a 400-row file with no truncation
      notice.
- [ ] AC-002: Exporting a 900-row report produces a 500-row file and a visible
      truncation notice naming the cap.
