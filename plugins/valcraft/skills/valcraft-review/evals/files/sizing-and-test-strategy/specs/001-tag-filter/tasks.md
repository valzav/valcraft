---
feature: FEAT-001
status: draft
created: 2026-08-07
updated: 2026-08-07
---

# Tasks: Tag filter

## Completion definition

The feature is complete when all applicable acceptance criteria are verified, automated checks pass, and affected docs are current.

## Phase 1: Filter modules

- [ ] T-001 Add `src/filter/tags.js` to derive the tag set from the loaded notes; supports FR-001.
- [ ] T-002 Add `src/filter/match.js` to keep only notes that carry every active tag; supports FR-002; blocked by T-001.
- [ ] T-003 Add `src/filter/state.js` to read and write the active tags in the URL query; supports FR-003; blocked by T-001.

## Phase 2: Surface

- [ ] T-004 Render one chip per tag in `src/list/view.js` and re-render the list on toggle; supports FR-001, FR-002, FR-003; blocked by T-002, T-003.

## Phase 3: Verification

- [ ] T-005 Add unit tests covering AC-001 and AC-002; verifies FR-001, FR-002; blocked by T-004.
- [ ] T-006 Verify AC-001 to AC-004 in the browser and confirm the console shows no error; verifies FR-003, NFR-001; blocked by T-005.
