# PRD: Activity retention windows

## Problem

Workspaces keep activity records forever. Admins in regulated industries have asked repeatedly for a way to bound how long we hold them, and we have no answer.

## What we want

An admin sets a retention window for workspace activity records, and records older than that window are removed.

The window is written the way admins already write these values elsewhere in the product: a whole number followed by a unit, such as `30d` or `12h`. Anything else is rejected rather than guessed at — silently reinterpreting a malformed window would delete data on a schedule the admin did not choose, which is the one outcome we cannot risk.

## Out of scope

- Per-record-type retention windows.
- Export or archive before deletion.
