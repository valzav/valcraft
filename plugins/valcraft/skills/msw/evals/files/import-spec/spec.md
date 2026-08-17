# Spec: bulk row import

## Goal

Users upload a CSV of rows; the system validates and inserts them, reporting per-row
failures.

## Functional requirements

- FR-001: Accept a CSV upload and insert each valid row.
- FR-002: Report each invalid row with its line number and reason.
- FR-003: The whole import must finish within 30 seconds — the platform gateway times
  out requests at 30 s.
- FR-004: Retry each failed row at most 3 times.
- FR-005: Reject files larger than 5 MB.

## Authoring rules

- Keep functional requirements to no more than 10 per spec.
