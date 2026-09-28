---
id: FEAT-001
title: Word count
status: draft
spec_issue: null
created: 2026-09-28
updated: 2026-09-28
---

# Word count

## Sources

- `docs/tally-prd.md`

## Summary

Tally reads one plain-text file named on the command line and prints its word count.

## Problem

Writers want a word count for a draft without opening an editor.

## Goals

- Print a file's word count with one command.
- Report an unreadable file clearly, with a distinct exit status.

## Non-goals

- Counting characters, lines, or sentences.
- Reading from standard input or from more than one file.
- Unicode whitespace beyond the four characters FR-001 names.

## User scenarios

### Scenario 1: Count a draft

**Given** a text file `draft.txt` containing `The quick  brown fox` **When** the writer runs Tally with `draft.txt` **Then** Tally prints `4` and exits with status 0.

### Scenario 2: Mistyped path

**Given** no file named `drat.txt` exists **When** the writer runs Tally with `drat.txt` **Then** Tally prints an error naming `drat.txt` on standard error, prints nothing on standard output, and exits with status 2.

## Functional requirements

- FR-001: Tally MUST print the number of words in the named file as a decimal integer followed by a newline on standard output, and exit with status 0. A word is a maximal run of characters other than space, tab, newline, and carriage return.
- FR-002: When the named file cannot be read, Tally MUST print one line naming the path on standard error, print nothing on standard output, and exit with status 2.

## Quality requirements

- NFR-001: Tally MUST run on Node.js alone, with no installed dependencies.

## Edge cases

- An empty file and a file of only whitespace both count 0.
- Leading, trailing, and repeated separators do not create words.
- A path that names a directory cannot be read as a file and follows FR-002.

## Acceptance criteria

- [ ] AC-001: For each whitespace-separated input in TS-001's domain, Tally prints the correct count and exits 0.
- [ ] AC-002: For a missing path and for a directory path, Tally prints one line naming the path on standard error, nothing on standard output, and exits 2.

## Assumptions

- Input files are UTF-8 text small enough to read into memory at once.

## Open questions

- None.
