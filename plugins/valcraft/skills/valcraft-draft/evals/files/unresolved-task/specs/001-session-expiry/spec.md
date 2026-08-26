# Session expiry

## Requirements

- FR-001: A session expires at its configured instant.

## Acceptance criteria

- AC-001: A write at the expiry boundary follows the defined expiry behavior.

## Open questions

- If expiry occurs while a write is in flight, does the write finish or fail?
