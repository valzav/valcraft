---
feature: FEAT-001
status: draft
created: 2026-08-16
updated: 2026-08-16
---

# Tasks: Invite links

## Completion definition

The feature is complete when AC-001 through AC-004 are verified and automated checks pass.

## Phase 1: Links

- [x] T-001 Add the `Link` record and `create_link` (TS-001); verifies FR-001, AC-001.
- [ ] T-002 Add `use_link` with unknown-token and expiry rejection (TS-002, TS-003) and single membership writes (TS-003); verifies FR-002, FR-003, AC-002, AC-003; blocked by T-001.
- [ ] T-003 Add the admin CLI for `create_link` (TS-004); verifies FR-001, AC-004; blocked by T-001.
