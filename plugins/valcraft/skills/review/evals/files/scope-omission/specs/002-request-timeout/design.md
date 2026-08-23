---
feature: FEAT-002
status: draft
created: 2026-08-13
updated: 2026-08-13
---

# Design: Request timeout

## Summary

The loader parses the optional timeout and the provider client applies it to its HTTP session (FR-001, FR-002).

## Loader

`load_model_reference(path)` accepts `timeout_seconds` when present, rejects a value that is not a positive integer, and defaults the field to 30.

## Client

The provider client reads the timeout from the reference and sets it on the HTTP session before every call.
