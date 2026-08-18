# The delivery loop

This reference owns the loop steps in full. `SKILL.md` summarizes them; when they differ, this file wins. Every "send" below is an assignment envelope from `references/contracts.md`; "await; report check" is the backend's `await` primitive followed by the completeness check in `references/contracts.md` (a report that fails it is re-requested per "Rejection").

Two commands enter the loop:

- **deliver** — "start sprint", "run the delivery loop", "work through feature NNN": steps 0–10 below, one task at a time, serially. "deliver quick" / "work through the quick tasks" runs the same steps over the quick pool `specs/quick/` (below).
- **decompose** — "new PRD #N", "decompose docs/prd.md": `references/decompose.md`, which produces the feature triplet the deliver command consumes.

Start only on the human's explicit command. Never auto-start on a new issue, a cleared label, or a merged PR.

## Quick tasks

A quick task (`../../cast/references/quick.md`) is one file `specs/quick/<NNN>-<slug>.md` that is its own Cast contract. A quick run walks the quick files in number order, one task at a time, and applies every step below with these substitutions:

- The canonical identity is `Q-NNN QT-XXX`. Derive branches as
  `feat/qNNN-qtNNN-<slug>` and logical worker/report names with
  `QNNN-QTNNN` (`worker-Q007-QT001`). Backend physical handles are mapped
  separately by the backend contract.
- Where a step names `specs/<feature>/spec.md` and `design.md`, or `specs/<feature>/tasks.md`, send the quick file's absolute path instead — it is the spec, the design, and the task list.
- Step 0 readiness is `quick.md`'s readiness rule, applied to the file about to be picked; an unready file stops the run.
- Pick, hold, and close follow the intake reference's quick paragraphs; quick tasks track locally in every tracker mode.
- A quick file whose last task closes is done — no confirmation, no step 11. The run continues with the next quick file and ends when none has an eligible task.

## Deliver

Rebuild state first: the tracker's view of the feature (per `references/intake-<mode>.md`), git's `tasks.md` for order, and the run directory for reports already written.

### 0. Resume or ready

- If a task is in progress (tracker label in `github` mode; an unmerged task branch or open task PR in `local` mode), resume it at the step its evidence shows: a plan without a review report → step 3; a review report without a forge handoff → step 4 or 6; a forge handoff without a PR → step 7; an open PR → step 8 or 9; a feature closed in this run without a `temper-<F>` report → step 11. Never restart from step 2 when a plan of record exists.
- Otherwise apply Cast's implementation-readiness gate (`../../cast/references/spec-intake.md`): substantive `design.md` and `tasks.md`, and no open product question that can change observable behavior or an acceptance criterion — unless the human has explicitly accepted that uncertainty for the affected scope in the committed feature artifacts. An unready feature stops the run: report the blocking question or artifact.
- Never interleave tasks from a different feature inside one deliver run; a quick run takes only quick files, a feature run only its feature.

### 1. Pick

