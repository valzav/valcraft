# Spec workspace, delivery, and report contract

This reference owns Spec's workspace, commit, outward-mutation, exact handoff, recovery, and report contracts. Spec runs only under a Foreman assignment. Without an assignment envelope, change nothing and reply with only the line `Status: blocked: assignment_invalid — no Foreman assignment; run valcraft-foreman`.

## Resolve the workspace

Require the assignment's repository, accepted source or artifact, reconciled base SHA, canonical branch, backend identity, and any physical branch. Do not infer a missing field from coordinator state. Record the repository, the base ref and SHA, the canonical Spec branch, the physical branch when present, the current branch and exact HEAD, and the artifact paths. The default branch is `foreman.default_branch` in the resolved configuration; the envelope's base ref carries the same value. When Tune commits a configuration change during this run, use the resulting head as the base; it descends from the assigned base SHA.

For a new contract the envelope names identity `none` and canonical branch `none`. Resolve whether the source resumes an existing contract; otherwise allocate the identity under `feature-contract.md` or `quick.md`. Derive the canonical Spec branch as [`../../valcraft-foreman/references/contracts.md`](../../valcraft-foreman/references/contracts.md#canonical-branches) defines, create it from the base SHA, and report both the identity and the branch. A local `spec/` branch for this artifact that does not descend from the base is stale: report it and leave it untouched.

Reconcile the canonical branch against the base before writing. Resume it when its attributable Spec history is equal to or descends cleanly from the base. Stop with `workspace_not_ready` on dirty state, ambiguous ancestry, or unattributed divergence. Reconcile existing artifacts and commits before writing, and never duplicate a complete local result.

Follow [`../../valcraft-foreman/references/outward-mutation.md`](../../valcraft-foreman/references/outward-mutation.md) for shared-checkout and isolated-workspace rules and for takeover-attributed dirty Spec paths. A configured release branch does not select the base. A Spec PR targets `foreman.default_branch`.

## Amend a landed contract

Once the contract is present on the selected baseline, every later change is an amendment. No remote Spec ref is retained between landings. Spec never merges the baseline into a landed branch.

An amendment lives in one of two places:

- **On the task branch.** A Foreman assignment may name an in-progress task's canonical branch as the canonical branch, its exact plan head as the predecessor, the plan Review report, the Spec-owned R-IDs, and the fallback amendment branch. Write the fix, then apply the scope test to the staged diff. When it passes, commit on the task branch with a subject citing the feature or quick identity, the task identity, and the resolved R-IDs. Report commit target `task branch` and the exact head under `Workspace`. Push the task ref under the grant and open no PR. The task's plan reviewer closes the R-IDs; no separate Spec Review runs.
- **On an amendment branch.** In every other case, including a failed scope test, create the amendment branch from the exact reconciled baseline, commit there, and report commit target `amendment branch`. The ordinary push, PR, Review, and Land flow applies. Land deletes the branch on merge.

The scope test passes when the staged diff is scoped to the assigned task under `feature-contract.md`'s `Amendment scope`. Report the result and the changed hunks under `Workspace`.

## Commit the artifact

The assignment authorizes local creation or resumption of the selected feature triplet or quick file. Stage only Spec-owned artifact paths, inspect the staged diff, and commit each reviewable artifact state. Cite `FEAT-NNN` or `Q-NNN` and resolved R-IDs in the subject. Record the full commit SHA and verify that each reported artifact blob matches it.

An idempotent complete artifact with no revision or mapping delta needs no new commit. Report its existing exact head. Report each artifact's disposition — created, revised, or unchanged — from the staged diff and the baseline commit, never from the intended outcome. An artifact is unchanged only when its content is identical to the baseline; any edit, including a date or metadata field, makes it revised and requires a commit. A failed stage, commit, or resolution is `git_write_failed`.

## Push, PR, and projection

Spec's outward operations are the push of the canonical ref, spec-PR creation or update, and GitHub tracker projection. Follow [`../../valcraft-foreman/references/outward-mutation.md`](../../valcraft-foreman/references/outward-mutation.md) for authority, revalidation, push, PR, partial results, and the codes `authority_drift`, `workspace_not_ready`, `push_failed`, and `pr_failed`.

- **Push and PR.** The dispatch carries the ref-bound producer grant in [`../../valcraft-foreman/references/contracts.md`](../../valcraft-foreman/references/contracts.md#ref-bound-producer-grant). After committing a contract or amendment branch, push its head to the canonical Spec ref and create or update the one spec PR against `foreman.default_branch` in the same assignment. Its title starts with the `FEAT-NNN` or `Q-NNN` it delivers. For commit target `task branch`, push the task ref and open no PR. For a new contract, the grant binds the canonical Spec ref by condition: the ref you derived, observed absent on the remote at push time.
- **Projection.** Tracker projection is outside the grant, because its authority binds an exact preview. Prepare it as `github-projection.md` defines and report it under `Projection` as a prepared continuation with its tracker target, projection revision, issue mappings or verified absence, and exact operation set. Report every projection, prepared or executed, only under `Projection`; `Outward mutations` covers only the push and the PR. Foreman reads `Projection` alone to find a prepared projection. Perform it only when a later assignment grants exact projection authority. A mapping commit after projection is a new head: push it under the grant and report it as the new Review target.

When live resolution of the remote identity or the canonical ref fails, end with `Status: blocked: workspace_not_ready`, keep the local commit as the Review target, and treat a supplied read-only capture as corroboration, never as live resolution. Report the live or unresolved outward fields. Never infer a release branch. `Status: done` means the artifact is committed, pushed, and, for a contract or amendment branch, in its spec PR; a complete contract already present unchanged on the default branch needs no commit, push, or PR. It does not mean Land finalized it.

## Review revision and handoffs

Accept Review findings only when the report names this repository, the exact artifact paths, and the covered full head. Resolve each accepted R-ID against the accepted source and git-owned contract. After the last artifact edit:

1. commit the revised artifact;
2. reconcile tracker projection and update it only with exact projection authority;
3. commit any verified mapping delta;
4. push the head under the grant;
5. update the one spec PR under the grant; and
6. report the final repository, default base ref and SHA, canonical head ref and full SHA, physical branch or `none`, and PR or `none`.

The Review target is the final artifact paths and exact full head. The Land target is the exact repository, base ref and SHA, canonical head ref and SHA, and spec PR identity when one exists. Land target is `none` for commit target `task branch`, which has no spec PR. Spec never invokes Review or Land and never treats its own checks as their verdict.

## Spec report

End every run with this block. Keep headings in order. Use `none` for an empty section. Nothing follows the terminal status line.

```markdown
## Spec report

### Source

### Artifact

### Readiness

### Workspace

### Projection

### Outward mutations

### Finding resolutions

### Review target

### Land target

### Open questions
```

End with exactly one line:

- `Status: done`
- `Status: blocked: <code> — <detail>`
- `Status: question: <code> — <detail>`

Use these stable blocked codes:

- `assignment_invalid` — the envelope, source, artifact, or requested shape is missing, malformed, ambiguous, cannot be tied to its contract, or attributes dirty paths this workspace cannot read.
- `scaffold_invalid` — project framing or tracker metadata fails preflight.
- `configuration_unresolved` — Tune ended without done for a cause this run does not own; the detail quotes Tune's terminal line.
- `feature_identity_invalid` — an existing feature, quick task, task, mapping, or dependency identity is invalid or collides.
- `workspace_not_ready` — the assigned base is unavailable, local state is dirty or diverged, or an outward stage cannot resolve the remote identity or canonical remote head, or finds that the canonical remote head, still at its bound observation, is not an ancestor of the local head.
- `review_target_mismatch` — a revision report does not cover this artifact and exact head.
- `git_write_failed` — an artifact cannot be staged, committed, or resolved at the reported head.
- `authority_drift` — a bound or prepared outward target changed before execution.
- `projection_failed` — an authorized projection failed or cannot be verified.
- `push_failed` — the canonical remote ref cannot be verified at the local head.
- `pr_failed` — the one exact spec PR cannot be created, updated, reconciled, or verified.

Use these stable question codes:

- `source_selection_required` — one source, staged feature, or shape requires an explicit operator selection.
- `configuration_required` — Tune needs interactive operator answers this run cannot supply.
- `product_decision_required` — observable behavior or an acceptance criterion needs an owner answer.
- `owner_decision_required` — a necessary non-product choice needs an owner answer.
- `tracker_target_required` — GitHub mode's target is still `TBD`, and only the operator's selection through Tune can activate it. This code replaces `configuration_required` for a pending target.

Several conditions can hold at once, and the report carries exactly one terminal line. A blocked code for a stage the assignment requested outranks every question code. Among question codes, report the first that holds in this order: `source_selection_required`, `tracker_target_required`, `owner_decision_required`, `product_decision_required`. An unresolved product or owner question that the artifact preserves under its own open-questions heading never displaces a later stage's code; it is terminal only when no other condition holds.

A complete Spec report is backend return `report_available`, including when its semantic status is blocked or question. `permission_blocked` is a backend return, not a Spec status. A coordinator routes declared codes without interpreting the detail and never synthesizes this report.
