---
id: FEAT-001
title: Outbound webhooks
status: draft
spec_issue: null
created: 2026-08-10
updated: 2026-08-10
---

# Outbound webhooks

## Sources

- `docs/outbound-webhooks-prd.md`

## Summary

An integrator registers an endpoint and receives signed deliveries for subscribed
workspace events.

## Functional requirements

- FR-001: An integrator MUST be able to register one HTTPS endpoint per workspace.
- FR-002: Every delivery MUST carry a signature the integrator can verify.
- FR-003: A delivery that fails MUST be retried, and MUST stop after the endpoint is
  disabled.

## Acceptance criteria

- [ ] AC-001: A registered endpoint receives a signed delivery for a subscribed event.
- [ ] AC-002: A delivery to a failing endpoint is retried and recorded.
- [ ] AC-003: A disabled endpoint receives no further deliveries.
