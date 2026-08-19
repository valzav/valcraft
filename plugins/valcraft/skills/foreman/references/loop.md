# The delivery loop

This reference owns the loop steps in full. `SKILL.md` summarizes them; when they differ, this file wins. Every "send" below is an assignment envelope from `references/contracts.md`; "await; report check" is the backend's `await` primitive followed by the completeness check in `references/contracts.md` (a report that fails it is re-requested per "Rejection").

Two commands enter the loop:

- **deliver** — "start sprint", "run the delivery loop", "work through feature NNN": steps 0–10 below, one task at a time, serially. "deliver quick" / "work through the quick tasks" runs the same steps over the quick pool `specs/quick/` (below).
- **decompose** — "new PRD #N", "decompose docs/prd.md": `references/decompose.md`, which produces the feature triplet the deliver command consumes.
- **record and close** — an explicit report that one open task was completed outside
  the loop: use `references/record-and-close.md`, then return to step 0.

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

Rebuild state first: the run directory for reports already written, then the tracker's
view of the feature (per `references/intake-<mode>.md`) and git's `tasks.md` for order.
Verify every resumed pointer and SHA against its authority before using it.

### 0. Resume or ready

- Recover the checkout expected by `state.md`. On a shared-checkout backend, inspect the
  current branch, exact HEAD, and staged, unstaged, and untracked state before any fetch,
  switch, synchronization, or task-branch creation. Any staged, unstaged, or untracked
  change stops: preserve it, record the paths, attribution when known, and checkout
  state, then wait. Do not clean, stash, reset, switch, or create a branch. Attribution
  does not waive this task-start gate; dead-worker recovery remains the separate backend
  rule. A clean checkout may switch to the expected branch.
- Before picking a new task, switch the clean checkout to `foreman_default_branch`,
  fetch its remote, and record the exact local and `origin/<foreman_default_branch>`
  SHAs. A missing ref or failed fetch stops. Classify their ancestry:
  - **equal** — record the common SHA and proceed;
  - **origin-ahead** — fast-forward the clean local default branch, verify both refs now
    identify the same commit, record it, and proceed;
  - **local-ahead** — wait before pushing. A push always needs an explicit operator
    instruction that names this default-branch push; neither approval mode supplies it.
    With that authority, push, verify both refs identify the same commit, and record it;
  - **diverged** — stop without merging, rebasing, resetting, force-pushing, or creating
    a task branch.
  Attended and unattended modes authorize only the operations listed in
  `references/approval-modes.md`; they do not alter this classification.
- If a task is in progress (tracker label in `github` mode; an unmerged task branch or open task PR in `local` mode), resume it at the step its evidence shows: a plan without a review report → step 3; a review report without a forge handoff → step 4 or 6; a forge handoff without a PR → step 7; an open PR → step 8 or 9; a feature closed in this run without a `temper-<F>` report → step 11. Never restart from step 2 when a plan of record exists.
- Otherwise apply Cast's implementation-readiness gate (`../../cast/references/spec-intake.md`): substantive `design.md` and `tasks.md`, and no open product question that can change observable behavior or an acceptance criterion — unless the human has explicitly accepted that uncertainty for the affected scope in the committed feature artifacts. An unready feature stops the run: report the blocking question or artifact.
- Never interleave tasks from a different feature inside one deliver run; a quick run takes only quick files, a feature run only its feature.

### 1. Pick

