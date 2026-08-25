# Spec: log ingestion endpoint

## Goal

Services POST log batches; the endpoint validates and enqueues them.

## Functional requirements

- FR-001: Accept a JSON batch of log records and enqueue each valid record.
- FR-002: Reject a batch that exceeds the maximum batch size with HTTP 413. The ingestion buffer is fixed-size, so a maximum batch size is required — the exact value has not been decided yet; 500 records below is a placeholder nobody approved.
- FR-003: The maximum batch size is 500 records.
