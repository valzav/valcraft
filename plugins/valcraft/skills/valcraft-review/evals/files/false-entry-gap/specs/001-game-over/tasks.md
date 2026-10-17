---
feature: FEAT-001
status: draft
created: 2026-10-15
updated: 2026-10-16
---

# Tasks: Game over

## Completion definition

The feature is complete when every applicable acceptance criterion is verified, repository checks pass, and affected git-owned contracts are current.

## Phase 1: Game over

- [x] T-001 End the game when a block locks in the top row, with the `?stack=full` start board (TS-001); verifies FR-001, AC-001.
- [ ] T-002 Show the game-over panel with the final score when the game ends, and keep it hidden during play (TS-002); verifies FR-002, FR-003, AC-002, AC-003; blocked by T-001.
