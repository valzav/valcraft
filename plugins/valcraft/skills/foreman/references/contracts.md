# Coordination contracts

This registry links producer-owned reports to coordinator transitions. It never copies a
report shape. The producing skill owns its headings, semantic fields, routing codes, and
terminal `Status:` line.

## Assignment envelope

Send every worker these fields in order:

1. **Cold start.** Invoke the named skill, then read root `AGENTS.md`, then only the
   named artifacts and references.
2. **Assignment identity.** Record the run id, assignment id, named state, feature or
   quick identity, canonical logical worker identity, current physical worker identity,
   backend, and exact absolute report path.
3. **Target.** Name the repository, tracker reference, authoritative task contract,
   exact predecessor artifact or PR identity and SHA, canonical branch, and physical
   branch when applicable. Use `none` instead of inventing a git target.
4. **Intent.** Name the producer skill, its mode, and the exact transition this report
   may unlock. Pass contract and prior-report paths rather than copied content.
5. **Attributed context.** Label each item `Operator instruction/decision`, `Operator
   attestation`, or `Foreman observation`, with its source and scope. Only a live
   operator instruction or an attributed Foreman assignment field can carry mutation
   authority. Bind authority to repository or remote, branch base and head, PR or
   tracker target, and operation set.
6. **Report instruction.** Require the producer's unchanged report contract at the
   assigned path. Require the producer to return only that path and its terminal
   `Status:` line through the backend channel.
7. **Trust boundary.** Include `SKILL.md`'s trust-boundary paragraph verbatim.

Every dated artifact resolves its date from repository policy, then an explicit
operator date for that artifact, then its creation date. The run id does not supply an
artifact date.

## Message registry

