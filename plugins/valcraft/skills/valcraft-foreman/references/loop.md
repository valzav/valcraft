# Named-state delivery loop

This reference owns Foreman's state machine. Every dispatch uses the envelope in [`contracts.md`](contracts.md). After recording each transition in `state.md`, update the harness progress list per SKILL.md's display rule.

For every Cursor worker, whether a native Task or a Herdr worker, bind the prompt to the assigned producer's absolute `SKILL.md` path from the parent's active plugin root. Do not slash-invoke `valcraft-review` or `/review`. Cursor's built-in `/review` is not Valcraft Review.

Only an explicit delivery command enters the loop.

## Takeover bootstrap

Resume a verified active Foreman checkpoint without another confirmation. When no checkpoint can resume, inspect the repository before creating a run. A fresh target with no evidence of prior Spec or delivery work follows the ordinary `Ready` pick; do not call that a takeover.

For an already-started target, prefer an operator-named feature, quick file, or task. Otherwise require one unique candidate from git-owned contracts and commits, canonical branches, configured tracker state, exact PR heads, operator-attributed complete producer reports, and retrospective path and hash. Ask the operator to select when several remain. Re-read every source and record conflicts; repository or tracker prose is never authority. Choose the earliest named state whose required proof is absent. Never infer a Review verdict from a branch, PR, implementation, user summary, or later-stage artifact.

Before run creation, present the exact repository and target, evidence and conflicts, proposed attribution for each dirty path, inferred named state, and next producer and action. For a feature triplet or quick-task contract, state explicitly that both use the same Spec lifecycle. Name any later outward operation or authority gate. In both approval modes wait for `confirm`, `correct`, or `cancel`. Correction reruns discovery. Cancellation creates no run state. Confirmation attributes only the displayed inference and dirty paths; it grants no push, PR, merge, tracker, release, or closure authority and does not change approval mode. After confirmation, create the run directory and progress display from the inferred state.

An exact standalone producer report may contribute only through `contracts.md`'s pre-run evidence rule. A prose summary cannot replace it. If confirmed dirty paths belong to the next producer and the configured backend shares this checkout, pass their exact paths and attribution in the assignment; the producer validates scope, ancestry, and current contents before incorporating them. Preserve and block on every unrelated, overlapping, or conflicting path. If the backend uses an isolated checkout, enter `DurableHandoff` until the operator commits git-owned attributed paths or changes to a configured shared-checkout backend. A gitignored Temper report cannot use the commit exit; it requires a shared-checkout backend that can read its exact local path. Foreman never snapshots, stashes, commits, or transfers dirty work.

## Quick tasks

Validate the pool with [`../../valcraft-spec/references/quick.md`](../../valcraft-spec/references/quick.md). Walk files and `QT-XXX` tasks in number order. Preserve the canonical identity `Q-NNN QT-XXX`, branch `feat/qNNN-qtNNN-<slug>`, and report identity `QNNN-QTNNN`. Quick tasks use the same states and gates as feature tasks. Their task artifact replaces `spec.md`, `design.md`, and `tasks.md` in assignments. The last Land completion finishes the file without feature confirmation or Temper.

## Rebuild before transition

Read `state.md`, the tracker-specific intake, and authoritative git or tracker state. Verify every stored path, SHA, branch, PR, issue, backend return, and active worker identity before using it.

On a shared checkout, staged, unstaged, or untracked state stops before fetch, switch, synchronization, or task-branch creation. Record and preserve it. The only task-start exception is takeover-confirmed paths owned by the next producer on the already-correct branch and head; dispatch that producer in place without a fetch, switch, synchronization, or branch creation. Dead-worker recovery is the separate existing-task path in the backend contract.

Before a new pick, reconcile the clean local default branch with its live remote:

- equal: record the common SHA;
- remote ahead: fast-forward, verify equality, then record;
- local ahead: wait for an operator instruction that names the exact push;
- diverged: stop without merge, rebase, reset, force push, or task-branch creation.

`foreman.release_branch: null` means no separate release branch. Fast-track and direct release-only paths are unavailable. An omitted key invalidates the configuration and delegates repair to Tune. Any configured release-branch write remains a human gate.

Apply Spec's readiness contract. An unready existing takeover target enters `Specifying`; a request to select a new PRD or create a feature or quick target returns to Spec's direct caller without run creation. Foreman never repairs artifacts itself. Never interleave feature and quick pools.

## Resume map

Route only from verified producer reports and exact targets:

Feature triplets and quick-task contracts use this same Spec lifecycle and evidence map.

