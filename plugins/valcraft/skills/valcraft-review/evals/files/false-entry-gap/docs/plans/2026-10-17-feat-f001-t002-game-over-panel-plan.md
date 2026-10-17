# FEAT-001 T-002 game-over panel plan

## Task

FEAT-001 T-002: show the game-over panel with the final score when the game ends, and keep it hidden during play. Authorities: `specs/001-game-over/spec.md`, `design.md`, and `tasks.md`. T-001 is complete at the baseline.

## Contract

FR-002, FR-003, AC-002, and AC-003. Preserve FR-001 and TS-001.

## Scope

- Touched: `src/ui.js` (new), `src/game.js` (call `render` after each step), and `style.css`.
- Untouched: `index.html` and `test/game.test.js`.
- Documents: `grep -rn "game-over\|Game over" README.md AGENTS.md docs/` at the baseline finds only the PRD, which the task does not make false.

## Implementation

1. Add `src/ui.js` exporting `render(state)`. It sets `document.getElementById('game-over').hidden = !state.over` and, when `state.over` is true, writes `String(state.score)` to `#final-score`.
2. In `src/game.js`, call `render(state)` after each `step` in the keydown handler and once after `createState`.
3. In `style.css`, add `#game-over[hidden] { display: none; }` after the existing `#game-over` rule, because that rule's `display: flex` overrides the browser's default `[hidden]` rule.

## Verification

- AC-002, AC-003, FR-002, and FR-003: TS-002.
- TS-002's gap: the entry reads the `hidden` property, which stays `true` while `#game-over { display: flex; }` keeps the panel rendered. Addition: at each TS-002 read, also run `agent-browser eval "getComputedStyle(document.getElementById('game-over')).display"` and the same for `visibility`. During play, `display` must be `none`. After the game ends, `display` must not be `none` and `visibility` must be `visible`. Failing input for the addition: step 3 reverted; the during-play read then returns `flex`.
- FR-001 is preserved: `node --test` passes TS-001.

## Open decisions

- None.
