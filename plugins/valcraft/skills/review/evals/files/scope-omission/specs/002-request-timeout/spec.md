---
id: FEAT-002
title: Request timeout
status: draft
spec_issue: null
created: 2026-08-13
updated: 2026-08-13
---

# Request timeout

## Sources

- `docs/request-timeout-prd.md`

## Summary

An operator bounds how long a provider call may run. The bound is configured per model reference.

## Functional requirements

- FR-001: The model reference MUST accept an optional `timeout_seconds` field holding a positive whole number of seconds.
- FR-002: When `timeout_seconds` is absent the service MUST use 30 seconds.

## Acceptance criteria

- [ ] AC-001: A reference with `timeout_seconds: 5` aborts a provider call that has not answered after 5 seconds.
- [ ] AC-002: A reference without `timeout_seconds` aborts a provider call that has not answered after 30 seconds.
- [ ] AC-003: A reference with a non-positive or non-integer `timeout_seconds` fails startup with a message naming the field.
