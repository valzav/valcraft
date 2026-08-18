---
id: Q-002
created: 2026-08-15
---

# Failed export shows a retry button

## Sources

- operator request, 2026-08-15

## Requirements

- FR-001: A failed export run MUST show a "Retry" action on the exports page.
- AC-001: An administrator viewing a failed run sees a "Retry" button next to its status.
- AC-002: Pressing "Retry" starts a new run with the failed run's parameters and the
  new run appears at the top of the list.

## Approach

Render the button in the run-status cell of the exports table when the run's status is
`failed`; the click posts to the existing "run export" endpoint with the failed run's
stored parameters. No new endpoint; the export job itself is untouched.

## Tasks

- [ ] QT-001 Render the "Retry" button for failed runs; verifies AC-001.
