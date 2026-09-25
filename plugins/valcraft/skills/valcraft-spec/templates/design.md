---
feature: FEAT-001
status: draft
created: <YYYY-MM-DD>
updated: <YYYY-MM-DD>
---

# Design: <Feature name>

<!-- Explain how the feature satisfies its requirements. Keep only applicable
     sections. Record consequential trade-offs, not only the chosen approach.
     Delete these comments from the generated artifact. -->

## Summary

<Technical approach, with the FR, NFR, BR, and AC IDs it satisfies.>

## Verified baseline assumptions

<One entry per existing-code fact the design depends on, checked at the exact baseline SHA: assumption, source locator, check performed, result. When a criterion needs an observation tool that a worker must drive, add the verification route: tool and version, executable, each event class the criteria need with its planted instance and the command that captured it, any class no command captured, and the harnesses that must drive it. Correct the design before readiness when a check disproves the assumption. Proposed changes do not belong here.>

## Impact on existing architecture

<Affected components, boundaries, ownership, and interfaces.>

## Data model

<Entities, keys, constraints, and migrations when applicable.>

## Interfaces

<Endpoints, commands, events, schemas, or external integrations.>

## Failure handling

<Timeouts, retries, idempotency, and partial failures when applicable.>

## Test strategy

<One entry per applicable acceptance criterion and invariant, and one per verifiable task-line obligation, listed by the task that owns it: observation method, the defect the check guards, an input under which that defect fails the check, the positive control on a correct build, and the domain: the population and free variables the criterion ranges over, and how the check covers them (complete enumeration, a derived worst-case bound, or selected cases with the derivation that the extrema lie among them). Then, per interaction or interface, the adversarial cases the checks exercise.>

## Alternatives considered

<Rejected options and why. Promote a long-lived constraint to an ADR.>

## Risks

<Risk and mitigation.>

## Open technical questions

- ...

<!-- Optional when real: Authorization; Concurrency and consistency; Security
     and privacy; Observability; Migration. -->
