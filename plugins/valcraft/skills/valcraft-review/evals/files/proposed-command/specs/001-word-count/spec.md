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

## User scenarios

### Scenario 1: Count a draft

**Given** a text file `draft.txt` containing `The quick  brown fox` **When** the writer runs `node src/cli.js draft.txt` **Then** Tally prints `4` and exits with status 0.

### Scenario 2: Mistyped path

**Given** no file named `drat.txt` exists **When** the writer runs `node src/cli.js drat.txt` **Then** Tally prints an error naming `drat.txt` on standard error, prints nothing on standard output, and exits with status 2.

## Functional requirements

- FR-001: Tally MUST print the number of words in the named file as a decimal integer followed by one newline on standard output, print nothing on standard error, and exit with status 0. A word is a maximal run of characters other than the four separators: space, tab, newline, and carriage return. Every other character belongs to a word.
- FR-002: When the named file cannot be read, for any reason, Tally MUST print exactly one line on standard error that names the path, print nothing on standard output, and exit with status 2.

## Quality requirements

- NFR-001: Tally MUST run on Node.js alone: the project declares no dependencies of any kind.

## Edge cases

- An empty file and a file of only separators both count 0, printed as `0`.
- Leading, trailing, and repeated separators do not create words.
- Other whitespace, such as a form feed, a vertical tab, or a no-break space, is a word character.
- A path that names a directory, or that passes through a regular file as if it were a directory, cannot be read and follows FR-002.
- A path containing a newline still produces exactly one line on standard error.

## Acceptance criteria

- [ ] AC-001: For a file with zero words, a file with several words split by each of the four separators, and a file whose words contain other whitespace and punctuation, Tally prints the correct count and one newline on standard output, nothing on standard error, and exits 0.
- [ ] AC-002: For a missing path, a directory path, a path through a regular file, a path containing a newline, and any other read failure, Tally prints exactly one line naming the path on standard error, nothing on standard output, and exits 2.
- [ ] AC-003: The project declares no dependencies.

## Assumptions

- Input files are UTF-8 text small enough to read into memory at once.

## Open questions

- None.
