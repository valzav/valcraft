# Tracker closure

Reconcile live tracker and PR state before preparation, immediately before mutation, after each mutation, and on resume.

## Target kinds

| Target | Valid completion operations |
| --- | --- |
| Task PR | add the exact mode-valid completion tick before the final gate when applicable; merge the reviewed PR; then apply any mode-valid hosted close batch |
| Spec PR | merge the reviewed PR; no task closure |
| Tracker-only feature or PRD | apply only the confirmed tracker close; invent no git target |
| `not planned` task | record the governing reason and close or remove the task as its tracker contract requires; no merge without a real PR |
| External completion | follow `record-and-close.md`, then apply only its real tracker closure |

A closed-unmerged PR never proves task completion. A spec merge never closes an implementation task.

## Tracker-mode closure

Resolve the tracker mode from the root `AGENTS.md` before preparing closure:

- In `local` mode, a selected feature task closes through its exact unchecked-to-checked transition in `tasks.md`. Apply the exception in `final-head-and-checks.md`. Do not prepare a hosted tracker batch.
- In `github` mode, a selected feature task closes through the serialized hosted tracker batch. Do not tick the feature task in `tasks.md`.
- In every tracker mode, a selected `Q-NNN QT-XXX` closes through its exact unchecked-to-checked transition in the quick-task file. Apply the exception in `final-head-and-checks.md`. Do not edit adjacent content or create a hosted quick-task close batch. A completed quick file needs no feature confirmation or retrospective.

For `not planned`, follow the committed tracker contract. Record the deciding reason. Do not invent a task PR or completed implementation.

## Hosted tracker batches

Prepare one ordered, serialized batch before execution. A completed task batch names the merged PR or sufficient external-completion evidence, records the close comment, closes the task, and removes only the applicable in-progress state. A `not planned` batch names the reason and deciding instruction.

Treat every operation as independently reconcilable. If the comment exists but close or label removal failed, resume only the missing operations. If the PR merged but tracker work failed, do not attempt another merge.

Feature or PRD closure requires authoritative proof that its children meet the tracker contract and a trusted operator confirmation for that exact target. Without it, return `operator_confirmation_required`. Quote the confirmation in the prepared close record.

## Merge and recovery

Immediately before merge, re-read the PR identity, base, head, state, merge method, Review coverage, and check state. Then verify the exact trusted target-bound authorization required by `SKILL.md`.

After any merge command error, inspect live PR state before deciding the merge failed. If authoritative state says merged, mark merge complete and advance to remaining closure. If it says open, preserve the exact error and return the remaining operation. A closed-unmerged PR stops task closure.

Persist or report enough state to resume: target kind, exact identifiers, prepared authorization fields, completed operations with authoritative locators, remaining operations, and last error. Never repeat a completed external mutation.
