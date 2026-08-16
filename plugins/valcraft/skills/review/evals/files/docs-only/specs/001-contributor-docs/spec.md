---
id: FEAT-001
title: Contributor docs
status: draft
spec_issue: null
created: 2026-08-14
updated: 2026-08-14
---

# Contributor docs

## Sources

- `docs/contributor-docs-prd.md`

## Summary

The README tells a contributor how to run the project's checks.

## Functional requirements

- FR-001: `README.md` MUST state the test command declared in `AGENTS.md`, verbatim.

## Non-goals

- No new tooling; the documented command is the existing one.

## Acceptance criteria

- AC-001: Running the test command exactly as printed in `README.md` from the repository
  root passes.
