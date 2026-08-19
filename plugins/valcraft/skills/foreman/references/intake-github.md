# Intake: `project_tracker: github`

Git owns definitions, phase order, and dependency intent (`specs/<NNN>-<feature>/tasks.md`, checkbox-free). GitHub owns open/closed status, discussion, and the labels `in-progress`, `needs-clarification`, `on-hold`, `fast-track`. Issue hierarchy (PRD → spec issue → task sub-issues) and blocked-by links are Spec's projections of git intent — foreman consumes them and never reprojects; a projection gap or unready feature routes to `valcraft:spec`. Bind every `gh` command with `--repo <owner/repo>` from `AGENTS.md`'s `github_repository`; never rely on the current directory.

## Rebuild state

On every command rebuild from GitHub: the spec issue for the feature (from `spec.md`'s `spec_issue`), its task sub-issues, their labels and blocked-by state, and git's `tasks.md` for order. Numbers, titles, labels, state, and relationship fields cover eligibility; read an issue body only when its content is the input to the current step (a PRD being decomposed, a question being routed).

Use `../../spec/references/github-projection.md` as the authority for projected identity and relationship shape. Foreman reads current tracker state only for eligibility and never performs projection reconciliation.

## Batches

Every GitHub write is first serialized as an exact batch — command list with repository, issue numbers, labels, comment bodies — recorded in the summary, then executed per the approval mode. A partial failure stops the batch: report completed operations, reconcile, rebuild the remainder as a fresh batch. Retry only after reconciling, so the retry adopts existing state instead of duplicating.

## Pick

Within the ready feature, take the first task in git `tasks.md` order whose projected issue is open, carries neither `needs-clarification` nor `on-hold`, is not `in-progress`, and has no open blocked-by dependency. Propose it (feature, T-ID, issue number, one-line summary). On confirmation or proceed, record and apply the `in-progress` label as a batch.

## Hold

- A question raised mid-task: record and apply `needs-clarification` with a question comment on the task issue, or `on-hold` when the block is not a question. When project configuration declares `foreman_clarification_assignees`, set the structured assignee field to the one login the question's category maps to (`default` when no category matches); never name assignees in free text. Notification and relayed answers are the tracker side's concern (a bridge, a human); the label is cleared by whoever answers, per the project's convention.
- After a hold, proceed to another task only if the feature still passes the readiness gate — no open behavior-changing question — or the human's explicit acceptance is committed in the feature artifacts. Otherwise stop and report.
- An answer or finding that contradicts the committed spec pauses the task; the spec amendment is committed and referenced from the issue before work resumes, and only then does the foreman record and clear `on-hold`.
- A task the human rejects, or an answer makes unnecessary, closes as `not planned` through an ordinary tracker write batch — the same standing as closing a done task — whose comment names the reason and the deciding answer; if the rejection contradicts the committed spec, the amendment lands first.

## Close a task

There is no checkbox: issue state is completion. After the merge at step 10, record and execute the closing batch — close the issue with a comment naming the merged PR, and remove `in-progress`.

For work completed outside the loop, use `record-and-close.md`. First serialize and
execute the attributed, criterion-keyed evidence comment as its own batch. After the
fresh reviewer reports every criterion sufficient and applicable checks pass against
their real targets, serialize the closing batch: a comment naming the evidence-comment
URL and sufficient verdict, close the issue, and remove `in-progress`. Do not
invent a branch, commit, PR, SHA, or git review target. A partial failure uses the
ordinary reconcile-before-retry rule.

## Deferred cross-task findings

For a finding that `loop.md` routes to a future owner, serialize one comment batch for
the owning task issue. The comment records the finding ID, owner identity, claim, and
source locator. After execution, record the resulting comment URL in `state.md`. Do not
alter the owner issue's status or labels. A future pick verifies that URL from the issue
and passes it to the planner.

## Close a feature

When every child of the spec issue is closed (merged or not planned) and the human confirms, build the feature-close batch (close the spec issue; close the PRD issue when one exists). The batch quotes the human's confirming message verbatim; without one it is not built. It waits per the approval mode.

## Post-projection batch (decompose)

Spec projection owns PRD parenting, generated hierarchy and dependencies, and staged clarification metadata. Foreman adds no post-projection decomposition batch. A missing relationship or generated label routes to Spec.

## Fast-track

- Fast-track is unavailable when `foreman_release_branch` is absent. Report that an explicit release branch is required; do not infer the default branch or fall back to an ordinary task PR.
- `fast-track` on a task issue is a request to land the task on `foreman_release_branch`. Read the label's latest add actor (`gh api repos/<owner>/<repo>/issues/<n>/events` or `.../timeline`, filter `labeled` + `fast-track`, last actor) and put it in the approval request; the human's approval is the authorization. An actor the human does not recognize: alert, remove the label only with approval, change nothing about branches.
- An authorized fast-track task branches from current `origin/<foreman_release_branch>`; the worker proves it (`git fetch origin && git merge-base --is-ancestor origin/<release> HEAD`, and `git log origin/<release>..HEAD` shows only the task's own commits) and its governing spec, design, tasks, and ADRs are identical on the release branch. Its PR targets the release branch. If the worker cannot create and prove that base, stop and surface — never fall back to the default branch base. The merge is a release-branch write (its approval-modes row).
- After any commit lands on the release branch (promotion, fast-track, hotfix, tag), a release → default back-merge is required before the next deliver run; check at step 0 and surface it when missing.

## Quick tasks

Quick tasks (`specs/quick/*.md`) track locally in this mode too: apply the "Quick tasks" paragraphs of `intake-local.md` — checkbox status, branch and PR names for in-progress detection, tick-and-push before merge. No spec issue, task issue, label, or closing batch exists for them; `fast-track` is unavailable.

## Trust boundary

`SKILL.md`'s trust boundary and `../../spec/references/github-projection.md`'s untrusted-content rules apply to every read.
