---
id: FEAT-001
title: Status codes
status: draft
spec_issue: null
created: 2026-09-29
updated: 2026-09-29
---

# Status codes

## Sources

- `docs/status-codes-prd.md`

## Summary

Status codes prints each build status's one-letter code beside the status name, one status per line.

## Problem

New operators do not know what each one-letter status code in a compact build log means.

## Goals

- Show every status code beside its status with one command.
- State the Node.js versions the package supports in its manifest.

## Non-goals

- Decoding real build logs.
- Supporting Node.js versions before 24.

## User scenarios

### Scenario 1: Show the codes

**Given** a terminal with Node.js 24 **When** the operator runs `node src/cli.js` **Then** Status codes prints `P PASS`, `F FAIL`, `S SKIP`, `W WARN`, and `I INFO` on five lines and exits with status 0.

## Functional requirements

- FR-001: Status codes MUST print exactly five lines on standard output, in the order `PASS`, `FAIL`, `SKIP`, `WARN`, `INFO`. Each line is the status's code, one space, the status name, and one newline, where a status's code is the first letter of its name. Status codes prints nothing on standard error and exits with status 0.

## Quality requirements

- NFR-001: Status codes MUST run on Node.js alone: the project declares no dependencies of any kind.
- NFR-002: The package MUST state, in the manifest field npm reads for supported runtimes, that it supports Node.js 24 and later.

## Edge cases

- Arguments are ignored; Status codes prints the same five lines with or without them.

## Acceptance criteria

- [ ] AC-001: `node src/cli.js`, with or without arguments, prints exactly the five lines of FR-001 in order, prints nothing on standard error, and exits 0.
- [ ] AC-002: The project declares no dependencies.

## Assumptions

- Operators install and run Status codes on Node.js 24 or later.

## Open questions

- None.
