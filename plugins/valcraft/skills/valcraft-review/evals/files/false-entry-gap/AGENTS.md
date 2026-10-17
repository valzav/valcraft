# Agent instructions

## Orientation

- `docs/` contains product context, the requirements source, and task plans.
- `specs/` contains canonical feature specifications.
- The project is Blockfall, a static browser game: `index.html`, `style.css`, and ES modules under `src/`, with no build step and no dependencies. Node's built-in test runner runs `test/`.

On conflict, accepted ADRs prevail, then `specs/`, then derived `docs/`.
