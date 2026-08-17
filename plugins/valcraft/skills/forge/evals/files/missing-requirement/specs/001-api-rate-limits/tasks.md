---
feature: FEAT-001
status: draft
created: 2026-08-08
updated: 2026-08-08
---

# Tasks: API rate limits

## Completion definition

The feature is complete when AC-001 and AC-002 are verified and automated checks pass.

## Phase 1: Counting

- [x] T-001 Add `record_request` and the rolling-window counter; verifies FR-001 and AC-001.

## Phase 2: Refusal

- [ ] T-002 Add `refuse_over_limit` middleware that refuses a workspace over its
      allowance; verifies FR-002 and AC-002; blocked by T-001.