Take the first eligible task per the intake reference — `tasks.md` order, dependencies satisfied, not held. Propose it (feature, T-ID, tracker reference, one-line summary); wait or proceed per the approval-modes table (the human's "confirm picks" makes this row wait for the run). Record the reconciled default-branch SHA as this task's branch base. Then mark it in progress per the intake reference.

### 2. Plan

Spawn `planner-<F>-<T>` on the second harness when the backend offers one. Send:

> Write an implementation plan for task `<task identity>` of `specs/<feature>/tasks.md` (tracker ref `<n>` when one exists), against `specs/<feature>/spec.md` and `design.md`. Planning only — do not implement and do not edit source. Write the plan as a tracked document in `docs/plans/` per the repository convention. Preserve the semantic plan type and slug; never add `quick` solely for a quick task. Then run `valcraft:msw` on that plan file. Report the plan's absolute path.

When the selected task owns deferred finding locators, append their verified tracker
locations to this envelope as named task-contract artifacts. The planner must address
each finding or state why the current committed contract settles it. Never pass only a
`state.md` pointer; verify the durable record from `tasks.md`, the quick file, or the
task issue after every restart.

Await; report check. The report names the plan path.

### 3. Plan review

Spawn `reviewer-1-<F>-<T>`. Send:

> Run `valcraft:review` in plan mode on the implementation plan at `<absolute plan path>` for task `<task identity>` of `specs/<feature>/tasks.md`, against `specs/<feature>/spec.md` and `design.md`.

Await; report check.

### 4. Address

Spawn `worker-<F>-<T>`. Send:

> Establish or resume task branch `<branch name>` from the reconciled default-branch commit `<SHA>` recorded for this task before editing. Take the plan document at `<absolute plan path>` as the plan of record. If your workspace is a separate worktree, copy it to the same repository-relative path in your worktree first. Address each finding by R-ID in the review report at `<review report path>`, update the plan, and commit the resolution changes on the task branch. Report the plan's absolute path and one line per R-ID: resolving commit, repository-relative file-and-line locator, and concise claim. Do not copy a hunk or before-and-after text.

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

Read the exact PR head SHA, record it as the pinned review target in `state.md`, and
include it in the assignment. Do not infer the target from a branch name alone.

Spawn `reviewer-2-<F>-<T>` on the second harness when the backend offers one. Send:

> Run `valcraft:review` in code mode on PR `<n>` of `<owner/repo>` at exact head `<SHA>` for task `<task identity>` of `specs/<feature>/tasks.md` — the pinned review target named in the forge handoff at `<handoff path>`.

Await; report check. A passing review records this SHA as the reviewer-covered SHA;
later heads remain uncovered until step 10 applies the exact-final-head gate.

### 9. Fix

Send the worker the review report path and require resolution by R-ID (a remediation plan in `docs/plans/` for material findings, resolution commits citing the R-IDs). Each resolution line names the R-ID, resolving commit, repository-relative file-and-line locator, and concise claim; it contains no copied hunk or before-and-after text. Then apply `references/review-round.md`: a closure check by `reviewer-2-<F>-<T>` on the resolved R-IDs, and a full second round only when a trigger fires. Failures from applicable PR checks go to the worker with the failing check name; intervene only when the worker stalls.

## Cross-task finding routing

At any review or evidence gate, identify the task whose contract owns each finding. A
finding against another task lands in the current work only when either causal test is
true:

1. the current diff caused the inconsistency; or
2. the owning contract blocks the current task from satisfying its own contract.

Record the owner and the passing test in `state.md`. Remediation that lands now follows
the ordinary R-ID resolution, closure check, second-full-round triggers, exact-final-head,
and applicable-check gates. Cross-task ownership, adjacency, or a small edit changes no
gate.

When neither test passes, do not remediate the finding now. Record its ID, owner, claim,
and source locator in the owner task's tracker-owned artifact according to the intake
reference, then record that durable locator in `state.md`. The current local worker
commits a local or quick tracker entry; the foreman uses a serialized issue-comment
batch in GitHub mode. On a later pick, verify the tracker record from its authority and
include its locator in the planner envelope as required in step 2. This rule survives a
run restart; the checkpoint alone is never the durable record.

Once the durable owner record is verified, classify the non-blocking cross-task finding
as deferred to its owner and settled for the current task. It does not block the current
task's exact-final-head or proceed decision. A missing or unverified durable record
remains an open finding.

### 10. Merge and close

For `local` intake, first have the worker perform its close-task write from
`references/intake-local.md`: change only the selected task's checkbox from unchecked
to checked, commit, and push. Wait for the push, then run the final-head gate below.

#### Exact-final-head gate

Read and record the exact current PR head and the reviewer-covered SHA. Compare the
complete delta between them. Only one delta may bypass another scoped review: in
`local` intake, the exact unchecked-to-checked transition of the selected task's own
checkbox. Adjacent text, documentation, a rename, generated output, a merge, or any
other delta is uncovered. Send the exact `<reviewer-covered SHA>..<current head>` delta
to `reviewer-2-<F>-<T>` for scoped code review, then apply step 9 and
`references/review-round.md` to any finding. Do not infer safety from a change-type
allow-list, diff statistics, file type, generation status, or merge provenance.
When a PR has no reviewer-covered SHA, obtain an initial code review pinned to its exact
head. After any review-driven change, re-read the head and apply this comparison again;
an earlier review cannot cover the new delta.

For the resulting head, classify applicable checks from all of these sources:

- the selected task's requirements;
- repository rules;
- externally configured required checks; and
- workflows present on the default branch or introduced by the PR.

Query every source. If any repository-rule, external-required-check, or applicable
workflow source is unavailable, stop before assigning a check state. Default-branch
workflow absence alone never proves that no check applies. Match results to the exact
current head; a result for an older SHA is evidence only for that older SHA.

Record exactly one check state:

- **passing** — every applicable configured or required check passed on the exact head;
- **pending/failing** — an applicable check is running or failed on the exact head;
- **missing-required** — a configured or required applicable check has no run for the
  exact head; or
- **none-applicable** — every source was queried and none configures or requires a
  check for the change.

`pending/failing` and `missing-required` wait before merge. `passing` and
`none-applicable` satisfy the check gate; `none-applicable` does not create a separate
approval path. Do not invent a universal CI gate. Advance the reviewer-covered SHA to
the exact final head only after the scoped review passes, or the exact local checkbox
exception applies, and the final head's check state is `passing` or `none-applicable`.

This classifier is the shared merge gate for normal task PRs, record-and-close, and
step 11 retrospective PRs. In a tracker-only record-and-close path with no real git
target, record the authoritative probes that established its absence and do not invent
a head; the evidence-sufficiency gate replaces code review, while every applicable
check still runs against its real target. The no-git branch passes only when those
probes establish absence and no applicable check requires a git target.
`record-and-close.md` owns that behavior.

Post the summary — PR link, exact final SHA, check state and sources, review summary
with open and resolved R-IDs, reviewer-covered SHA, and residual risks — and apply the
proceed/wait test:

- **Proceed** when the task is implemented against its spec and design, review and a
  `passing` or `none-applicable` check state cover the exact final head, and every
  finding from steps 8 and 9 is either resolved or is a verified, non-blocking
  cross-task deferral settled under the causal-routing rule. Record the decision
  against that SHA.
- **Wait** when anything is unsettled and settling it would take the human — a
  `pending/failing` or `missing-required` check state; an unavailable applicability
  source; an open current-task or blocking finding; a non-blocking cross-task deferral
  without a verified durable owner record; the implementation diverged from the plan's
  approach or scope; an issue the plan did not anticipate. Name it.

The approval-modes table says whether a "proceed" executes without the human; a PR against `foreman_release_branch` is its own row.

To merge, in this order:

1. Re-read the PR head immediately before merge. If it differs from the recorded exact
   final SHA, return to the exact-final-head gate.
2. The foreman runs `gh pr merge <n> --repo <owner/repo> --squash --delete-branch` itself — never through a worker (their permission classifiers deny it). A denied merge is reported with the exact command and waits for the human; it is never retried or worked around.
3. `github` intake only: record and execute the closing batch (`references/intake-github.md`, "Close a task").
4. Release the task's workers per the backend. Return to step 0 before the next pick.

When every task of the feature is closed (merged or not planned) and the human confirms the feature, close the feature per the intake reference — the closing batch quotes the human's confirming message verbatim, and without one it is not built. Then run step 11. A quick file needs neither: its last tick closes it, and the run moves to the next quick file.

### 11. Temper

Once per feature, after the feature closes — never per task, never per quick file (`valcraft:temper` runs at milestones; quick work is retrospected on demand over `specs/quick/`). Spawn `temper-<F>`. Send:

> Run `valcraft:temper` in analyze mode on the feature directory `specs/<feature>/` (tracker refs `<n…>` when they exist). Then commit the report it created under `docs/retro/` on branch `retro/<f>-<slug>` from `origin/<foreman_default_branch>` and open a pull request against `<foreman_default_branch>` with `gh pr create`; title `Retro: <feature>`; body: the report path and one line per routed proposal (tier, `L-NNN`, rule statement). Do not apply any proposal. Report the report path, the PR URL, and the proposal lines.

Await; report check. Post the summary — report path, PR link, proposals by tier — and
apply step 10's exact-final-head review and check classifier to the report PR. Merge it
under the step 11 approval-modes row only when that shared gate passes. The proposals
are for the human: the foreman never edits `AGENTS.md`, a user artifact, or a plugin
from them. Release the temper worker; report the run's end (`SKILL.md`, "Report").
