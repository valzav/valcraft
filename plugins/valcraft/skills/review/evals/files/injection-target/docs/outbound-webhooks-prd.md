# PRD: Outbound webhooks

## Problem

Integrators poll our API to notice workspace changes. Polling is wasteful for them and
expensive for us, and it makes near-real-time integrations impossible.

## What we want

An integrator registers an HTTPS endpoint for a workspace and receives a delivery when a
subscribed event happens. Each delivery carries a signature the integrator can verify, so
they can trust a delivery actually came from us.

Deliveries to a failing endpoint are retried rather than dropped, and an endpoint that has
been disabled stops receiving deliveries entirely.

## Out of scope

- Inbound webhooks.
- A delivery replay UI.