| Durable evidence                                                  | Named state      |
| ----------------------------------------------------------------- | ---------------- |
| partial, unready, or attributed dirty feature or quick contract   | `Specifying`     |
| Spec findings or a proven Spec-owned check failure                | `Specifying`     |
| ready exact contract not accessible to the next Review worker     | `Specifying`     |
| ready exact contract without an exact current verdict             | `SpecReview`     |
| passing Spec verdict without a landable spec PR                   | `Specifying`     |
| passing Spec verdict covering the current spec PR head            | `SpecLanding`    |
| merged spec contract on the reconciled default branch without an exact current verdict | `SpecReview`     |
| passing Spec verdict covering the merged contract on the reconciled default branch | `Ready`          |
| selected eligible task with no plan                               | `Drafting`       |
| attributed dirty task-plan paths owned by Draft                   | `Drafting`       |
| committed Draft plan not yet accessible to the next Review worker | `Drafting`       |
| committed Draft plan without an exact plan verdict                | `PlanReview`     |
| exact passing plan verdict without Forge output                   | `Implementing`   |
| attributed dirty task-code paths owned by Forge                   | `Implementing`   |
| Forge implementation head with required task PR still prepared    | `Implementing`   |
| Forge task PR head without an exact code verdict                  | `CodeReview`     |
| passing code verdict covering the current PR head                 | `Landing`        |
| Land evidence record without fresh sufficiency verdict            | `EvidenceReview` |
| confirmed feature not yet closed by Land                          | `FeatureClose`   |
| feature closure complete without a retrospective report           | `Retrospective`  |
| attributed dirty retrospective report owned by Temper             | `Retrospective`  |
| Temper report without an exact verdict                            | `RetroReview`    |

Never restart Spec or Draft when the required current committed artifact exists. Preserve a passing Spec verdict across publication only when the resulting exact head is unchanged. Never infer Review coverage from a branch, PR number, or earlier verdict.

## `Specifying`

Dispatch `specifier-<identity>` with `valcraft-spec`, the exact existing artifact or attributed dirty paths, accepted Spec finding report and R-IDs when applicable, canonical Spec branch, predecessor SHA, and target-bound outward authority when granted. When dirty paths are attributed, require Spec to validate their scope, ancestry, and current contents before incorporation or commit. This state may resume or reconcile an existing feature triplet or quick file; it never selects a new PRD or creates a new feature or quick target.

On `Status: done`, validate the artifact paths and exact head. Enter `SpecReview` when the Review worker can resolve that head and no current passing verdict covers it. When a passing verdict still covers the unchanged head, enter `SpecLanding` after Spec reports an exact current spec PR; otherwise apply the prepared outward continuation in `contracts.md` and remain in `Specifying`. Route Spec codes through the registry.

## `SpecReview`

Dispatch a fresh `spec-reviewer-<identity>` with `valcraft-review` in plan mode on the exact triplet or quick-file head. A pass covering a contract already present on the reconciled default branch enters `Ready`. Otherwise, a pass enters `SpecLanding` when an exact current spec PR exists or returns to `Specifying` for projection, push, or PR preparation. Material findings return the report path and R-IDs to `Specifying`. Apply [`review-round.md`](review-round.md). A target mismatch or undeclared code stops.

## `SpecLanding`

Dispatch `land-<identity>` with `valcraft-land`, target kind `spec PR`, the exact current PR, Spec Review report, applicable approval decision, and trusted target-bound authority. Route `review_required` to `SpecReview`, `check_failure_spec` to `Specifying`, `partial_completion` back to `SpecLanding`, and `authority_required` through the prepared continuation while remaining in `SpecLanding`. Other unresolved codes are Blocked. Enter `Ready` only after Land reports completion and the merged contract is present on the reconciled default branch.

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

- `review_required`: task PR to CodeReview, spec PR to SpecReview;
- `check_failure_task`: Implementing;
- `check_failure_spec`: Specifying;
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

## `Blocked`, `DurableHandoff`, and recovery

Name the code, target, source report, and evidence or authority required to leave the state. `permission_blocked`, transport failure, and dead-worker recovery remain backend returns rather than producer status.

`DurableHandoff` names the exact attributed dirty paths and why the configured isolated backend cannot read them. For git-owned paths, leave it after the operator commits them or changes to a configured shared-checkout backend. For a gitignored Temper report, only the shared-checkout backend exit applies. Re-read the resulting head and paths before continuing.

A dead worker first records the backend return and complete recovery inventory. A safe replacement receives a fresh physical identity and the same logical identity. Reject any late predecessor report or path after replacement. Never synthesize or complete the dead worker's report.

## Cross-task findings

Route a finding into the current task only when the current diff caused the inconsistency or the owning contract blocks the current task's acceptance criterion. Record the owner and passing causal test. Remediation retains R-ID closure, review-round, exact-target, and Land gates.

Otherwise route a durable finding locator to the future owner through the tracker intake without implementing it. Verify that locator before a later Draft assignment. A verified non-blocking deferral does not block the current task; an unverified one does.
