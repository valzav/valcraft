---
feature: FEAT-001
status: draft
created: 2026-08-03
updated: 2026-08-04
---

# Design: Bounded CSV export

## Summary

The export endpoint streams rows from the reporting database through a row limiter and
writes them to a CSV response (FR-001, FR-002).

## Interfaces

`GET /reports/{id}/export.csv` streams the CSV body.

## Failure handling

The limiter stops the stream at 5000 rows and appends a truncation notice row. A stream
that stops early returns the partial file rather than an error.
