---
feature: FEAT-001
status: draft
created: 2026-09-28
updated: 2026-09-28
---

# Design: Word count

## Summary

A `countWords` function and a command-line module, both plain ES modules, tested with Node's built-in test runner (FR-001, FR-002, NFR-001, AC-001, AC-002, AC-003).

## Verified baseline assumptions

The baseline is the repository's root commit, which adds this design.

- VB-001, runtime. Assumption: development and CI run Node.js v24.19.0. Locator: `.nvmrc`. Check: `node --version`. Result: `v24.19.0`.
- VB-002, empty baseline. Assumption: no `package.json`, `src/`, or `test/` exists, so every file below is new. Check: `git ls-files` at the baseline. Result: it lists no `package.json` and nothing under `src/` or `test/`.

## Impact on existing architecture

All files are new:

- `package.json` declares the module type and the test script.
- `src/count.js` exports `countWords(text)`.
- `src/cli.js` exports `run(args, io)` and, when executed directly, calls it with the real process streams.
- `test/count.test.js`, `test/cli.test.js`, and `test/package.test.js` hold the tests.

## Interfaces

`package.json`:

```json
{
  "name": "tally",
  "private": true,
  "type": "module",
  "scripts": {
    "test": "node --test test/"
  }
}
```

It has no `dependencies`, `devDependencies`, `optionalDependencies`, or `peerDependencies` key; `node:test` and `node:assert` ship with Node.js (NFR-001).

- `countWords(text: string): number` splits on `/[ \t\n\r]+/` and counts the non-empty pieces.
- `run(args: string[], io: { readFile(path): string, stdout: { write(s) }, stderr: { write(s) } }): number` reads `args[0]` with `io.readFile`, writes the count and one newline to `io.stdout`, and returns 0.
- Command line: `node src/cli.js <path>`. When `src/cli.js` is the entry module, it calls `run(process.argv.slice(2), …)` with `readFileSync(path, 'utf8')` and the process streams, and sets `process.exitCode` to the result.

## Failure handling

`run` wraps `io.readFile(path)` in one `try`. Its `catch` does not inspect the error: every read error writes `tally: cannot read ` followed by `JSON.stringify(path)` and one newline to `io.stderr`, and returns 2 (FR-002). `JSON.stringify` escapes a newline in the path, so the message stays on one line.

## Test strategy

Task T-001 owns every entry.

- TS-001 (AC-001, FR-001), word counting.
  - Observation: `test/count.test.js` asserts `countWords` over a case table.
  - Guarded defect: splitting on the space character alone, counting empty pieces, or splitting on a wider whitespace class such as `/\s+/`.
  - Failing input: `text.split(' ').length` returns 1 for `""` and 1 for `"a\tb\nc"`; `/\s+/` returns 2 for `"a\fb"`.
  - Positive control: the design's split passes every case.
  - Domain: strings over separators and word characters. The count depends only on whether each character is one of the four separators and where the separators sit relative to words. The cases therefore place each separator at the start, between two words, at the end, and in runs, and put each class of non-separator whitespace and punctuation between two word characters: `""`, `" "`, `"\t\n\r "`, `"one"`, `"one two"`, `"a\tb"`, `"a\nb"`, `"a\rb"`, `"  lead"`, `"trail  "`, `"a   b\t\tc"`, `"a\fb"`, `"a\vb"`, `"a b"`, `"a b"`, `"a,b"`, `"a-b"`. A character outside these classes is either one of the four separators or a word character like `a`, so it adds no new case.
- TS-002 (AC-001, AC-002, FR-001, FR-002), command-line output.
  - Observation: `test/cli.test.js` spawns `node src/cli.js` with `child_process.spawnSync` on temporary files and paths, and calls `run` directly with an injected `readFile`. Each case asserts exit status, standard output, and standard error exactly.
  - Guarded defect: a count printed without its newline, a zero count suppressed by a truthiness test, output on the wrong stream, an unhandled read error, an error handler that branches on error codes, or a path printed raw.
  - Failing input: removing the `try` makes the missing-path case exit 1; `if (n) write(n + '\n')` prints nothing for the empty file; handling only `ENOENT` and `EISDIR` fails the not-a-directory and injected cases; interpolating the raw path writes two lines for the newline path.
  - Positive control: the design's `run` passes every case.
  - Domain: success over three files, enumerated: empty (`0\n`), `one two` (`2\n`), and `a\fb c` (`2\n`). Failure over the constructible read errors, enumerated: a missing path, a directory, a path through a regular file (`ENOTDIR`), and a missing path containing a newline. The injected `readFile` throws an error with code `EINJECTED`, which no real read produces, so a handler that lists codes fails it; that covers FR-002's "any reason".
- TS-003 (T-001 obligation: `npm test` runs every test file and fails when any test fails).
  - Observation: at T-001's head, run `npm test` on a clean checkout.
  - Guarded defect: a `test` script that runs no test file or only some of them.
  - Failing input: plant a temporary `test/planted.test.js` containing one failing assertion; `npm test` must exit nonzero, then delete the file.
  - Positive control: on a clean checkout `npm test` exits 0 and reports the tests of all three shipped test files.
  - Domain: every `*.test.js` file under `test/`, enumerated: the three shipped files and the planted file.
- TS-004 (AC-003, NFR-001), no dependencies.
  - Observation: `test/package.test.js` parses `package.json` and asserts that none of the four dependency keys is present.
  - Guarded defect: a dependency added to the manifest.
  - Failing input: add `"devDependencies": { "left-pad": "1.3.0" }`.
  - Positive control: the design's manifest passes.
  - Domain: the four dependency keys npm reads, enumerated.

Adversarial cases for the command-line interface: an empty file, a separators-only file, other whitespace inside words, a missing path, a directory path, a path through a regular file, a path containing a newline, and an unknown read error.

## Alternatives considered

- A third-party test framework was rejected because `node:test` ships with Node.js and NFR-001 forbids dependencies.
- An `npm start` script was rejected because npm prints its own lines on standard output, which FR-001 and FR-002 forbid.

## Risks

- None beyond the test strategy.

## Open technical questions

- None.
