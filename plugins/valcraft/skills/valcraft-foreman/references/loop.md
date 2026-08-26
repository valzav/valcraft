# Named-state delivery loop

This reference owns Foreman's state machine. Every dispatch uses the envelope in [`contracts.md`](contracts.md). After recording each transition in `state.md`, update the harness progress list per SKILL.md's display rule.

On Cursor, bind every worker prompt to the assigned producer's absolute `SKILL.md` path from the parent's active plugin root. Do not slash-invoke `valcraft-review` or `/review`. Cursor's built-in `/review` is not Valcraft Review.

Only an explicit delivery command enters the loop.

## Quick tasks

Validate the pool with [`../../valcraft-spec/references/quick.md`](../../valcraft-spec/references/quick.md). Walk files and `QT-XXX` tasks in number order. Preserve the canonical identity `Q-NNN QT-XXX`, branch `feat/qNNN-qtNNN-<slug>`, and report identity `QNNN-QTNNN`. Quick tasks use the same states and gates as feature tasks. Their task artifact replaces `spec.md`, `design.md`, and `tasks.md` in assignments. The last Land completion finishes the file without feature confirmation or Temper.

## Rebuild before transition

Read `state.md`, the tracker-specific intake, and authoritative git or tracker state. Verify every stored path, SHA, branch, PR, issue, backend return, and active worker identity before using it.

On a shared checkout, staged, unstaged, or untracked state stops before fetch, switch, synchronization, or task-branch creation. Record and preserve it. Known attribution does not waive this task-start gate. Dead-worker recovery is the separate existing-task path in the backend contract.

Before a new pick, reconcile the clean local default branch with its live remote:

- equal: record the common SHA;
- remote ahead: fast-forward, verify equality, then record;
- local ahead: wait for an operator instruction that names the exact push;
- diverged: stop without merge, rebase, reset, force push, or task-branch creation.

`foreman.release_branch: null` means no separate release branch. Fast-track and direct release-only paths are unavailable. An omitted key invalidates the configuration and delegates repair to Tune. Any configured release-branch write remains a human gate.

Apply Spec's readiness contract. An unready feature routes to Spec's direct caller; Foreman never repairs feature artifacts. Never interleave feature and quick pools.

## Resume map

Route only from verified producer reports and exact targets:

| Durable evidence                                                  | Named state      |
| ----------------------------------------------------------------- | ---------------- |
| selected eligible task with no plan                               | `Drafting`       |
| committed Draft plan not yet accessible to the next Review worker | `Drafting`       |
| committed Draft plan without an exact plan verdict                | `PlanReview`     |
| exact passing plan verdict without Forge output                   | `Implementing`   |
| Forge implementation head with required task PR still prepared    | `Implementing`   |
| Forge task PR head without an exact code verdict                  | `CodeReview`     |
| passing code verdict covering the current PR head                 | `Landing`        |
| Land evidence record without fresh sufficiency verdict            | `EvidenceReview` |
| confirmed feature not yet closed by Land                          | `FeatureClose`   |
| feature closure complete without a retrospective report           | `Retrospective`  |
| Temper report without an exact verdict                            | `RetroReview`    |

Never restart Draft when a current committed plan exists. Never infer Review coverage from a branch, PR number, or earlier verdict.

## `Ready`

Select the first eligible task in artifact order with satisfied dependencies and no hold. Apply the approval-mode pick gate. Record the reconciled predecessor SHA, canonical task branch, contract path, and intermediate in-progress tracker state. Move to `Drafting`.

When no eligible task remains:

- a quick run completes when its files are fully closed by Land;
- a feature waits for operator confirmation, then enters `FeatureClose`;
- an unconfirmed feature remains at the named human gate.

## `Drafting`

Dispatch `drafter-<identity>` with `valcraft-draft`, the task contract, predecessor SHA, canonical branch, backend physical branch when applicable, durable deferred-finding locators, and exact target-bound outward authority when granted. Foreman writes no plan and does not run MSW.

On a complete `Status: done` Draft report, verify the committed plan path and exact head. Apply the prepared outward continuation in `contracts.md` when the next Review worker cannot access that exact commit. Enter `PlanReview` only when the Review worker can resolve the exact committed head. Route declared Draft codes through `contracts.md`.

## `PlanReview`

Dispatch a fresh `plan-reviewer-<identity>` with `valcraft-review` in plan mode on the exact committed plan head. A pass enters `Implementing`. Material findings return the report path and R-IDs to Drafting. Apply [`review-round.md`](review-round.md) without deciding a finding. An exact-target mismatch or undeclared code stops.

## `Implementing`

