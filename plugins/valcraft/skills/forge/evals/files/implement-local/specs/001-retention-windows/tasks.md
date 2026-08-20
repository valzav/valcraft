---
feature: FEAT-001
status: draft
created: 2026-08-07
updated: 2026-08-07
---

# Tasks: Activity retention windows

## Completion definition

The feature is complete when AC-001, AC-002, and AC-003 are verified, automated checks pass, and affected docs are current.

## Phase 1: Window parsing

- [ ] T-001 Add `parse_window` to `src/retention.py` with unit tests; verifies FR-001, AC-001, and AC-002.

## Phase 2: Sweep

- [ ] T-002 Add the activity sweep that removes records older than the window; verifies FR-002 and AC-003; blocked by T-001.
