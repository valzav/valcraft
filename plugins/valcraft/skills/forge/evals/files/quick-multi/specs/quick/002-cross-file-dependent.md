---
id: Q-002
created: 2026-08-18
---

# Cross-file dependent validation

## Sources

- operator request, 2026-08-18

## Requirements

- FR-001: Validation MUST expose the completed hardening result.
- AC-001: The completed whitespace validation is available to callers.

## Approach

Expose the existing validated result without changing validation behavior.

## Tasks

- [ ] QT-001 Expose the validated result; verifies AC-001; blocked by Q-001 QT-001.
