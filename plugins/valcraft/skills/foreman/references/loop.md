# The delivery loop

This reference owns the loop steps in full. `SKILL.md` summarizes them; when they differ, this file wins. Every "send" below is an assignment envelope from `references/contracts.md`; every "await" is the backend's `await` primitive followed by the report check in `references/backends/README.md`.

Two commands enter the loop:

- **deliver** — "start sprint", "run the delivery loop", "work through feature NNN": steps 0–10 below, one task at a time, serially.
- **decompose** — "new PRD #N", "decompose docs/prd.md": the decomposition flow at the end of this file, which produces the feature triplet the deliver command consumes.

Start only on the human's explicit command. Never auto-start on a new issue, a cleared label, or a merged PR.

## Deliver

Rebuild state first: the tracker's view of the feature (per `references/intake-<mode>.md`), git's `tasks.md` for order, and the run directory for reports already written.

### 0. Resume or ready

- If a task is in progress (tracker label in `github` mode; an unmerged task branch or open task PR in `local` mode), resume it at the step its evidence shows: a plan without a review report → step 3; a review report without a forge handoff → step 4 or 6; a forge handoff without a PR → step 7; an open PR → step 8 or 9. Never restart from step 2 when a plan of record exists.
- Otherwise apply Cast's implementation-readiness gate (`../../cast/references/spec-intake.md`): substantive `design.md` and `tasks.md`, and no open product question that can change observable behavior or an acceptance criterion — unless the human has explicitly accepted that uncertainty for the affected scope in the committed feature artifacts. An unready feature stops the run: report the blocking question or artifact.
- Never interleave tasks from a different feature inside one deliver run.

### 1. Pick

Take the first eligible task per the intake reference — `tasks.md` order, dependencies satisfied, not held. Propose it (feature, T-ID, tracker reference, one-line summary). `attended`: wait for confirmation. `gated` and `delegated`: proceed, unless the human said "confirm picks" for this run. On confirmation, mark it in progress per the intake reference.

### 2. Plan

Spawn `planner-<F>-<T>` on the second harness when the backend offers one. Send:

> Write an implementation plan for task `<T>` of `specs/<feature>/tasks.md` (tracker ref `<n>` when one exists), against `specs/<feature>/spec.md` and `design.md`. Planning only — do not implement and do not edit source. Write the plan as a tracked document in `docs/plans/` per the repository convention. Then run `valcraft:msw` on that plan file. Report the plan's absolute path.

Await. The report must name the plan path.

### 3. Plan review

Spawn `reviewer-1-<F>-<T>`. Send:

> Run `valcraft:review` in plan mode on the implementation plan at `<absolute plan path>` for task `<T>` of `specs/<feature>/tasks.md`, against `specs/<feature>/spec.md` and `design.md`.

Await. The report must be the full review contract; a verdict-only report is rejected and re-requested.

### 4. Address

Spawn `worker-<F>-<T>`. Send:

> Take the plan document at `<absolute plan path>` as the plan of record. If your workspace is a separate worktree, copy it to the same repository-relative path in your worktree first. Address each finding by R-ID in the review report at `<review report path>`, update the plan, and report the plan's absolute path and each R-ID's resolution.

The planner has no further work; release it per the backend (or leave it idle until step 10 cleanup when release is not immediate).

### 5. Iterate

Apply "After a review round" (below) to the round-one report and the worker's resolution list: a closure check by `reviewer-1-<F>-<T>` on the resolved R-IDs, and a full second round only when a trigger fires. Then post the summary — plan path, resolved R-IDs, open findings, and whether the loop is proceeding or waiting — and apply the proceed/wait test:

- **Proceed to step 6** when every remaining finding is one the foreman's judgement settles: wording, a scoping call the spec or design already answers, a finding the worker already resolved, or a preference that does not change the plan's approach. Record the decision in the summary.
- **Wait for the human** when a significant finding remains: a conflict with the spec or design, a change to the task's scope or approach, an unresolved risk, or anything the foreman would have to guess about. Name the finding.

In `attended` mode the summary always waits.

### 6. Implement

Send `worker-<F>-<T>`:

> Run `valcraft:forge` for task `<T>` of `specs/<feature>/tasks.md` (tracker ref `<n>` when one exists) with the plan at `<plan path>`. Branch `<branch name>` from `origin/<foreman_default_branch>`. Reference `<T>` and the covered `FR-`/`AC-` IDs in commit subjects.

Await. Forge ends at its review handoff; the report is the full handoff block. If forge stops on a question the spec and design cannot answer, go to held-task handling in the intake reference. If the backend reports the worker blocked on a prompt, apply the blocked-worker rule in `references/backends/README.md`.

### 7. PR

When the forge handoff is complete and its verification evidence is present, send the worker:

> Push your branch and open a pull request against `<foreman_default_branch>` with `gh pr create`. Title: `<T>: <summary>`. Body: the `FR-`/`AC-` IDs covered and the plan path, written under the MSW deletion test. Report the PR URL.

Then perform the backend's PR-tracking hook if it declares one.

### 8. PR review

Spawn `reviewer-2-<F>-<T>` on the second harness when the backend offers one. Send:

> Run `valcraft:review` in code mode on PR `<n>` of `<owner/repo>` for task `<T>` of `specs/<feature>/tasks.md` — the pinned review target named in the forge handoff at `<handoff path>`.

Await. Full review contract required.

### 9. Fix

Send the worker the review report path and require resolution by R-ID (a remediation plan in `docs/plans/` for material findings, resolution commits citing the R-IDs). Then apply "After a review round" (below): a closure check by `reviewer-2-<F>-<T>` on the resolved R-IDs, and a full second round only when a trigger fires. CI failures on the PR go to the worker with the failing check name; intervene only when the worker stalls.

