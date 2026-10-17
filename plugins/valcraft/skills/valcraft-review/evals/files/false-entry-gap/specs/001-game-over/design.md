---
feature: FEAT-001
status: draft
created: 2026-10-15
updated: 2026-10-15
---

# Design: Game over

## Summary

`src/game.js` marks the state as over when a block locks in the top row (FR-001). A new `src/ui.js` shows or hides the existing game-over panel from that state (FR-002, FR-003).

## Verified baseline assumptions

The baseline is the commit that adds this design.

- VB-001, panel markup. Assumption: `index.html` already contains the panel `<div id="game-over" hidden>` with a `#final-score` element. Check: read `index.html`. Result: present, with the `hidden` attribute set.
- VB-002, panel layout. Assumption: `style.css` lays the panel out as a centered overlay. Check: read `style.css`. Result: `#game-over { display: flex; align-items: center; justify-content: center; position: absolute; inset: 0; }` is the only rule that names `#game-over`.

## Verification route

- VR-001: agent-browser 0.27.0 at `/usr/local/bin/agent-browser`, driving headless Chrome at 800 × 600 against `python3 -m http.server 8000` at the repository root. Proof: `agent-browser open http://localhost:8000/` followed by `agent-browser eval "document.title"` returned `Blockfall`.

## Impact on existing architecture

- `src/game.js` (T-001) sets `state.over` and accepts `?stack=full`, which starts the board with the stack one row below the top.
- `src/ui.js` (T-002, new) exports `render(state)`, which shows the panel with `state.score` in `#final-score` when `state.over` is true and hides it otherwise. `src/game.js` calls it after every step.
- T-002 may adjust the panel rules in `style.css`. `index.html` is unchanged.

## Test strategy

- TS-001 (AC-001, FR-001), owned by T-001, game end.
  - Observation: `test/game.test.js` builds a state with `?stack=full`'s board, steps until the falling block locks, and asserts `state.over === true`.
  - Guarded defect: the game not ending when a block locks in the top row.
  - Failing input: the top-row comparison changed from row 0 to row -1.
  - Positive control: the design's `step` passes.
  - Domain: the one board state in which the next lock reaches the top row.
- TS-002 (AC-002, AC-003, FR-002, FR-003), owned by T-002, panel visibility.
  - Observation: through VR-001, open `http://localhost:8000/` and run `agent-browser eval "document.getElementById('game-over').hidden"`; it must return `true`. Open `http://localhost:8000/?stack=full`, press Space until the game ends, and run the same eval; it must return `false`, and `agent-browser eval "document.getElementById('final-score').textContent"` must equal the text of `#score`.
  - Guarded defect: the panel visible during play, the panel not visible after the game ends, or a final score that differs from the game's score.
  - Failing input: `render` with its two branches swapped; `render` that never shows the panel; the final score written as `0`.
  - Positive control: the design's `render` passes both loads.
  - Domain: the two game phases, in progress and over, each observed once for the panel's visibility, and the final score after the game ends.

## Alternatives considered

- A modal dialog element was rejected because the existing overlay markup already fits.

## Risks

- None beyond the test strategy.

## Open technical questions

- None.
