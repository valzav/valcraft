# Normalize export headers

## Requirements

- FR-001: CSV export emits lowercase header names.
- AC-001: `User ID` becomes `user id` without changing cell values.

## Design

Normalize header strings in `src/export.py` immediately before serialization.

## Tasks

- [ ] QT-001 Normalize headers and add regression coverage (FR-001, AC-001)
