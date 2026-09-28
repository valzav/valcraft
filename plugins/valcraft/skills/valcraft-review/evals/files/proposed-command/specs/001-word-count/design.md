---
feature: FEAT-001
status: draft
created: 2026-09-28
updated: 2026-09-28
---

# Design: Word count

## Summary

A pure `countWords` function and a thin command-line wrapper, both plain ES modules, tested with Node's built-in test runner (FR-001, FR-002, NFR-001, AC-001, AC-002).

## Verified baseline assumptions

- VB-001, runtime. Assumption: development and CI run Node.js v24.19.0. Locator: `.nvmrc`. Check: `node --version` at the baseline commit. Result: `v24.19.0`.
- VB-002, empty baseline. Assumption: the baseline has no `package.json`, `src/`, or `test/`, so every file below is new. Check: `git ls-files` at the baseline commit. Result: only `AGENTS.md`, `.gitignore`, `.nvmrc`, `.valcraft/config.yaml`, `docs/`, and `specs/`.

## Impact on existing architecture

All files are new:

- `package.json` declares the module type and the scripts.
- `src/count.js` exports `countWords(text)`.
- `src/cli.js` reads the file named by the first argument, prints the count, and handles read failures.
- `test/count.test.js` and `test/cli.test.js` hold the tests.

## Interfaces

`package.json`:

```json
{
  "name": "tally",
  "private": true,
  "type": "module",
  "scripts": {
    "start": "node src/cli.js",
    "test": "node --test test/"
  }
}
```

It declares no dependencies; `node:test` and `node:assert` ship with Node.js (NFR-001).

- `countWords(text: string): number` splits on the four separators FR-001 names and counts the non-empty pieces.
- Command line: `node src/cli.js <path>` or `npm start -- <path>`.

## Failure handling

`src/cli.js` wraps `readFileSync(path, 'utf8')` in a `try`. Any read error, including `ENOENT` and `EISDIR`, prints `tally: cannot read <path>` on standard error and sets `process.exitCode = 2` (FR-002).

## Test strategy

Task T-001 owns every entry.

- TS-001 (AC-001, FR-001), word counting.
  - Observation: `test/count.test.js` asserts `countWords` over a case table.
  - Guarded defect: splitting on the space character alone, or counting empty pieces between separators.
  - Failing input: `text.split(' ').length`, which returns 1 for `""` and 1 for `"a\tb\nc"`.
  - Positive control: a split on `/[ \t\n\r]+/` that drops empty pieces passes every case.
  - Domain: strings over word characters and the four separators. The count depends only on each separator's class and position relative to words, so the selected cases place each separator class at the start, between two words, at the end, and in runs of two or more: `""`, `" "`, `"\t\n\r "`, `"one"`, `"one two"`, `"a\tb"`, `"a\nb"`, `"a\rb"`, `"  lead"`, `"trail  "`, `"a   b\t\tc"`.
- TS-002 (AC-002, FR-002), unreadable path.
  - Observation: `test/cli.test.js` spawns `node src/cli.js` with `child_process.spawnSync` and asserts exit status, standard output, and standard error.
  - Guarded defect: an unhandled read error, which exits 1 with a stack trace.
  - Failing input: removing the `try`, so a missing path exits 1.
  - Positive control: a temporary file containing `one two` exits 0 and prints `2`.
  - Domain: the two read failures the spec names, enumerated: a path that does not exist and a path that names a directory.
- TS-003 (T-001 obligation: `npm test` runs every test file and fails when any test fails).
  - Observation: at T-001's head, run `npm test` on a clean checkout.
  - Guarded defect: a `test` script that runs no test file or only some of them.
  - Failing input: plant a temporary `test/planted.test.js` containing one failing assertion; `npm test` must exit nonzero, then delete the file.
  - Positive control: on a clean checkout `npm test` exits 0 and reports the tests of both `test/count.test.js` and `test/cli.test.js`.
  - Domain: every `*.test.js` file under `test/`, enumerated: the two shipped files and the planted file.

Adversarial cases for the command-line interface: an empty file, a whitespace-only file, a missing path, and a directory path.

## Alternatives considered

- A third-party test framework was rejected because `node:test` ships with Node.js and NFR-001 forbids installed dependencies.

## Risks

- None beyond the test strategy.

## Open technical questions

- None.
