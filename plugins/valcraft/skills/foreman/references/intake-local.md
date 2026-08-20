# Intake: `project_tracker: local`

Git-owned task artifacts define order, dependencies, holds, and completion. Foreman reads them for coordination; producer skills own every artifact write.

## Rebuild and pick

Require feature tasks to use `T-XXX`. Validate quick tasks with [`../../spec/references/quick.md`](../../spec/references/quick.md). Inspect task branches and open PR identities to find in-progress work.

Select the first unchecked task in file order whose dependencies are checked and which is not held. A local pick needs no tracker write; record it in `state.md`. An existing task branch, plan, producer report, or PR resumes through `loop.md`'s named-state map.

Quick runs walk files and tasks in order, use canonical `Q-NNN QT-XXX`, and derive eligibility from quick-file checkboxes only. No GitHub issue, label, or tracker batch exists for quick work.

## Hold

Record an unresolved task question in `state.md` and route it to the operator. Continue to another task only when the feature remains ready or the operator's accepted uncertainty is committed by the artifact owner. A contract-changing answer routes to Spec before delivery resumes. A rejected or unnecessary task changes through an ordinary reviewed Spec or task-artifact change; Foreman never deletes it.

## Land targets

Pass these tracker semantics to Land without copying Land's procedure:

- **Feature task PR:** the selected task's only local completion mutation is its exact unchecked-to-checked transition. Land owns that tick, final-head gates, merge, and reconciliation.
- **Quick task PR:** Land applies the same exact tick to the selected `QT-XXX`. A file whose tasks are all checked is complete without feature confirmation or Temper.
- **External completion:** Land records criterion-keyed evidence beside the selected task, returns the durable Review target, consumes fresh Review sufficiency, and then applies the valid tick and landing operations. Foreman writes and judges none of it.
- **Feature closure:** local mode has no closure write. Tracker-only Land records the exact operator confirmation and reports completion before Temper begins.

Only Land's declared exact completion-tick exception can bypass another scoped Review. Adjacent text remains uncovered. Foreman never edits a task file, creates a PR, runs checks, merges, or ticks completion.

## Deferred findings

For a non-blocking finding owned by another task, have the artifact-producing worker record the R-ID, owner, claim, and source locator beside the owner task through an ordinary reviewed commit. Record the resulting locator in `state.md`. A later Draft assignment receives it only after Foreman verifies the committed artifact.

## Release safety

Local mode has no fast-track label. Without an explicit release branch, release-only flows are unavailable. With one, any release-branch operation remains an operator gate and passes exact target-bound authority to the producer or Land; Foreman performs no write.
