---
id: Q-001
created: 2026-08-10
---

# Export filename carries the export date

## Sources

- operator request, 2026-08-10

## Requirements

- FR-001: The system MUST name a downloaded export `ledger-export-<YYYY-MM-DD>.csv`.
- AC-001: Downloading an export run on 2026-08-10 yields `ledger-export-2026-08-10.csv`.

## Approach

Set the `Content-Disposition` filename in the download handler from the run's stored date; body and storage path stay untouched.

## Verification

- TS-001 (AC-001): Observation: a unit test downloads an export run stored with date 2026-08-10 while the clock reads 2026-08-11 and asserts that the `Content-Disposition` filename is `ledger-export-2026-08-10.csv`. Guarded defect: the filename built from the download date instead of the run's stored date, or a date format other than `YYYY-MM-DD`. Failing input: the run stored on 2026-08-10 downloaded on 2026-08-11; a download-date or reformatted filename fails the assertion. Positive control: the handler that formats the run's stored date passes. Domain: the filename depends only on the run's stored date; a download date that differs from the run date separates the two sources, and one date covers the fixed format.

## Tasks

- [x] QT-001 Set the download filename from the run date; verifies AC-001.
