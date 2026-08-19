---
feature: FEAT-001
status: draft
created: <YYYY-MM-DD>
updated: <YYYY-MM-DD>
---

# Tasks: <Feature name>

## Completion definition

The feature is complete when every applicable acceptance criterion is verified,
repository checks pass, and affected git-owned contracts are current.

<!-- Read project_tracker from root AGENTS.md. Use exactly one shape throughout.

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

<!-- Keep T-IDs stable. Root AGENTS.md owns tracker mode. The paired spec.md owns
     the feature-issue mapping. This file owns task mappings only.

     Git owns task text, phases, order, and dependency intent. GitHub owns task
     status and discussion. List position is not a dependency. Only
     `blocked by T-XXX` declares one.

     Make every task concrete and verifiable. Name the behavior, file, or
     subsystem it changes and the requirement or criterion it serves. Put tests
     and operational work with the behavior they prove. -->

## Phase 1: <Foundation>

- [ ] T-001 <Task>; verifies FR-001.
- [ ] T-002 <Task>; supports AC-001.

## Phase 2: <Core behavior>

- [ ] T-003 <Task>; verifies FR-002.
- [ ] T-004 Add discriminating checks for <behavior>.

## Phase 3: <Surface and verification>

- [ ] T-005 <User-facing surface>; verifies AC-002.
- [ ] T-006 Verify every acceptance criterion and update affected contracts.
