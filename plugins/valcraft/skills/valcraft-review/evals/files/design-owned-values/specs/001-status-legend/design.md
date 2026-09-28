---
feature: FEAT-001
status: draft
created: 2026-09-28
updated: 2026-09-28
---

# Design: Status legend

## Summary

A palette module, a line formatter, and a command-line module, all plain ES modules, tested with Node's built-in test runner (FR-001, BR-001, NFR-001, AC-001, AC-002, AC-003).

## Verified baseline assumptions

The baseline is the repository's root commit, which adds this design.

- VB-001, runtime. Assumption: development runs Node.js v24.19.0. Locator: `.nvmrc`. Check: `node --version`. Result: `v24.19.0`.
- VB-002, empty baseline. Assumption: no `package.json`, `src/`, or `test/` exists, so every file below is new. Check: `git ls-files` at the baseline. Result: it lists no `package.json` and nothing under `src/` or `test/`.
- VB-003, test script. Assumption: on v24.19.0, `node --test 'test/*.test.js'` runs every matching file and exits nonzero when any test fails. Check: in a scratch package, one passing and one failing test file under `test/`, then `node --test 'test/*.test.js'`. Result: both files run, exit status 1; with the failing file removed, exit status 0.

## Impact on existing architecture

All files are new:

- `package.json` declares the module type and the test script.
- `src/palette.js` exports `STATUSES` and `PALETTE`.
- `src/legend.js` exports `formatLine(name, rgb)` and `legendLines()`.
- `src/cli.js` writes `legendLines()` to standard output when executed directly.
- `test/palette.test.js`, `test/legend.test.js`, `test/cli.test.js`, and `test/package.test.js` hold the tests.

## Interfaces

`package.json`:

```json
{
  "name": "legend",
  "private": true,
  "type": "module",
  "scripts": {
    "test": "node --test 'test/*.test.js'"
  }
}
```

It has no `dependencies`, `devDependencies`, `optionalDependencies`, or `peerDependencies` key; `node:test` and `node:assert` ship with Node.js (NFR-001).

- `STATUSES`: the array `['PASS', 'FAIL', 'SKIP', 'WARN', 'INFO']` (FR-001).
- `PALETTE`: an object mapping each name in `STATUSES` to an sRGB color `[r, g, b]` of integers from 0 to 255 whose five colors satisfy BR-001.
- `formatLine(name: string, rgb: [number, number, number]): string` returns `` `\x1b[38;2;${r};${g};${b}m${name}\x1b[0m\n` ``.
- `legendLines(): string` returns `STATUSES.map((name) => formatLine(name, PALETTE[name])).join('')`.
- Command line: `node src/cli.js`. When `src/cli.js` is the entry module, it calls `process.stdout.write(legendLines())` and leaves the exit status at 0. It reads no arguments.

## Color difference

BR-001's ΔE is computed as follows, and `test/palette.test.js` implements exactly this:

1. Divide each channel by 255, then linearize it: `c / 12.92` when `c <= 0.04045`, otherwise `((c + 0.055) / 1.055) ** 2.4`.
2. Convert to XYZ with the sRGB D65 matrix: `X = 0.4124564 R + 0.3575761 G + 0.1804375 B`, `Y = 0.2126729 R + 0.7151522 G + 0.0721750 B`, `Z = 0.0193339 R + 0.1191920 G + 0.9503041 B`.
3. Normalize by the D65 white point `Xn = 0.95047`, `Yn = 1.0`, `Zn = 1.08883`, and apply `f(t) = t ** (1/3)` when `t > 216/24389`, otherwise `(24389/27 * t + 16) / 116`.
4. `L = 116 f(Y/Yn) - 16`, `a = 500 (f(X/Xn) - f(Y/Yn))`, `b = 200 (f(Y/Yn) - f(Z/Zn))`.
5. ΔE is the Euclidean distance between two colors' `(L, a, b)`.

## Failure handling

