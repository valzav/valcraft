---
id: FEAT-001
title: Game over
status: draft
spec_issue: null
created: 2026-10-15
updated: 2026-10-15
---

# Game over

## Sources

- `docs/game-over-prd.md`

## Summary

The game ends when a block locks in the top row, and a game-over panel shows the final score.

## Functional requirements

- FR-001 The game must end when a block locks in the top row.
- FR-002 The game-over panel must not be visible while a game is in progress.
- FR-003 When the game ends, the game-over panel must be visible and show the final score.

## Acceptance criteria

- AC-001 With the stack one row below the top, the next block that locks ends the game.
- AC-002 At 800 × 600, the game-over panel is not visible during play.
- AC-003 At 800 × 600, after the game ends, the game-over panel is visible and its final score equals the game's score.

## Edge cases

- None beyond the acceptance criteria.
