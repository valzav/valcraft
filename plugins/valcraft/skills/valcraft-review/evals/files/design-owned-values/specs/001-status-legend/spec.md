---
id: FEAT-001
title: Status legend
status: draft
spec_issue: null
created: 2026-09-28
updated: 2026-09-28
---

# Status legend

## Sources

- `docs/legend-prd.md`

## Summary

Legend prints the five build statuses, each in its own color, one per line.

## Problem

Operators misread build statuses whose colors look alike.

## Goals

- Show every status in its assigned color with one command.
- Keep every pair of status colors clearly distinct.

## Non-goals

- Coloring real build output.
- Terminals without 24-bit color.

## User scenarios

### Scenario 1: Show the legend

**Given** a 24-bit color terminal **When** the operator runs `node src/cli.js` **Then** Legend prints `PASS`, `FAIL`, `SKIP`, `WARN`, and `INFO` on five lines, each in its color, and exits with status 0.

## Functional requirements

- FR-001: Legend MUST print exactly five lines on standard output, in the order `PASS`, `FAIL`, `SKIP`, `WARN`, `INFO`. Each line is `ESC[38;2;<r>;<g>;<b>m`, the status name, `ESC[0m`, and one newline, where `<r>`, `<g>`, and `<b>` are the decimal channels of that status's color and `ESC` is the byte 0x1B. Legend prints nothing on standard error and exits with status 0.

## Business rules

- BR-001: Every pair of the five status colors is at least 25 apart in CIE76 ΔE, computed in CIELAB from sRGB with a D65 white point. Source: operator decision, 2026-09-28.

## Quality requirements

- NFR-001: Legend MUST run on Node.js alone: the project declares no dependencies of any kind.

## Edge cases

- Arguments are ignored; Legend prints the same five lines with or without them.

## Acceptance criteria

- [ ] AC-001: `node src/cli.js` prints the five lines of FR-001 exactly, in order, with each status's color, prints nothing on standard error, and exits 0.
- [ ] AC-002: Every pair of the five status colors satisfies BR-001.
- [ ] AC-003: The project declares no dependencies.

## Assumptions

- The operator's terminal renders 24-bit foreground color escapes.

## Open questions

- None.