Legend reads no input, so it has no read or parse failure. A write error on standard output is left to Node.js's default handling.

## Test strategy

Task T-001 owns every entry.

- TS-001 (AC-001, FR-001), legend output.
  - Observation: `test/legend.test.js` asserts that `STATUSES` deep-equals the literal array `['PASS', 'FAIL', 'SKIP', 'WARN', 'INFO']`, asserts `formatLine` on fixed inputs, and asserts `legendLines()` against the expected string built from that literal array, pairing each name with `PALETTE[name]`; `test/cli.test.js` spawns `node src/cli.js` and `node src/cli.js extra args` with `child_process.spawnSync` and asserts exit status 0, empty standard error, and standard output equal to `legendLines()`.
  - Guarded defect: a missing reset, a missing newline, the 256-color form `ESC[38;5;<n>m`, statuses out of order, a status printed with another status's color, or output on standard error.
  - Failing input: `formatLine('PASS', [1, 2, 3])` must equal `'\x1b[38;2;1;2;3mPASS\x1b[0m\n'`, which a formatter without the reset or the newline fails; swapping two entries of `STATUSES` fails the literal-array assertion; a `legendLines` that pairs a name with another status's color fails the expected string; writing with `console.error` leaves standard output empty.
  - Positive control: the design's formatter and entry pass every case.
  - Domain: the five statuses, enumerated, each checked for its position, name, and color; and the command line with and without arguments.
- TS-002 (AC-002, BR-001), distinct colors.
  - Observation: `test/palette.test.js` first asserts its conversion against reference values within 0.01 per component: `[255, 0, 0]` gives `(53.24, 80.09, 67.20)` and `[128, 128, 128]` gives `(53.59, 0.00, 0.00)`. It then asserts that every channel of every `PALETTE` color is an integer from 0 to 255, converts each color with the steps under Color difference, and asserts ΔE ≥ 25 for every pair.
  - Guarded defect: two statuses given colors closer than BR-001 allows, a conversion that departs from the Color difference steps, or a channel outside the integer range.
  - Failing input: setting `WARN` to the same color as `FAIL` gives ΔE 0 for that pair; skipping linearization gives L 76.19 for `[128, 128, 128]`; a D50 white point gives a nonzero `b` for that gray; a channel of `200.5` or `256` fails the range assertion.
  - Positive control: a palette that satisfies BR-001 passes.
  - Domain: the ten pairs of the five statuses, enumerated; the fifteen channels, enumerated; and the conversion, pinned by the two reference colors, which exercise both branches of the linearization and of `f`.
- TS-003 (T-001 obligation: `npm test` runs every test file directly under `test/` and fails when any test fails).
  - Observation: at T-001's head, run `npm test` on a clean checkout.
  - Guarded defect: a `test` script that runs no test file or only some of them.
  - Failing input: plant a temporary `test/planted.test.js` containing one failing assertion; `npm test` must exit nonzero, then delete the file.
  - Positive control: on a clean checkout `npm test` exits 0 and reports the tests of all four shipped test files.
  - Domain: every `*.test.js` file directly under `test/`, which the script's glob matches, enumerated: the four shipped files and the planted file. The design places no test file in a subdirectory.
- TS-004 (AC-003, NFR-001), no dependencies.
  - Observation: `test/package.test.js` parses `package.json` and asserts that none of the four dependency keys is present.
  - Guarded defect: a dependency added to the manifest.
  - Failing input: add `"devDependencies": { "left-pad": "1.3.0" }`.
  - Positive control: the design's manifest passes.
  - Domain: the four dependency keys npm reads, enumerated.

Adversarial cases for the command-line interface: extra arguments, and each status checked for its own position and color so a swap cannot pass.

## Alternatives considered

- A third-party color library was rejected because NFR-001 forbids dependencies and the conversion is five lines of arithmetic.
- An `npm start` script was rejected because npm prints its own lines on standard output, which FR-001 forbids.

## Risks

- None beyond the test strategy.

## Open technical questions

- None.
