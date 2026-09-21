---
id: FEAT-001
title: Tag filter
status: draft
spec_issue: null
created: 2026-08-07
updated: 2026-08-07
---

# Tag filter

## Sources

- `docs/tag-filter-prd.md`

## Summary

A reader narrows the note list by toggling tag chips and shares the filtered view by link.

## Functional requirements

- FR-001: The note list MUST show one chip per tag, and a click on a chip MUST toggle that tag.
- FR-002: With one or more tags active, the list MUST show only notes that carry every active tag.
- FR-003: The active tags MUST appear in the page URL, and opening that URL MUST restore the same filter.

## Quality requirements

- NFR-001: The browser console MUST show no error while the reader toggles chips.

## Acceptance criteria

- [ ] AC-001: Toggling the chip `draft` on shows only notes tagged `draft`; toggling it off shows every note again.
- [ ] AC-002: With `draft` and `idea` both active, a note tagged only `draft` is hidden.
- [ ] AC-003: Opening a URL copied while `draft` was active shows the list already filtered to `draft`.
- [ ] AC-004: The browser console shows no error during AC-001 to AC-003.
