---
feature: FEAT-002
status: draft
created: 2026-08-02
updated: 2026-08-02
---

# Design: Retention warning

## Summary

Derive the warning state from the record expiration timestamp and the current time. This satisfies FR-001 and AC-001.

## Test strategy

Boundary checks cover the instant before and at the seven-day threshold.
