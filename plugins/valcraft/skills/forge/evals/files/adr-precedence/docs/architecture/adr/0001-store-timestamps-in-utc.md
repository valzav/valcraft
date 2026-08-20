---
id: ADR-0001
title: Store all timestamps in UTC
status: accepted
date: 2026-07-20
---

# ADR-0001: Store all timestamps in UTC

## Context

Two incidents came from timestamps stored in a local timezone: a daylight-saving transition produced duplicate rows in one job, and a workspace that changed its timezone silently shifted every historical record.

## Decision

Every timestamp persisted by the system is stored in UTC. A local timezone is a presentation concern: it is applied when rendering a value to a member, never when storing one. Any value that a member enters in local time is converted to UTC before it is written, and the workspace timezone is stored alongside it as a separate field.

## Consequences

Storage and comparison are unambiguous, and a workspace timezone change never rewrites history. Rendering code must convert explicitly, which is a visible cost at every display site.
