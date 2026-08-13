---
feature: FEAT-001
status: draft
tracker: <local | github>
spec_issue: <null | TBD | issue number>
created: <YYYY-MM-DD>
updated: <YYYY-MM-DD>
---

# Tasks: <Feature name>

## Completion definition

The feature is complete when all applicable acceptance criteria are verified, automated
checks pass, and affected docs (specs, ADRs) are current.

<!-- Render exactly one task shape throughout this file. Remove the unused shapes and
     this instruction from the generated file.

     Local (`tracker: local`, `spec_issue: null`):
     - [ ] T-001 <Task>; verifies FR-001.
     - [ ] T-002 <Task>; verifies FR-002; blocked by T-001.

     GitHub before activation (`tracker: github`, `spec_issue: TBD`):
     - T-001 <Task>; verifies FR-001. → TBD
     - T-002 <Task>; verifies FR-002; blocked by T-001. → TBD

     GitHub after activation (`tracker: github`, `spec_issue: <issue number>`):
     - T-001 <Task>; verifies FR-001. → #123
     - T-002 <Task>; verifies FR-002; blocked by T-001. → #124
-->

<!-- Keep T-IDs stable. In GitHub mode, each arrow maps a T-ID to its task issue. Use
     `TBD` until activation records the issue number. List position expresses intended
     order, not a hard dependency. Only `blocked by T-XXX` declares a dependency; never
     use an issue number there.

     Git owns task text, phases, order, and dependency intent. GitHub titles, bodies,
     sub-issue order, and blocked-by relationships are generated from this file. GitHub
     owns open/closed status and the `in-progress` and `needs-clarification` labels; never
     copy that status into this file. -->

<!-- Ordered, concrete, verifiable. Each task names the file, subsystem, behavior, or
     test it changes, and references the requirement or criterion it serves. Keep tasks
     small enough to review, large enough to mean progress. Tests and operational work
     belong inside the phases, not appended at the end. Note dependencies where tasks
     can't safely run in parallel. Number tasks T-001… in intended order. -->

## Phase 1: <Foundation — data model, core structure>

- [ ] T-001 <Task>; verifies FR-001.
- [ ] T-002 <Task>; supports AC-001.

## Phase 2: <Core behavior>

- [ ] T-003 <Task>; verifies FR-002.
- [ ] T-004 Add unit and integration tests for <behavior>.

## Phase 3: <Surface + verification>

- [ ] T-005 <UI/CLI/API surface>; verifies AC-002.
- [ ] T-006 Verify every acceptance criterion; update affected docs.
