---
id: FEAT-001
title: Document search
status: draft
spec_issue: null
created: 2026-08-07
updated: 2026-08-07
---

# Document search

## Sources

- `docs/document-search-prd.md`

## Summary

A member searches documents by title and body text and opens a result.

## Functional requirements

- FR-001: A member MUST be able to search documents by title text.
- FR-002: A member MUST be able to search documents by body text.
- FR-003: Search results MUST exclude documents the member cannot read.

## Acceptance criteria

- [ ] AC-001: Searching a word in a document title returns that document.
- [ ] AC-002: Searching a word that appears only in a document body returns that document.
- [ ] AC-003: A document in a private folder the member cannot read never appears in their results.
