---
feature: FEAT-001
status: draft
created: 2026-08-07
updated: 2026-08-07
---

# Design: Document search

## Summary

A search index stores one row per document with its title, body text, and folder id. A
query matches the indexed text and filters results by the caller's readable folder ids
(FR-001, FR-002, FR-003).

## Data model

`search_documents(document_id, folder_id, title_text, body_text)`, reindexed when a
document is saved.

## Interfaces

`GET /search?q=` returns ranked document summaries.

## Test strategy

Unit tests cover the query builder. Integration tests cover the endpoint against a
seeded index.
