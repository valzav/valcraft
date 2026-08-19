---
feature: FEAT-001
status: draft
created: 2026-08-05
updated: 2026-08-05
---

# Tasks: Workspace invitations

## Completion definition

The feature is complete when AC-001 and AC-002 are verified, automated checks pass, and affected docs are current.

## Phase 1: Invitation record

- [ ] T-001 Add the `Invitation` record and `create_invitation`; verifies FR-001.

## Phase 2: Acceptance

- [ ] T-002 Add `accept_invitation` and the membership write; verifies FR-002; blocked by T-001.
- [ ] T-003 Add unit tests for the already-used token path; supports AC-002; blocked by T-002.
