---
feature: FEAT-001
status: draft
created: 2026-08-10
updated: 2026-08-10
---

# Design: Outbound webhooks

## Summary

A delivery worker reads queued events, signs each payload with the endpoint's secret, and posts it to the registered endpoint (FR-001, FR-002, FR-003).

## Data model

`webhook_endpoints(workspace_id, url, secret, enabled)` and `webhook_deliveries(id, endpoint_id, event_id, attempt, status)`.

## Failure handling

A failed delivery is requeued with backoff. The worker skips an endpoint whose `enabled` flag is false.

## Test strategy

Unit tests cover signing. Integration tests cover delivery, retry, and the disabled-endpoint path against a local receiver.
