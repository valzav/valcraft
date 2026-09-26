---
id: Q-001
created: <YYYY-MM-DD>
---

# <Title — the change in one line>

<!-- One file is the complete quick-task contract. Follow
     ../references/quick.md. Delete these comments from the generated file. -->

## Sources

- <repository-relative path | canonical issue URL | operator request, YYYY-MM-DD>

## Requirements

<!-- Requirements use FR-; observable acceptance criteria use AC-. Both restart
     at 001 in each quick file. -->

- FR-001: The system MUST ...
- AC-001: <Observable condition demonstrating success.>

## Approach

<!-- State intended behavior, mechanism, touched scope, and untouched scope. Link
     to docs/status.md instead of copying mutable environment observations. -->

...

## Verification

<!-- One Test strategy entry per AC-, as feature-contract.md defines it. TS- IDs
     restart in each quick file. The failing input must be constructible at the
     head of the QT- task that verifies the criterion. -->

- TS-001 (AC-001): Observation: <method a worker drives>. Guarded defect: <the mistake an implementer could make>. Failing input: <input under which that defect makes the check fail>. Positive control: <the check passing on a correct build>. Domain: <what the criterion ranges over and how the check covers it>.

## Tasks

<!-- Checkbox status is authoritative in every tracker mode. Cite a task as
     `Q-001 QT-001`. Use `blocked by QT-XXX` locally or
     `blocked by Q-NNN QT-XXX` across quick files. -->

- [ ] QT-001 <Task>; verifies AC-001.

## Open questions

<!-- Delete when empty. A behavior-changing question blocks readiness unless the
     operator explicitly accepts the uncertainty here. -->

- ...
