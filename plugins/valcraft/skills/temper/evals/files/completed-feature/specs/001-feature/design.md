---
feature: FEAT-001
status: complete
created: 2026-08-10
updated: 2026-08-14
---

# Design: Record export

## Approach

One serializer converts a stored record to an ordered field mapping, and the caller receives that mapping together with its field count. Satisfies FR-001, FR-002, AC-001, AC-002.

## Trade-offs

The serializer returns the whole record rather than a projection. A projection would need a field-selection contract that no current requirement states.
