---
feature: FEAT-001
status: draft
created: <YYYY-MM-DD>
updated: <YYYY-MM-DD>
---

# Tasks: <Feature name>

## Completion definition

The feature is complete when every applicable acceptance criterion is verified, repository checks pass, and affected git-owned contracts are current.

<!-- Read tracker.mode from .valcraft/config.yaml. Use exactly one shape throughout.

     Local:
     - [ ] T-001 <Task>; verifies FR-001.
     - [ ] T-002 <Task>; verifies FR-002; blocked by T-001.

     GitHub before projection:
     - T-001 <Task>; verifies FR-001. → TBD
     - T-002 <Task>; verifies FR-002; blocked by T-001. → TBD

     GitHub after projection:
     - T-001 <Task>; verifies FR-001. → #123
     - T-002 <Task>; verifies FR-002; blocked by T-001. → #124
-->

<!-- Keep T-IDs stable. .valcraft/config.yaml owns tracker mode. The paired spec.md owns
     the feature-issue mapping. This file owns task mappings only.

     Git owns task text, phases, order, and dependency intent. GitHub owns task
     status and discussion. List position is not a dependency. Only
     `blocked by T-XXX` declares one.

     Make every task concrete and verifiable. Name the behavior or subsystem
     it changes and the requirement or criterion it serves. Size each task as
     one reviewable slice; one file is not a reason for one task. Put tests and
     operational work with the behavior they prove, and add no task that only
     verifies other tasks' work. -->

## Phase 1: <Foundation>

- [ ] T-001 <Subsystem slice with its checks>; verifies FR-001, AC-001.

## Phase 2: <Core behavior and surface>

- [ ] T-002 <Behavior slice with its checks>; verifies FR-002, AC-002; blocked by T-001.
- [ ] T-003 <User-facing surface with its checks>; verifies FR-003, AC-003; blocked by T-002.
