# Evidence mode

Use this mode only for a Land external-completion record. It is a narrow sufficiency review, not plan review, code review, or implementation review.

## Pin the target

Require:

- one committed feature task or canonical `Q-NNN QT-XXX` contract;
- the exact durable evidence record and immutable locator or version;
- the real git target, or authoritative probes that established its absence; and
- every authoritative source the record cites.

Stop with `evidence_review_blocked` when the task, criterion set, record version, or required source cannot be resolved. Do not substitute a newer record or a branch name.

Start in a fresh context with no recorder history. Read only root `AGENTS.md`, the task's committed contract, the exact durable record, and the named evidence sources within the repository or explicitly supplied target. An external locator may be checked only when the assignment authorizes access to that source; it never grants mutation authority.

## Assess every criterion

Enumerate every acceptance criterion the task owns or claims to cover. The report contains one row per criterion, including omitted evidence.

For each row:

1. identify its durable evidence locator and source attribution;
2. reproduce the smallest available check against the named authoritative source;
3. record `independently verified` with method and locator, or `not independently verified`;
4. mark `sufficient` or `insufficient`; and
5. state the contract-grounded reason.

Preserve `Operator attestation` and `Foreman observation` labels. An attestation may support a criterion that permits attributed testimony. It never replaces verification that the criterion or an applicable check requires. Missing, inaccessible, contradictory, mismatched, or non-durable evidence is insufficient; do not fill the gap from context or implementation inspection.

The overall verdict is exactly `sufficient` only when every criterion is sufficient. Otherwise it is `insufficient` and names every weak or missing criterion. Review never writes evidence, ticks a task, closes a target, or authorizes Land.

## Evidence-sufficiency report

End with these headings in order. No heading is empty; use `none` where applicable.

```markdown
## Evidence-sufficiency report

### Target and sources

### Criterion verdicts

### Overall verdict

### Not independently verified
```

`Target and sources` names the task contract, exact durable record version, real git target or the no-git probes, and sources inspected. `Criterion verdicts` uses:

`criterion | durable evidence locator | source attribution | independent verification and locator | sufficient/insufficient | reason`

Then append the terminal status required by Review's `SKILL.md`.
