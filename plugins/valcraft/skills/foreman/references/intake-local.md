# Intake: `project_tracker: local`

Git is the only tracker. `specs/<NNN>-<feature>/tasks.md` holds checkbox tasks; an unchecked `- [ ] T-XXX …` item is available work. No GitHub CLI, remote issue, or authentication is required; a git remote is required only for the PR steps.

## Rebuild state

Read `tasks.md` of the selected feature. Require every feature task to use `T-XXX`;
stop on any other task prefix, including `QT-XXX`. Read `git branch --list 'feat/*'`
and `gh pr list --state open --json number,headRefName,title` (when a remote exists) to
detect in-progress tasks: a task branch or open PR whose name carries
`<feature>-<task>` marks that task in progress.

## Pick

Take the first unchecked task in file order whose every `blocked by T-XXX` annotation names a checked task, and which is not held (below). Propose it. Marking in progress: none — the branch created at step 6 is the marker; before that, the run directory's `state.md` records the picked task.

## Hold

- A question raised mid-task that the spec, design, or plan does not answer: record it in the run directory's `state.md` (`held: <T> — <question>`), leave the task unchecked, and route the question to the human. Proceed to another task only if the feature still passes the readiness gate — no open behavior-changing question — or the human's explicit acceptance of the uncertainty is committed in the feature artifacts. Otherwise stop and report.
- An answer that contradicts the committed spec pauses the task; the spec amendment lands as its own reviewed change and is referenced from the plan before work resumes.
- A task the human rejects, or an answer makes unnecessary, is removed from `tasks.md` by an ordinary reviewed change that names the reason; the foreman does not delete tasks itself.

## Close a task

At step 10, before the final-head gate and merge, the worker changes only the selected
task's box in `specs/<feature>/tasks.md` from unchecked to checked
(`- [x] T-XXX …`), commits that on the PR branch with a subject citing the T-ID, and
pushes. `valcraft:forge` leaves the tick to the loop, and the worker retains ownership
of this write. Only that exact transition may bypass another scoped review. Adjacent
text or any other delta follows `loop.md`'s exact-final-head gate. Then the foreman
merges.

For work completed outside the loop, use `record-and-close.md`. The recorder stores
the criterion-keyed `Completion evidence` block directly beneath the selected task,
then the fresh evidence reviewer returns a sufficient verdict before the recorder may
tick it. The evidence write is part of the task PR and receives the shared scoped-review,
exact-final-head, and applicable-check gates.

## Close a feature

When every task is checked or removed and the human confirms, the feature is closed by the human's confirmation recorded in the summary. No file changes.

## Quick tasks

The quick pool is `specs/quick/*.md` (`../../spec/references/quick.md`); each file is its own contract with its own `## Tasks` checkboxes.

- **Rebuild state**: validate every quick file against `quick.md` before eligibility. Stop on a legacy or mixed prefix, malformed ID, wrong-prefix dependency, missing referenced Q file or QT-ID, or `QT-XXX` in feature `tasks.md`. Read valid quick files in number order; detect in-progress work by branches and open PRs named `qNNN-qtNNN`.
- **Pick**: walk files and tasks in order. Pick the first unchecked `QT-XXX` whose local `blocked by QT-XXX` and cross-file `blocked by Q-NNN QT-XXX` targets are checked and which is not held. In every tracker mode, read status only from quick-file checkboxes and perform no quick-task issue lookup. Propose the canonical `Q-NNN QT-XXX` identity, file path, and summary. A bare `Q-NNN` selects that file's next eligible task.
- **Hold**: as above; `state.md` records `held: Q-NNN QT-XXX — <question>`. An answer that contradicts the file's `Requirements` amends the file in its own reviewed change before work resumes.
- **Close a task**: the worker changes only the selected quick task's box from unchecked
  to checked, commits on the PR branch citing `Q-NNN QT-XXX`, and pushes. Only that
  exact transition may bypass another scoped review; the final-head check classifier
  still applies. Then the foreman merges. A file whose every task is ticked is done —
  no confirmation, no retrospective.
- **Record and close**: store the `Completion evidence` block directly beneath the
  selected `QT-XXX` item in the quick file. Use no feature task or GitHub issue. The
  fresh sufficiency review, exact tick, final-head gate, and applicable checks are the
  same as for a local feature task.

## Deferred cross-task findings

For a finding that `loop.md` routes to a future owner, record one durable entry directly
beneath that owner's task: finding ID, owner identity, claim, and source locator. The
current worker commits this tracker-only record; because it is not the selected task's
exact checkbox transition, the final-head gate reviews its delta. Record its resulting
repository-relative file-and-line locator in `state.md`. Never tick or otherwise change
the owner task. A future pick verifies the entry in the authoritative task artifact and
passes its locator to the planner.

## Fast-track

Not applicable: local mode has no label channel. A change that must reach an explicitly configured `foreman_release_branch` directly is a human instruction to the foreman (release-branch row of the approval-modes table). Without that key, direct release-branch writes are unavailable; do not infer the default branch.
