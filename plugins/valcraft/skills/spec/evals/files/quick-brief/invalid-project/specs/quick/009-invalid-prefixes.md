---
id: Q-009
created: 2026-08-18
---

# Invalid quick grammar

## Sources

- operator request, 2026-08-18

## Requirements

- FR-001: The utility MUST reject invalid input.
- AC-001: Invalid input is rejected.

## Approach

Validate the input before processing it.

## Tasks

- [x] QT-001 Add validation; verifies AC-001.
- [ ] T-002 Add the error path; verifies AC-001.
- [ ] QT-03 Add coverage; verifies AC-001; blocked by Q-404 T-001.
- [ ] QT-004 Check an existing file target; verifies AC-001; blocked by Q-009 QT-999.
- [ ] QT-005 Check a missing file target; verifies AC-001; blocked by Q-404 QT-001.
