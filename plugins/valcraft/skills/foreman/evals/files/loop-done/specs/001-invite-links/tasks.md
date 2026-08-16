---
feature: FEAT-001
status: complete
created: 2026-08-16
updated: 2026-08-16
---

# Tasks: Invite links

## Completion definition

The feature is complete when AC-001 and AC-002 are verified and automated checks pass.

## Phase 1: Links

- [x] T-001 Add the `Link` record and `create_link`; verifies FR-001, AC-001.
- [x] T-002 Add `use_link` with expiry rejection; verifies FR-002, FR-003, AC-002; blocked by T-001.
- [x] T-003 Add the admin CLI for `create_link`; supports FR-001; blocked by T-002.