| Message | Producer | Consumer | Authoritative report contract | Active state | `done` transition |
| --- | --- | --- | --- | --- | --- |
| Project frame | Cast | direct caller, then Spec | [`../../cast/SKILL.md#report`](../../cast/SKILL.md#report) | OutsideLoop | `ReturnToCaller` |
| Feature or quick contract | Spec | direct caller, Review, Land | [`../../spec/references/delivery.md#spec-report`](../../spec/references/delivery.md#spec-report) | OutsideLoop | `ReturnToCaller` |
| Task plan | Draft | Foreman, Review | [`../../draft/references/plan-contract.md#report`](../../draft/references/plan-contract.md#report) | Drafting | `PlanReview` |
| Plan verdict | Review | Foreman, Draft or Forge | [`../../review/SKILL.md#reports`](../../review/SKILL.md#reports) | PlanReview | `PlanVerdict` |
| Task implementation and PR | Forge | Foreman, Review | [`../../forge/references/verification-and-handoff.md#forge-report`](../../forge/references/verification-and-handoff.md#forge-report) | Implementing | `CodeReview` |
| Code verdict | Review | Foreman, Forge or Land | [`../../review/SKILL.md#reports`](../../review/SKILL.md#reports) | CodeReview | `CodeVerdict` |
| Finalization or evidence record | Land | Foreman, Review or direct caller | [`../../land/SKILL.md#report`](../../land/SKILL.md#report) | Landing or FeatureClose | `LandResult` |
| Evidence-sufficiency verdict | Review | Foreman, Land | [`../../review/references/evidence-mode.md#report`](../../review/references/evidence-mode.md#report) | EvidenceReview | `Landing` |
| Retrospective report and PR | Temper | Foreman, Review | [`../../temper/SKILL.md#report`](../../temper/SKILL.md#report) | Retrospective | `RetroReview` |
| Retrospective verdict | Review | Foreman, Temper or Land | [`../../review/SKILL.md#reports`](../../review/SKILL.md#reports) | RetroReview | `RetroVerdict` |

`PlanVerdict`, `CodeVerdict`, and `RetroVerdict` read the report's structured verdict,
not prose: pass advances to Implementing, Landing, or Landing respectively; material
findings return to Drafting, Implementing, or Retrospective. LandResult uses the
reported target kind: a completed task returns Ready, a completed tracker-only feature
close enters Retrospective, a completed retrospective PR enters Complete, and completed
external closure returns Ready.

## Declared outcome routing

Each declared code has one transition. The detail after `—` never changes it.

### Cast

| Outcome | Transition |
| --- | --- |
| `scaffold_approval_required` | `AwaitOwner` |
| `baseline_required`, `baseline_failed`, `artifact_validation_failed`, `authority_drift`, `push_failed` | `StopProducer` |

### Draft

| Outcome | Transition |
| --- | --- |
| `assignment_invalid`, `workspace_not_ready`, `review_target_mismatch`, `msw_failed`, `git_write_failed`, `authority_drift`, `push_failed` | `Blocked` |
| `product_decision_required`, `owner_decision_required` | `AwaitOwner` |

### Forge

| Outcome | Transition |
| --- | --- |
| `draft_required` | `Drafting` |
| `review_target_mismatch` | `CodeReview` |
| `assignment_invalid`, `workspace_not_ready`, `implementation_blocked`, `authority_drift`, `push_failed`, `pr_failed` | `Blocked` |
| `product_decision_required` | `AwaitOwner` |

### Review

| Outcome | Transition |
| --- | --- |
| `review_target_mismatch` | `Blocked` |
| `review_blocked`, `evidence_review_blocked` | `Blocked` |
| `evidence_insufficient` | `Landing` |

### Land

| Outcome | Transition |
| --- | --- |
| `review_required` | `ReviewByTarget` |
| `check_failure_task` | `Implementing` |
| `check_failure_spec` | `ReturnToSpecCaller` |
| `check_failure_retro` | `Retrospective` |
| `evidence_review_required` | `EvidenceReview` |
| `operator_action_required` | `OperatorAction` |
| `partial_completion` | `Landing` |
| `operator_confirmation_required` | `AwaitOwner` |
| `missing_required_check`, `check_source_unavailable`, `external_blocked`, `authority_required`, `authority_drift`, `release_authority_required`, `evidence_insufficient`, `target_ambiguous` | `Blocked` |

`ReviewByTarget` means task PR to CodeReview, retrospective PR to RetroReview, and spec
PR to Spec's direct caller outside the loop. It is one target-kind transition function.

### Spec

| Outcome | Transition |
| --- | --- |
| `source_selection_required`, `product_decision_required`, `owner_decision_required`, `tracker_target_required` | `AwaitOwner` |
| `assignment_invalid`, `scaffold_invalid`, `feature_identity_invalid`, `workspace_not_ready`, `review_target_mismatch`, `git_write_failed`, `authority_drift`, `projection_failed`, `push_failed`, `pr_failed` | `StopProducer` |

### Temper

| Outcome | Transition |
| --- | --- |
| `authority_required` | `Blocked` |
| `corpus_invalid`, `analysis_blocked`, `git_write_failed`, `authority_drift`, `push_failed`, `pr_failed` | `Blocked` |
| `owner_decision_required` | `AwaitOwner` |

## Backend returns

Record exactly one return against the active assignment before report validation.

| Backend return | Await effect | Transition |
| --- | --- | --- |
| `report_available` | terminal | `ReportValidation` |
| `permission_blocked` | wait for an allowed answer or escalation | `BlockedPrompt` |
| `idle_without_report` | terminal | `WorkerRecovery` |
| `dispatch_error` | terminal | `DispatchRecovery` |
| `dead` | terminal | `DeadWorkerRecovery` |
| `wait_timeout` | nonterminal; foreground only | remain in the current named state and re-arm await |

Only `report_available` opens the attributed producer report. A producer's
`Status: blocked: <code> — <detail>` is report content under `report_available`; it is
never `permission_blocked`.

## Validation and rejection

Require the active assignment id, logical worker, physical worker, backend return, and
report path to match `state.md` and `workers.md`. Reject a predecessor's late report
after replacement, even when its report contract is complete. A report is complete
only when its producer-owned headings are present in order, required exact identities
are populated, and exactly one terminal status line is last.

On the first incomplete report, reassign the same producer to append the missing named
parts. On the second, escalate under the established two-attempt rule. Never fill a
missing field, copy a shape into another report, interpret prose as a code, or advance
on an undeclared code.
