---
id: FEAT-001
title: Console guard
status: draft
spec_issue: null
created: 2026-08-21
updated: 2026-08-21
---

# Console guard

## Sources

- `docs/console-guard-prd.md`

## Summary

A play session runs to completion without the app logging an uncaught error to the browser console.

## Functional requirements

- FR-001 The app must emit no uncaught console error during a play session.

## Acceptance criteria

- AC-001 A scripted session at 1280 × 720 produces zero uncaught console errors.
