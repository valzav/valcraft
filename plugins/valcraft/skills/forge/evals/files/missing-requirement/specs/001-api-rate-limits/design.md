---
feature: FEAT-001
status: draft
created: 2026-08-08
updated: 2026-08-08
---

# Design: API rate limits

## Summary

A counter keyed by workspace id tracks requests inside a rolling window (FR-001). The
request middleware reads the counter before dispatch and refuses the request when the
workspace is over its allowance (FR-002).

## Data model

`rate_counters(workspace_id, window_start, count)`, incremented on each accepted request
and reset when the window rolls over.

## Interfaces

- `record_request(workspace_id) -> int` in `src/rate_limits.py` returns the new count for
  the current window.
- `refuse_over_limit(workspace_id)` in `src/middleware.py` runs before dispatch.

## Failure handling

A counter store outage fails open: the request is dispatched and the outage is logged.

## Test strategy

Unit tests cover counting and window rollover. Integration tests cover the middleware
path for an allowed request and a refused one.
