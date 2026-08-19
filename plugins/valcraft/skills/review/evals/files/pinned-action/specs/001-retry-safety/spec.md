# Retry safety

## Requirements

- **FR-001:** A retry workflow must preserve the queued item when an optional action mode is omitted.

## Acceptance criteria

- **AC-001:** Running the workflow without a `mode` input reports `safe: queued item preserved`.