Dispatch `forge-<identity>` with `valcraft-forge`, the exact passing plan Review report, canonical remote task ref, predecessor head, and target-bound push and task-PR authority when granted. Forge owns implementation, code-finding remediation, verification, push, and task-PR preparation or creation.

A complete Forge report whose task PR is still `none` applies the prepared outward continuation in `contracts.md` and remains in `Implementing`. Enter `CodeReview` only after Forge reports one exact task PR and its exact Review target. `draft_required` returns to Drafting. Route every other code through the registry. Foreman never edits source, pushes, or creates a PR.

## `CodeReview`

Dispatch a fresh `code-reviewer-<identity>` with `valcraft-review` in code mode on the Forge report's exact repository, PR, base, and head. A pass covering the current head enters `Landing`. Material findings return to Implementing by R-ID. Apply [`review-round.md`](review-round.md). A stale target stops or takes the producer's declared mismatch route; Foreman never reviews the delta.

## `Landing`

Dispatch `land-<identity>` with `valcraft-land`, the target kind, exact current target, Review report, applicable approval-mode decision, tracker closure target, and any trusted target-bound authorization. Land owns final-head comparison, applicable checks, completion ticks, merge, closure, partial-mutation reconciliation, and external evidence recording.

Route the Land report exactly:

- `review_required`: task PR to CodeReview, spec PR to Spec's direct caller;
- `check_failure_task`: Implementing;
- `check_failure_spec`: Spec's direct caller;
- `evidence_review_required`: EvidenceReview;
- `partial_completion`: Landing with only remaining operations;
- `authority_required`: apply the prepared mutation continuation in `contracts.md` and remain in Landing; and
- unresolved, external, configuration, authority, or applicability codes: Blocked.

When checks are pending, keep Foreman and the active Land worker alive. Continue the backend's await discipline against the same assignment. Do not turn a pending check into a user-status prompt, new worker, or Foreman-owned classifier. A missing required check routes to an artifact owner only after Land's authoritative evidence proves that owner; otherwise it remains Blocked.

A completed task target returns to Ready. A completed external closure returns to Ready. A completed feature-close target enters Retrospective.

## `EvidenceReview`

Dispatch a fresh `review-evidence-<identity>` with `valcraft-review` in evidence mode on Land's exact durable evidence record. Review owns criterion-by-criterion sufficiency. A sufficient report returns to Landing with the exact verdict. An insufficient or blocked report follows the registry. Foreman records and judges no evidence.

The return re-enters `Landing` carrying the whole ownership listed there — final-head comparison, applicable checks, completion ticks, merge, closure, partial-mutation reconciliation, and evidence recording — not the completion tick alone. Which of those the resolved tracker mode actually requires, and in what order, is Land's own contract in [`../../valcraft-land/references/tracker-closure.md`](../../valcraft-land/references/tracker-closure.md).

## `FeatureClose`

Dispatch tracker-only Land with the exact feature or PRD target and the operator's quoted confirmation. Land closes only the authorized real tracker target. On completion, enter Retrospective. Foreman neither builds nor executes a closing batch.

## `Retrospective`

Dispatch `temper-<feature>` with `valcraft-temper` in analyze mode on the exact closed feature corpus and the repository head it describes. Temper writes one local report under the gitignored `docs/.retro/` and no git state; the assignment grants no outward authority because none is needed.

Enter `RetroReview` when Temper reports its exact Review target: the absolute report path, its content hash, and the described head. Material retrospective findings return here by R-ID, and Temper edits the same report in place. `report_dir_not_ignored` is Blocked: the project frame owns `.gitignore`. Foreman never creates the report and never applies proposals; an unattended run leaves Temper's escalated proposals as `offered, awaiting selection` for the operator.

## `RetroReview`

Dispatch a fresh `retro-reviewer-<feature>` with `valcraft-review` in plan mode on the exact report path and content hash. A pass enters Complete; nothing is merged, because the report is not in git. Material findings return to Retrospective. Foreman never reviews the report.

## `Blocked` and recovery

Name the code, target, source report, and evidence or authority required to leave the state. `permission_blocked`, transport failure, and dead-worker recovery remain backend returns rather than producer status.

A dead worker first records the backend return and complete recovery inventory. A safe replacement receives a fresh physical identity and the same logical identity. Reject any late predecessor report or path after replacement. Never synthesize or complete the dead worker's report.

## Cross-task findings

Route a finding into the current task only when the current diff caused the inconsistency or the owning contract blocks the current task's acceptance criterion. Record the owner and passing causal test. Remediation retains R-ID closure, review-round, exact-target, and Land gates.

Otherwise route a durable finding locator to the future owner through the tracker intake without implementing it. Verify that locator before a later Draft assignment. A verified non-blocking deferral does not block the current task; an unverified one does.
