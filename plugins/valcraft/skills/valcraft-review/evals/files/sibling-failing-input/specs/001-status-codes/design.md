---
feature: FEAT-001
status: draft
created: 2026-09-29
updated: 2026-09-29
---

# Design: Status codes

## Summary

One command-line module and a package manifest, tested with Node's built-in test runner (FR-001, NFR-001, NFR-002, AC-001, AC-002).

## Verified baseline assumptions

The baseline is the repository's root commit, which adds this design.

- VB-001, runtime. Assumption: development runs Node.js v24.19.0 with npm 11.17.0. Locator: `.nvmrc`. Check: `node --version` and `npm --version`. Result: `v24.19.0` and `11.17.0`.
- VB-002, empty baseline. Assumption: no `package.json`, `src/`, or `test/` exists, so every file below is new. Check: `git ls-files` at the baseline. Result: it lists no `package.json` and nothing under `src/` or `test/`.
- VB-003, test script. Assumption: on v24.19.0, `node --test 'test/*.test.js'` runs every matching file and exits nonzero when any test fails. Check: in a scratch package, one passing and one failing test file under `test/`, then `node --test 'test/*.test.js'`. Result: both files run, exit status 1; with the failing file removed, exit status 0.
- VB-004, supported-runtime field. Assumption: npm 11.17.0 reads `engines.node` from a package's manifest when installing it. Check: in a scratch directory, install a local package whose `engines.node` is `>=99`, first with `npm install` and then with `npm install --engine-strict`; repeat the strict install with `>=24`. Result: the plain install warns `EBADENGINE`; the strict install fails with `notsup`, reporting `Required: {"node":">=99"}` and `Actual: {"node":"v24.19.0","npm":"11.17.0"}`; with `>=24` the strict install succeeds.

## Impact on existing architecture

All files are new:

- `package.json` declares the module type, the supported Node.js versions, and the test script.
- `src/cli.js` writes the five code lines to standard output.
- `test/cli.test.js` and `test/package.test.js` hold the tests.

## Interfaces

`package.json`:

```json
{
  "name": "status-codes",
  "private": true,
  "type": "module",
  "engines": {
    "node": ">=24"
  },
  "scripts": {
    "test": "node --test 'test/*.test.js'"
  }
}
```

- `engines.node` is the manifest field npm reads for supported runtimes (VB-004); `>=24` states NFR-002's range.
- The manifest has no `dependencies`, `devDependencies`, `optionalDependencies`, or `peerDependencies` key; `node:test`, `node:assert`, and `node:child_process` ship with Node.js (NFR-001).

`src/cli.js`:

```js
const STATUSES = ['PASS', 'FAIL', 'SKIP', 'WARN', 'INFO'];

process.stdout.write(STATUSES.map((name) => `${name[0]} ${name}\n`).join(''));
```

- Command line: `node src/cli.js`. It never reads `process.argv` and leaves the exit status at 0 (FR-001).

## Failure handling

Status codes reads no input, so it has no read or parse failure. A write error on standard output is left to Node.js's default handling.

## Test strategy

Task T-001 owns every entry.

- TS-001 (AC-001, FR-001), command output.
  - Observation: `test/cli.test.js` runs `node src/cli.js` and `node src/cli.js --help extra` from the package root with `child_process.spawnSync(process.execPath, …)`. For each run it asserts exit status 0, standard error equal to the empty string, and standard output equal to the literal string `'P PASS\nF FAIL\nS SKIP\nW WARN\nI INFO\n'`.
  - Guarded defect: statuses out of order, a code other than the first letter of its status, a missing or extra line, a missing newline, output on standard error, a nonzero exit status, or output that changes when arguments are given.
  - Failing input: swapping `'PASS'` and `'FAIL'` in `STATUSES`; taking the last letter with `name.at(-1)`; joining lines with `'\n'` and dropping the final newline; prefixing a `'Statuses\n'` header; writing with `process.stderr.write`; setting `process.exitCode = 1`; printing a usage line when `process.argv` contains `--help`. Each fails the matching assertion.
  - Positive control: the design's `src/cli.js` passes both runs.
  - Domain: the whole output of each run, compared as one literal string, so each of the five lines is checked for its position, code, name, and newline; and the command line without arguments and with `--help extra`. The entry module never reads `process.argv`, so no argument reaches the output; `--help` covers the argument an implementer would most likely handle by mistake.
- TS-002 (T-001 obligation: `npm test` runs every test file directly under `test/` and fails when any test fails).
  - Observation: at T-001's head, run `npm test` on a clean checkout.
  - Guarded defect: a `test` script that runs no test file or only some of them.
  - Failing input: plant a temporary `test/planted.test.js` containing one failing assertion; `npm test` must exit nonzero, then delete the file.
  - Positive control: on a clean checkout `npm test` exits 0 and reports the tests of both shipped test files.
  - Domain: every `*.test.js` file directly under `test/`, which the script's glob matches, enumerated: the two shipped files and the planted file. The design places no test file in a subdirectory.
- TS-003 (AC-002, NFR-001), no dependencies.
  - Observation: `test/package.test.js` parses `package.json` and asserts that none of the four dependency keys is present.
  - Guarded defect: a dependency added to the manifest.
  - Failing input: add `"devDependencies": { "left-pad": "1.3.0" }`; the same edit under each of the other three keys also fails.
  - Positive control: the design's manifest passes.
  - Domain: the four dependency keys npm reads, enumerated.

Adversarial cases for the command-line interface: arguments, including `--help`, and each status checked for its own position and code so a swap cannot pass.

## Alternatives considered

- An `npm start` script was rejected because npm prints its own lines on standard output, which FR-001 forbids.

## Risks

- None beyond the test strategy.

## Open technical questions

- None.
