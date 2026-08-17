---
id: FEAT-001
title: Document slugs
status: draft
spec_issue: null
created: 2026-08-08
updated: 2026-08-08
---

# Document slugs

## Sources

- `docs/document-slugs-prd.md`

## Summary

Derive a readable URL slug from a document title, and reject a title that cannot produce
one.

## Functional requirements

- FR-001: The system MUST derive a lowercase hyphenated slug from a document title.
- FR-002: The system MUST reject a title that contains no usable characters, including a
  title made only of whitespace.

## Non-goals

- No usage analytics, metrics, or telemetry in this feature.
- No custom or user-edited slugs.

## Acceptance criteria

- [ ] AC-001: A title with mixed case and spacing produces a lowercase hyphenated slug.
- [ ] AC-002: A whitespace-only title is rejected and produces no document.
