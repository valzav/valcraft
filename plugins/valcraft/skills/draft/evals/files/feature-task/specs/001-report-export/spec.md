# Report export

## Requirements

- FR-001: A user can export a report immediately.
- FR-002: A user can schedule an export for a future UTC timestamp.

## Acceptance criteria

- AC-001: An immediate export returns a CSV document.
- AC-002: A future UTC timestamp queues exactly one export and returns its
  identifier.
