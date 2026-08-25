---
id: Q-001
created: 2026-08-10
---

# Export filename carries the export date

## Sources

- operator request, 2026-08-10

## Requirements

- FR-001: The system MUST name a downloaded export `ledger-export-<YYYY-MM-DD>.csv`, using the export's run date.
- AC-001: Downloading an export run on 2026-08-10 yields `ledger-export-2026-08-10.csv`.

## Approach

Set the `Content-Disposition` filename in the download handler from the run's stored date; the export body and storage path stay untouched.

## Tasks

- [x] QT-001 Set the download filename from the run date; verifies AC-001.
