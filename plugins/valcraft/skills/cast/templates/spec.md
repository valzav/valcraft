---
id: FEAT-001
title: <Feature name>
status: draft
spec_issue: <null | TBD | issue number>
created: <YYYY-MM-DD>
updated: <YYYY-MM-DD>
---

# <Feature name>

<!-- What and why. User-visible behavior, business rules, acceptance criteria.
     No framework names or table definitions unless they are genuine external
     constraints. Delete sections that don't apply; add the optional ones below
     only when the feature really has them. -->

## Sources

- `<canonical repo-relative PRD/plan path or canonical GitHub issue URL>`

<!-- Record the exact intake source. Use a repository-relative path for a local source,
     never an absolute path. Use this section, not a second issue field, for issue
     provenance. -->

## Summary

<One paragraph: the capability being added.>

## Problem

<The user or business problem this feature addresses.>

## Goals

- ...

## Non-goals

- ...

## User scenarios

### Scenario 1: <Name>

**Given** ... **When** ... **Then** ...

## Functional requirements

- FR-001: The system MUST ...
- FR-002: The user MUST be able to ...

## Quality requirements

<Only real ones — performance, security, access. Skip if none bind this feature.>

- NFR-001: ...

## Edge cases

<Retain only applicable cases; state required behavior precisely. Prompts: invalid
input, duplicates, concurrency, timeouts, partial completion, stale references.>

## Acceptance criteria

- [ ] AC-001: <Observable condition demonstrating success.>
- [ ] AC-002: ...

## Assumptions

- ...

## Open questions

- ...

<!-- Optional sections, add only when real: ## Business rules (BR-NNN),
     ## State model, ## Dependencies, ## Rollout constraints. -->
