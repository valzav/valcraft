# Record and close external completion

Use this flow for one open feature task or canonical `Q-NNN QT-XXX` completed outside the delivery loop. It does not implement work or bypass an open finding.

## Record criterion evidence

Resolve the committed task contract and enumerate every acceptance criterion the task owns or claims to cover. An unresolved criterion set stops the flow.

Create one durable record row per criterion:

`criterion | claim | source class and locator | durable evidence locator`

Preserve `Operator attestation` and `Foreman observation` attribution. Neither is automatically fact or sufficient evidence. Store the record in the tracker-owned task artifact: beneath the local feature or quick task, or as a prepared hosted issue comment. A hosted comment requires its own exact tracker-write authority.

Record the real branch, PR, commit, and head if any exists. Otherwise probe authoritative git and hosting sources, record their observed absence, and invent no git identity.

## Request fresh Review

Return an evidence-mode `valcraft:review` handoff that names:

- the exact task contract and every criterion;
- the durable record and immutable locator or version;
- each authoritative source named by the record; and
- the real git target or the probes that established its absence.

Land never judges sufficiency and never spawns Review on direct invocation. The next caller supplies the Review report on resume.

Accept only a fresh Review context's complete `## Evidence-sufficiency report` for the exact record. Every criterion needs an independent-verification result, `sufficient` or `insufficient`, and a reason. A mismatched or incomplete report returns `evidence_review_required`. Any insufficient row returns `evidence_insufficient`; leave the task open and unticked.

## Close against real state

After a sufficient verdict, apply the check classifier to every real applicable target. A check that requires a commit cannot pass without one. With no git target, the final-head gate passes only when authoritative probes establish absence and no applicable check requires git.

Then prepare the exact task closure under `tracker-closure.md`. For local or quick evidence, the evidence delta receives scoped Review before the exact completion tick. For a hosted tracker, the close batch cites the durable evidence locator and sufficient verdict. Execute only with target-bound tracker authority and preserve partial results for reconciliation.