Take the first eligible task per the intake reference — `tasks.md` order, dependencies satisfied, not held. Propose it (feature, T-ID, tracker reference, one-line summary); wait or proceed per the approval-modes table (the human's "confirm picks" makes this row wait for the run). Then mark it in progress per the intake reference.

### 2. Plan

Spawn `planner-<F>-<T>` on the second harness when the backend offers one. Send:

> Write an implementation plan for task `<task identity>` of `specs/<feature>/tasks.md` (tracker ref `<n>` when one exists), against `specs/<feature>/spec.md` and `design.md`. Planning only — do not implement and do not edit source. Write the plan as a tracked document in `docs/plans/` per the repository convention. Preserve the semantic plan type and slug; never add `quick` solely for a quick task. Then run `valcraft:msw` on that plan file. Report the plan's absolute path.

Await; report check. The report names the plan path.

### 3. Plan review

Spawn `reviewer-1-<F>-<T>`. Send:

> Run `valcraft:review` in plan mode on the implementation plan at `<absolute plan path>` for task `<task identity>` of `specs/<feature>/tasks.md`, against `specs/<feature>/spec.md` and `design.md`.

Await; report check.

### 4. Address

Spawn `worker-<F>-<T>`. Send:

> Establish or resume task branch `<branch name>` from `origin/<foreman_default_branch>` before editing. Take the plan document at `<absolute plan path>` as the plan of record. If your workspace is a separate worktree, copy it to the same repository-relative path in your worktree first. Address each finding by R-ID in the review report at `<review report path>`, update the plan, and commit the resolution changes on the task branch. Report the plan's absolute path and one line per R-ID: resolving commit, repository-relative file-and-line locator, and concise claim. Do not copy a hunk or before-and-after text.

The planner has no further work; release it per the backend (or leave it idle until step 10 cleanup when release is not immediate).

### 5. Iterate

Apply `references/review-round.md` to the round-one report and the worker's resolution list: a closure check by `reviewer-1-<F>-<T>` on the resolved R-IDs, and a full second round only when a trigger fires. Then post the summary — plan path, resolved R-IDs, open findings, and whether the loop is proceeding or waiting — and apply the proceed/wait test:

- **Proceed** when every remaining finding is settled by the committed artifacts or by a choice that does not change the plan's approach or scope (wording; a scoping call the spec or design already answers). Record the decision.
- **Wait** when settling a finding would take knowledge only the human has — a conflict with the spec or design, a scope or approach change, an unresolved risk. Name the finding.

The approval-modes table says whether a "proceed" executes without the human.

### 6. Implement

Send `worker-<F>-<T>`:

> Run `valcraft:forge` for task `<task identity>` of `specs/<feature>/tasks.md` (tracker ref `<n>` when one exists) with the plan at `<plan path>`. Resume the existing task branch `<branch name>` and its plan-resolution commit; do not create a second branch or reimplement the remediation. Reference `<task identity>` and the covered `FR-`/`AC-` IDs in commit subjects.

Await; report check. If forge stops on a question the spec and design cannot answer, go to held-task handling in the intake reference; a worker blocked on a prompt follows the blocked-worker rule in `references/backends/README.md`.

### 7. PR

When the forge handoff is complete and its verification evidence is present, send the worker:

> Push your branch and open a pull request against `<foreman_default_branch>` with `gh pr create`. Title: `<task identity>: <summary>`. Body: the `FR-`/`AC-` IDs covered and the plan path, written under the MSW deletion test. Report the PR URL.

Then perform the backend's PR-tracking hook if it declares one.

### 8. PR review

Spawn `reviewer-2-<F>-<T>` on the second harness when the backend offers one. Send:

> Run `valcraft:review` in code mode on PR `<n>` of `<owner/repo>` for task `<task identity>` of `specs/<feature>/tasks.md` — the pinned review target named in the forge handoff at `<handoff path>`.

Await; report check.

### 9. Fix

Send the worker the review report path and require resolution by R-ID (a remediation plan in `docs/plans/` for material findings, resolution commits citing the R-IDs). Each resolution line names the R-ID, resolving commit, repository-relative file-and-line locator, and concise claim; it contains no copied hunk or before-and-after text. Then apply `references/review-round.md`: a closure check by `reviewer-2-<F>-<T>` on the resolved R-IDs, and a full second round only when a trigger fires. CI failures on the PR go to the worker with the failing check name; intervene only when the worker stalls.

### 10. Merge and close

Post the summary — PR link, CI state, review summary with open and resolved R-IDs, residual risks — and apply the proceed/wait test:

- **Proceed** when the task is implemented against its spec and design, CI is green, and every finding from steps 8 and 9 is resolved. Record the decision.
- **Wait** when anything is unsettled and settling it would take the human — CI red, still running, or never ran; a finding open or deferred; the implementation diverged from the plan's approach or scope; an issue the plan did not anticipate. Name it.

The approval-modes table says whether a "proceed" executes without the human; a PR against `foreman_release_branch` is its own row.

To merge, in this order:

1. `local` intake only: the worker ticks the task's checkbox in `tasks.md`, commits, and pushes on the PR branch (`references/intake-local.md`, "Close a task"). Wait for that push before merging.
2. The foreman runs `gh pr merge <n> --repo <owner/repo> --squash --delete-branch` itself — never through a worker (their permission classifiers deny it). A denied merge is reported with the exact command and waits for the human; it is never retried or worked around.
3. `github` intake only: record and execute the closing batch (`references/intake-github.md`, "Close a task").
4. Release the task's workers per the backend. Return to step 1.

When every task of the feature is closed (merged or not planned) and the human confirms the feature, close the feature per the intake reference — the closing batch quotes the human's confirming message verbatim, and without one it is not built. Then run step 11. A quick file needs neither: its last tick closes it, and the run moves to the next quick file.

### 11. Temper

Once per feature, after the feature closes — never per task, never per quick file (`valcraft:temper` runs at milestones; quick work is retrospected on demand over `specs/quick/`). Spawn `temper-<F>`. Send:

> Run `valcraft:temper` in analyze mode on the feature directory `specs/<feature>/` (tracker refs `<n…>` when they exist). Then commit the report it created under `docs/retro/` on branch `retro/<f>-<slug>` from `origin/<foreman_default_branch>` and open a pull request against `<foreman_default_branch>` with `gh pr create`; title `Retro: <feature>`; body: the report path and one line per routed proposal (tier, `L-NNN`, rule statement). Do not apply any proposal. Report the report path, the PR URL, and the proposal lines.

Await; report check. Post the summary — report path, PR link, proposals by tier — and merge the report PR when CI is green (its approval-modes row). The proposals are for the human: the foreman never edits `AGENTS.md`, a user artifact, or a plugin from them. Release the temper worker; report the run's end (`SKILL.md`, "Report").
