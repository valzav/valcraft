---
feature: FEAT-001
status: draft
created: 2026-08-09
updated: 2026-08-09
---

# Design: Daily activity digest

## Summary

`set_send_time` stores the workspace's configured digest send time (FR-001). The digest
scheduler reads it each hour and queues digests for workspaces whose send time has
arrived (FR-002).

## Data model

`workspace_digest_settings(workspace_id, send_at, timezone)`.

Store `send_at` as the workspace's local wall-clock time, in the workspace's own
timezone, so the admin sees back exactly the value they entered. The scheduler converts
each workspace's local send time to the current instant when it runs.

## Interfaces

- `set_send_time(workspace_id, send_at, timezone)` in `src/digest_settings.py`.
- `due_workspaces(now)` in `src/digest_scheduler.py`.

## Test strategy

Unit tests cover storing a send time and selecting due workspaces across two timezones.
