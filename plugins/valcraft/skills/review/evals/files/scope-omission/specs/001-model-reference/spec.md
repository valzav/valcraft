---
id: FEAT-001
title: Provider model reference
status: complete
spec_issue: null
created: 2026-08-10
updated: 2026-08-12
---

# Provider model reference

## Sources

- `docs/model-reference-prd.md`

## Summary

An operator configures which provider and model the service calls. The reference is loaded from configuration and validated before the service accepts traffic.

## Functional requirements

- FR-001: The configuration MUST accept a model reference naming the provider, the model, the base URL, and the environment variable holding the API key.
- FR-002: The service MUST reject a reference whose API key environment variable is unset at startup.

## Acceptance criteria

- [x] AC-001: A reference with all four fields loads and the service starts.
- [x] AC-002: A reference whose API key variable is unset fails startup with a message naming the variable.
