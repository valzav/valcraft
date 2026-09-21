---
feature: FEAT-001
status: draft
created: 2026-08-07
updated: 2026-08-07
---

# Design: Tag filter

## Summary

Three plain ES modules under `src/filter/` hold the filter logic, and the existing list view renders chips from them (FR-001, FR-002, FR-003, NFR-001).

## Impact on existing architecture

`src/filter/tags.js` derives the tag set from the loaded notes. `src/filter/match.js` decides whether a note carries every active tag. `src/filter/state.js` reads and writes the active tags in the URL query. `src/list/view.js` renders one chip per tag and re-renders the list when a chip toggles.

## Interfaces

The URL query parameter `tags` holds the active tags as a comma-separated list.

## Test strategy

Unit tests cover the filter modules. A browser check covers the chip toggle and the console.

## Alternatives considered

Keeping the filter in memory only was rejected because FR-003 requires a shareable link.
