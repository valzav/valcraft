---
id: FEAT-001
title: Bulk tagging
status: draft
spec_issue: TBD
created: 2026-09-20
updated: 2026-09-20
---

# Bulk tagging

## Sources

- `docs/bulk-tagging-prd.md`

## Summary

A user adds one tag to several selected records in one action.

## Functional requirements

- FR-001: A user MUST be able to select several records in the record list and add one tag to all of them in one action.
- FR-002: The system MUST NOT add a tag twice to a record that already carries it.
- FR-003: The system MUST report how many records received the tag.

## Edge cases

- A selection in which every record already carries the tag reports zero records tagged and changes nothing.

## Acceptance criteria

- [ ] AC-001: After bulk tagging a selection, every selected record carries the tag exactly once.
- [ ] AC-002: The result count equals the number of selected records that did not already carry the tag.

## Assumptions

- None.

## Open questions

- None.
