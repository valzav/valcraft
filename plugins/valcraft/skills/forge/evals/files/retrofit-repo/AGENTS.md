# Agent notes

- Install with `npm install`, test with `npm test`, lint with `npm run lint`.
- Source lives in `src/`, tests in `test/`.
- Never call the SQLite database directly from command handlers — go through
  `src/store.js`.
