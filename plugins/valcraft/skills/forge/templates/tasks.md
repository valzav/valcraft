---
feature: FEAT-001
status: draft
created: <YYYY-MM-DD>
updated: <YYYY-MM-DD>
---

# Tasks: <Feature name>

## Completion definition

The feature is complete when all applicable acceptance criteria are verified, automated
checks pass, and affected docs (specs, ADRs) are current.

<!-- Ordered, concrete, verifiable. Each task names the file, subsystem, behavior, or
     test it changes, and references the requirement or criterion it serves. Keep tasks
     small enough to review, large enough to mean progress. Tests and operational work
     belong inside the phases, not appended at the end. Note dependencies where tasks
     can't safely run in parallel. Number tasks T001… in intended order. -->

## Phase 1: <Foundation — data model, core structure>

- [ ] T001 <Task>; verifies FR-001.
- [ ] T002 <Task>; supports AC-001.

## Phase 2: <Core behavior>

- [ ] T003 <Task>; verifies FR-002.
- [ ] T004 Add unit and integration tests for <behavior>.

## Phase 3: <Surface + verification>

- [ ] T005 <UI/CLI/API surface>; verifies AC-002.
- [ ] T006 Verify every acceptance criterion; update affected docs.
