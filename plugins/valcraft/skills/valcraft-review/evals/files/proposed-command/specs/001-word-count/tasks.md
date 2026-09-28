---
feature: FEAT-001
status: draft
created: 2026-09-28
updated: 2026-09-28
---

# Tasks: Word count

## Completion definition

The feature is complete when every applicable acceptance criterion is verified, repository checks pass, and affected git-owned contracts are current.

## Phase 1: Command-line tool

- [ ] T-001 Build the Tally command: `package.json` with the `start` and `test` scripts, where `npm test` runs every test file and fails on any failing test (TS-003); `countWords` (TS-001); and read-failure handling in `src/cli.js` (TS-002); verifies FR-001, FR-002, NFR-001, AC-001, AC-002.
