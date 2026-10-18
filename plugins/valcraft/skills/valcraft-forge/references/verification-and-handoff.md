# Forge verification and handoff

Read this reference before editing code. It owns Forge's assignment, verification, outward-mutation, recovery, Review-handoff, and report contracts.

## Assignment and workspace

Forge runs only under a Foreman assignment. Without an assignment envelope, change nothing and reply with only the line `Status: blocked: assignment_invalid — no Foreman assignment; run valcraft-foreman`. Require the envelope's repository, task identity, canonical task branch, start SHA, which is the passed plan-review SHA, backend identity, and any physical branch. Never derive a branch.

Follow [`../../valcraft-foreman/references/outward-mutation.md`](../../valcraft-foreman/references/outward-mutation.md) for shared-checkout and isolated-workspace rules. Takeover-attributed dirty Forge paths are allowed only on the already-correct shared canonical branch at an attributable implementation head that equals or descends from the reviewed-plan SHA while the reviewed plan remains unchanged; validate and incorporate them as that reference defines.

## Verify the implementation

Run the repository's real tests, typecheck, lint, and applicable integration checks. Cite command output. For every new or changed test, state the defect that could still pass it.

Every verification step the passed plan names is part of the implementation. Do not return `Status: done` while the head leaves one unimplemented. Implement it. Return `implementation_blocked` when current repository evidence cannot support it, and `draft_required` when it needs a different approach. Disclosing the step under `Open questions` does not replace that return.

Scope each run to what the change can affect. While iterating, run the targeted suites, checks, and reproductions for the files and contracts the commit touches; red-first evidence and mutation checks use the targeted suite. Run the repository's full gate — every configured test, typecheck, lint, and build — on the exact head that will be pushed. Reuse a full-gate result only when that run passed and the verification inputs it depended on — the head, the toolchain, the configuration, and the data state — are unchanged. Retry a failed run after its cause is fixed. A changed head or input needs a new run. Do not re-run a passed gate on unchanged inputs, and do not run the full gate in place of a targeted reproduction. Cite each full-gate run beside the head SHA and inputs it covered.

Before accepting verification results, establish the effective environment prerequisites the check depends on and record the evidence beside the result. For browser checks, prove that the runner reaches the intended candidate, including when it reuses an existing server. Inspect effective configuration or data state when it can change the result; a requested command or exported variable is not proof of the state used. Do not require unrelated infrastructure checks. An unresolved prerequisite leaves the affected verification unproven and follows the existing blocker route.

- Test negative and invariant claims by attempting to violate them.
- Before relying on a negative result, inject a known-present condition and prove the same instrument detects it. Record that calibration beside the check; reversing a fix does not calibrate the instrument.
- Characterize uncovered behavior before changing it.
- Mutation-check a non-trivial fix by reversibly restoring the unfixed behavior, observing the focused regression test fail, restoring the fix, and rerunning green.
- Reproduce a review finding's failure mode in disposable state.
- Cover combinations of orthogonal inputs, not only each dimension alone.
- Force an interleaving when checked state can change before an action.
- Test that empty, partial, or default success output cannot replace real data.
- Read raw command or CI output when a wrapper may hide failure.
- Verify UI criteria yourself through the recorded verification route, headless when the route allows it. Never defer a UI judgment to the operator or to Review. When no route is available, report the code-only exception.

Update affected git-owned contracts and documentation in the same change. Verify branch claims against the final code. Confirm no secret or consumer-specific material was added.

## Commit the completion transition

The task's own checkbox transition is part of the implementation in `local` tracker mode for a feature task, and in every tracker mode for a quick task. Read the tracker mode from the committed `.valcraft/config.yaml`.

- Make the transition the last edit before the full gate, and commit it with the final implementation change.
- Change exactly the selected `T-XXX` line in `tasks.md`, or the selected `QT-XXX` line in the quick file, from unchecked to checked.
- Change no other line of the feature triplet or quick file. This transition is the only edit Forge makes to either.
- Keep the transition in every head you push, including after remediation. Never make it twice or revert it.

