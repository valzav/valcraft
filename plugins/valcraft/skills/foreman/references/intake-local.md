# Intake: `project_tracker: local`

Git is the only tracker. `specs/<NNN>-<feature>/tasks.md` holds checkbox tasks; an unchecked `- [ ] T-XXX …` item is available work. No GitHub CLI, remote issue, or authentication is required; a git remote is required only for the PR steps.

## Rebuild state

Read `tasks.md` of the selected feature. Read `git branch --list 'feat/*'` and `gh pr list --state open --json number,headRefName,title` (when a remote exists) to detect in-progress tasks: a task branch or open PR whose name carries `<feature>-<task>` marks that task in progress.

## Pick

Take the first unchecked task in file order whose every `blocked by T-XXX` annotation names a checked task, and which is not held (below). Propose it. Marking in progress: none — the branch created at step 6 is the marker; before that, the run directory's `state.md` records the picked task.

## Hold

- A question raised mid-task that the spec, design, or plan does not answer: record it in the run directory's `state.md` (`held: <T> — <question>`), leave the task unchecked, and route the question to the human. Proceed to another task only if the feature still passes the readiness gate — no open behavior-changing question — or the human's explicit acceptance of the uncertainty is committed in the feature artifacts. Otherwise stop and report.
- An answer that contradicts the committed spec pauses the task; the spec amendment lands as its own reviewed change and is referenced from the plan before work resumes.
- A task the human rejects, or an answer makes unnecessary, is removed from `tasks.md` by an ordinary reviewed change that names the reason; the foreman does not delete tasks itself.

## Close a task

At step 10, before the merge: the worker ticks the task's box in `specs/<feature>/tasks.md` (`- [x] T-XXX …`), commits that on the PR branch with a subject citing the T-ID, and pushes. `valcraft:forge` leaves the tick to the loop. Then the foreman merges.

## Close a feature

When every task is checked or removed and the human confirms, the feature is closed by the human's confirmation recorded in the summary. No file changes.

## Quick tasks

The quick pool is `specs/quick/*.md` (`../../cast/references/quick.md`); each file is its own contract with its own `## Tasks` checkboxes.

- **Rebuild state**: read every quick file in number order; detect in-progress work by branches and open PRs named `q<NNN>-t<XXX>`.
- **Pick**: the first unchecked task, walking files in number order and tasks in file order, whose `blocked by T-XXX` annotations name checked tasks of the same file, and which is not held. Propose it as `Q-<NNN> T-<XXX>` with the file path and a one-line summary.
- **Hold**: as above; `state.md` records `held: Q-<NNN> T-<XXX> — <question>`. An answer that contradicts the file's `Requirements` amends the file in its own reviewed change before work resumes.
- **Close a task**: the worker ticks the box in the quick file, commits on the PR branch citing `Q-<NNN> T-<XXX>`, and pushes; then the foreman merges. A file whose every task is ticked is done — no confirmation, no retrospective.

## Fast-track

Not applicable: local mode has no label channel. A change that must reach `foreman_release_branch` directly is a human instruction to the foreman (release-branch row of the approval-modes table).
