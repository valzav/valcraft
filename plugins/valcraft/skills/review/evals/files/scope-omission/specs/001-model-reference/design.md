---
feature: FEAT-001
status: complete
created: 2026-08-10
updated: 2026-08-12
---

# Design: Provider model reference

## Summary

Configuration loading produces one validated model reference that the provider client consumes (FR-001, FR-002).

## Data shape

A model reference is the tuple `{provider, model, base_url, api_key_env}`. All four fields are required strings and the tuple carries nothing else. The loader resolves `api_key_env` against the process environment at startup and fails fast when the variable is unset.

## Interfaces

`load_model_reference(path)` reads the configuration file and returns the validated tuple. The provider client accepts the tuple and owns the HTTP session.
