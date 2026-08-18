# Record and close

Read this reference when the operator says an open Cast task was completed outside the
delivery loop. This is an evidence-and-tracker path, not retrospective implementation:
do not create a planner, an implementation plan, or a normal full review round. Do not
use it for partially completed work or to bypass an open finding; route either through
the ordinary loop.

## Establish the contract

Resolve one open feature task or canonical `Q-NNN QT-XXX` quick task through its
tracker-owned artifact. Read the task's committed contract and enumerate every
acceptance criterion it owns or claims to cover. A task whose criterion set cannot be
resolved is not ready to close. Record the operator's completion claim as an `Operator
attestation` with its source locator; it is evidence to assess, not proof.

Use two fresh workers with the assignment envelope from `contracts.md`:

1. `recorder-<F>-<T>` (quick: `recorder-QNNN-QTNNN`) gathers evidence and records it in
   the tracker-owned artifact. It does not implement the task.
2. `evidence-reviewer-<F>-<T>` (quick: `evidence-reviewer-QNNN-QTNNN`) starts only after
   the durable record exists. It has no context from the recorder and judges evidence
   sufficiency only. It does not run `valcraft:review` or review the implementation.

The recorder and reviewer use the report shapes in `contracts.md`. They must be
different fresh workers. A self-review, verdict-only report, or report that omits one
criterion is incomplete.

## Record evidence

For each criterion record its ID, the claim being supported, the source class and
source locator, and the durable evidence locator. Preserve `Operator attestation` and
`Foreman observation` labels from the assignment. Never promote either to a fact.

The tracker mode determines the durable location:

- **Local feature:** place a `Completion evidence` block directly beneath the target
  task in `specs/<feature>/tasks.md`, keyed by criterion ID.
- **Quick:** place the same block directly beneath the target `QT-XXX` item in its quick
  file. Create no feature-task entry or GitHub issue.
- **GitHub:** the recorder proposes the complete attributed evidence comment in its
  report. The foreman records and executes that task-issue comment as an exact tracker
  batch, then gives the resulting comment URL to the reviewer. The recorder does not
  write the tracker.

In local and quick mode, the recorder creates or resumes the task branch, commits the
evidence block, pushes, and opens or updates the task PR. Evidence for one task never
lands beside another task merely because it is nearby.

## Review sufficiency

The evidence reviewer reads the committed task contract, the durable evidence record,
and only the authoritative sources named by those records. Its criterion table contains
every criterion from the contract, including omitted evidence. For each row it records:

- criterion ID and durable evidence locator;
- source attribution;
- `independently verified` with the method and locator, or `not independently verified`;
- `sufficient` or `insufficient`, with the reason.

An operator attestation may support a criterion whose contract permits attributed
testimony. It is not automatically sufficient and never replaces verification that the
criterion or an applicable check requires. The overall verdict is `sufficient` only
when every criterion row is sufficient. Otherwise record the weak or missing criteria
in `state.md`, leave the task open and unticked, and perform no closing batch or merge.

## Apply the closing gates

After a sufficient verdict, apply `loop.md`'s shared applicable-check classifier.
Inspect the task requirements and every configured source; run or query each applicable
check against its real authoritative target. A check that requires a commit or head
cannot pass without one.

For a local or quick evidence PR, obtain scoped review of the exact evidence delta and
record its head as reviewer-covered. Then have the recorder add only the target task's
unchecked-to-checked transition, commit, and push. Apply the exact-final-head gate;
only that exact tick may bypass another scoped review. Merge only after review and
checks cover the exact final head.

For GitHub evidence with a real cited PR or commit, verify it and apply the same exact
target and applicable-check rules. When the completed work has no git change, record
that observed fact and do not invent a branch, commit, PR, SHA, or review target. The
narrow sufficiency review remains the review gate. This no-git branch of the final-head
gate passes only when authoritative probes establish the absence and no applicable
check requires a git target; otherwise wait. Applicable checks still use their real
targets. After all gates pass, close through `intake-github.md`'s serialized batch and
include the evidence comment URL and sufficient verdict in the close comment.

Record the recorder report, durable evidence, sufficiency report, per-criterion verdicts,
real git target or its observed absence, applicable checks, exact final SHA when one
exists, and closing operation in `state.md`.
