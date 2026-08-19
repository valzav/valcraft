---
feature: FEAT-001
status: draft
created: 2026-08-03
updated: 2026-08-04
---

# Tasks: Bounded CSV export

## Completion definition

The feature is complete when AC-001 and AC-002 are verified, automated checks pass, and affected docs are current.

## Phase 1: Export path

- [ ] T-001 Add the CSV streaming endpoint; verifies FR-001.
- [ ] T-002 Add the row limiter and truncation notice; verifies FR-002; blocked by T-001.

## Phase 2: Verification

- [ ] T-003 Add tests for the truncation boundary; verifies AC-002; blocked by T-002.
