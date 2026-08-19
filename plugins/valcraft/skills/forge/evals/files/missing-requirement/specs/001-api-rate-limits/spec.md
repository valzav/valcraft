---
id: FEAT-001
title: API rate limits
status: draft
spec_issue: null
created: 2026-08-08
updated: 2026-08-08
---

# API rate limits

## Sources

- `docs/api-rate-limits-prd.md`

## Summary

Bound each workspace's API request rate so one workspace cannot exhaust shared capacity.

## Functional requirements

- FR-001: The system MUST count API requests per workspace within a rolling window.
- FR-002: The system MUST refuse a request from a workspace that has exceeded its allowance for the current window.

## Acceptance criteria

- [ ] AC-001: Requests from a workspace are counted within the rolling window.
- [ ] AC-002: A workspace that exceeds its allowance receives a refusal rather than a normal response.
