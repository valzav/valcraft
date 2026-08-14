---
feature: FEAT-001
status: draft
created: 2026-08-07
updated: 2026-08-07
---

# Tasks: Document search

## Completion definition

The feature is complete when all applicable acceptance criteria are verified, automated
checks pass, and affected docs are current.

## Phase 1: Index

- [ ] T-001 Create the `search_documents` table and reindex hook; supports FR-001.
- [ ] T-002 Add the title query builder; verifies FR-001; blocked by T-001.

## Phase 2: Surface

- [ ] T-003 Add the `GET /search` endpoint; verifies AC-001; blocked by T-002.
- [ ] T-004 Add the readable-folder filter; verifies FR-003; blocked by T-009.

## Phase 3: Verification

- [ ] T-005 Add integration tests for AC-001 and AC-003; blocked by T-004.
