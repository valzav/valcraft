---
feature: FEAT-001
status: draft
created: 2026-09-29
updated: 2026-09-29
---

# Tasks: Status codes

## Completion definition

The feature is complete when every applicable acceptance criterion is verified, repository checks pass, and affected git-owned contracts are current.

## Phase 1: Command-line tool

- [ ] T-001 Build the Status codes command: the command-line entry printing the five code lines (TS-001); `package.json` whose `test` script runs every test file directly under `test/` and fails on any failing test (TS-002), that declares no dependencies and that states `engines.node` as `>=24` (TS-003); verifies FR-001, NFR-001, NFR-002, AC-001, AC-002.