In `github` mode, do not edit `tasks.md`; Land closes the task issue. The checkbox still means merged into the default branch, because the task branch reaches the default branch only through Land's merge.

## Stay inside the passed plan

A necessary change can fall outside the passed plan's touched scope, or change its declared approach, even with no Review finding. Examples are an edit to a file the plan does not touch and a different technique for a planned step. When implementation shows such a change is needed, do not commit, push, or open a PR containing it. Keep verified in-scope work as local commits. Record the change as a diff under `Open questions`, with the evidence that makes it necessary. Then restore exactly the paths that change touched to the last commit, staged and unstaged, so the checkout is clean for Draft and for Forge's later resume. This removes only Forge's own uncommitted edit; it is not the reset that manufactures readiness, and it touches no other path, unrelated state, or commit. Return `draft_required` with the exact plan path and commit. Disclosing the change under `Open questions` does not replace that return.

## Push and open the task PR

Local implementation and commits follow from the Forge assignment. The dispatch carries the ref-bound producer grant in [`../../valcraft-foreman/references/contracts.md`](../../valcraft-foreman/references/contracts.md#ref-bound-producer-grant): non-force push of the canonical task ref and task-PR creation or update. It binds every field except the head, and authorizes pushing only the clean head on which your full gate passed, descending from the passed plan SHA with the plan blob unchanged. It covers no other head. Follow [`../../valcraft-foreman/references/outward-mutation.md`](../../valcraft-foreman/references/outward-mutation.md) for revalidation, push, PR, partial results, and the codes `authority_drift`, `workspace_not_ready`, `push_failed`, and `pr_failed`.

When that head exists, push it and create or update the one task PR in the same assignment. The PR body cites the task identity and, for each Spec-owned commit the passed plan Review pinned, that commit and its R-IDs. A remediation push updates the same PR.

Under `Outward mutations`, name the grant as ref-bound and record the exact head it pushed and the PR. `Status: done` means the implementation is pushed and in its task PR, ready for Review; it does not imply the task shipped.

## Hand off to Review

Return one exact code target:

- repository identity;
- base ref and full base SHA: the base ref's head observed when you report. Review diffs from the merge base of base and head, so the target covers every commit on the task branch, including implementation committed under an earlier plan;
- head ref and full implementation SHA;
- canonical task branch and physical branch or `none`;
- PR identity or `none`; and
- verification evidence and the passed plan path and full plan SHA.

Foreman routes the target to a fresh `valcraft-review` worker. Forge never invokes itself as reviewer and never treats its own verification as a Review verdict.

## Forge report

End every run with this block. Keep headings in order. Use `none` for an empty section. Nothing follows the terminal status line.

```markdown
## Forge report

### Task

### Plan and plan review

### Workspace

### Changed (IDs)

### Verification evidence

### Finding resolutions

### Outward mutations

### Open questions

### Review target
```

End with exactly one line:

- `Status: done`
- `Status: blocked: <code> — <detail>`
- `Status: question: <code> — <detail>`

Use these stable routing codes:

- `assignment_invalid` — the assignment or task identity is missing, malformed, ambiguous, cannot be tied to its contract, or attributes dirty paths this workspace cannot read.
- `draft_required` — a required plan or exact passing plan review is missing or stale, or a finding or a necessary change found during implementation changes plan scope or approach.
- `workspace_not_ready` — required branch state is dirty, missing, ambiguous, or diverged.
- `configuration_required` — Tune needs interactive operator answers this run cannot supply.
- `configuration_unresolved` — Tune ended without done for another cause; the detail quotes Tune's terminal line.
- `implementation_blocked` — the passed plan cannot be implemented or verified from current repository evidence.
- `product_decision_required` — an unsettled behavior-changing owner decision is required.
- `review_target_mismatch` — a remediation report does not cover the task and exact implementation head.
- `authority_drift` — a prepared or ref-bound outward target changed before execution.
- `push_failed` — the canonical remote ref cannot be verified at the local head.
- `pr_failed` — the one exact task PR cannot be created, updated, reconciled, or verified.

A complete Forge report is backend return `report_available`, including when its semantic status is blocked or question. `permission_blocked` is a backend transport return, not a Forge status.
