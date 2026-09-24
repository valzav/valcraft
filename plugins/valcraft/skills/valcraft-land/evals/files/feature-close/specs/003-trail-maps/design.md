---
feature: FEAT-003
status: draft
created: 2026-09-01
updated: 2026-09-01
---

# Design: Trail maps

## Architecture

The trail page loads the stored GPX track, renders it with the map component, and computes the elevation profile from the track points (FR-001 to FR-003).

## Test strategy

- AC-001: a browser test selects the first trail and asserts the map route loads.
- AC-002: a component test counts the drawn track points and both markers.
- AC-003: a browser probe records the time from navigation to the profile's first paint.