### 10. Merge and close

Post the summary — PR link, CI state, review summary with open and resolved R-IDs, residual risks — and apply the proceed/wait test:

- **Merge without waiting** when the task is fully implemented against its spec and design, CI is green, and every finding from steps 8 and 9 is resolved or is one the foreman's judgement settles. Record the decision.
- **Wait for the human** when anything remains unsettled: CI red, still running, or never ran; a review finding open or deferred; the implementation diverged from the plan's approach; the change reaches outside the task's scope; a new issue the plan did not anticipate. Name it.

In `attended` mode the summary always waits. A PR against `foreman_release_branch` waits in every mode.

To merge, in this order:

1. `local` intake only: the worker ticks the task's checkbox in `tasks.md`, commits, and pushes on the PR branch (`references/intake-local.md`, "Close a task"). Wait for that push before merging.
2. The foreman runs `gh pr merge <n> --repo <owner/repo> --squash --delete-branch` itself. Never route the merge through a worker: worker permission classifiers deny it, and a denied merge is reported with the exact command, never retried or worked around.
3. `github` intake only: record and execute the closing batch (`references/intake-github.md`, "Close a task").
4. Release all four workers per the backend. Return to step 1.

When every task of the feature is closed (merged or not planned) and the human confirms the feature, close the feature per the intake reference — the closing batch quotes the human's confirming message verbatim, and without one it is not built.

## After a review round

Steps 5 and 9 (and decompose step 4) share this procedure. One review round is the default; a second full round is the exception, and two is the cap (`references/hygiene.md`).

A round-one verdict of **pass** needs nothing more: proceed. **blocked** is not a round — apply the report check in `references/contracts.md`. On **material findings**, after the worker's resolution report:

1. **Closure check.** Send the same reviewer the worker's resolution report path and the R-IDs it claims resolved: "Re-run the reproduction from each listed R-ID's evidence cell against the remediated artifact and record the new output in its resolution column (`valcraft:review` rule 6). Review nothing else. Report the table with the updated resolution column and the `Status:` line." This is a closure check, not a review round: it opens no new findings, and a finding whose re-run still fires stays open. Without it, closure rests on the implementer's own claim, which the invariant forbids.
2. **Second full round — only when a trigger fires.** Send the reviewer the updated artifact for a complete `valcraft:review` pass when round one or the resolution shows any of:
   - three or more P1 findings in round one (authority: the owner's rule for this loop, 2026-08-16);
   - the resolution reached beyond the findings — a resolution commit or plan edit touches a file, module, or plan step that no round-one R-ID's evidence cell cites, or the plan's approach changed;
   - the worker declined or deferred a material R-ID (resolution other than fixed) — the reviewer holds the evidence and adjudicates, not the foreman;
   - a round-one P1 on a trust boundary, a security or permission check, data loss, or a migration;
   - the resolution added a dependency, replaced (not added) a test, or changed CI configuration to go green.

   Findings from round two go to the worker once more, followed by a closure check — except a finding the worker declined and round two upheld, which is a disagreement the human settles: escalate at once. A material finding still open after the closure check is also an escalation. The foreman never runs a third round and never decides a material finding itself.

3. **Otherwise** the closure check's table is the round's final state: proceed to the step's summary and proceed/wait test.

Record which branch applied and why in the summary and in `state.md`.

## Decompose

Input: a PRD issue (`github` mode) or a local PRD/plan file that `valcraft:spec` accepts as an explicitly selected source. Derive the source id `<source>` used in worker names and report files: an issue → `prd<N>` (`prd225`); a file → its basename without extension, lowercased, with every character outside `[a-z0-9-]` replaced by `-` (`docs/Q3 PRD.md` → `q3-prd`). Never interpolate a raw path.

1. Spawn `planner-<source>` on the second harness when the backend offers one. Send:

   > Run `valcraft:spec` with `<source>` as the explicitly selected source to create the next feature spec under `specs/`. Then continue with `valcraft:cast` to stage `design.md`, `tasks.md`, and the tracker projection. At each Cast operator-approval point, write the exact proposal to your report file and stop; resume only when the foreman relays the decision. Each task in `tasks.md` states what it covers from the source by `FR-`/`AC-` ID. A task you cannot fully specify keeps its open question in the spec and stages a clarification for its tracker item.

2. Answer Cast's approval points on the foreman's own judgement when the proposal follows from the source and repository facts; relay to the human only a proposal that changes product intent, invents an unstated requirement, or that the foreman would have to guess about. In `attended` mode relay every proposal. Record every decision in the summary. Deliver each answer as a new assignment to the same planner when the backend can answer a waiting worker, or as a respawn with the decision included when it cannot.
3. After the projection completes, apply the tracker's post-projection batch per `references/intake-github.md` (parenting, staged clarifications). `local` mode has none.
4. Have the planner open the spec PR (feature triplet plus `tasks.md` references) against `foreman_default_branch`. Spawn a fresh `reviewer-<source>`. Send:

   > Run `valcraft:review` in plan mode on the feature triplet `specs/<feature>/spec.md`, `design.md`, and `tasks.md` at the head of branch `<spec PR branch>` (pull request `<n>` of `<owner/repo>` is context, not the target), against `<source>`.

   Material findings go back to the planner for remediation with commits citing the R-IDs, then "After a review round" applies with `reviewer-<source>` as the reviewer. Merge only when no material finding is open. Post the summary, then merge the spec PR (foreman merges; the release-branch and mode rules above apply).

5. Report: feature ID and paths, tracker references, tasks with their clarification state, review outcome. End the run — clarification can take days; deliver starts only on the human's command.
