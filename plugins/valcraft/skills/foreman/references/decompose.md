# Decompose

Read this for the decompose command ("new PRD #N", "decompose docs/prd.md"). It produces the feature triplet the deliver command consumes. Input: a PRD issue (`github` mode) or a local PRD/plan file that `valcraft:spec` accepts as an explicitly selected source. Derive the source id `<source>` used in worker names and report files: an issue → `prd<N>` (`prd225`); a file → its basename without extension, lowercased, with every character outside `[a-z0-9-]` replaced by `-` (`docs/Q3 PRD.md` → `q3-prd`). Never interpolate a raw path.

1. Spawn `planner-<source>` on the second harness when the backend offers one. Send:

   > Run `valcraft:spec` with `<source>` as the explicitly selected source to create the next feature spec under `specs/`. Then continue with `valcraft:cast` to stage `design.md`, `tasks.md`, and the tracker projection. Write every proposal and mutation preview Cast builds to your report file as you go, each marked `recorded — proceeded` or `waiting`. Where Cast waits under the project's `cast_approval` declaration, stop after writing it; resume only when the foreman relays the decision. Each task in `tasks.md` states what it covers from the source by `FR-`/`AC-` ID. A task you cannot fully specify keeps its open question in the spec and stages a clarification for its tracker item.

2. Answer the approval points Cast raises (which ones depends on `cast_approval` — `templates/project-block.md`) per the approval-modes table: on the foreman's own judgement when the proposal follows from the source and repository facts; relay a proposal that changes product intent, invents an unstated requirement, or that the foreman would have to guess about. Record every decision in the summary. Deliver each answer as a new assignment to the same planner when the backend can answer a waiting worker, or as a respawn with the decision included when it cannot.
3. After the projection completes, apply the tracker's post-projection batch per `references/intake-github.md` (parenting, staged clarifications). `local` mode has none.
4. Have the planner open the spec PR (feature triplet plus `tasks.md` references) against `foreman_default_branch`. Spawn a fresh `reviewer-<source>`. Send:

   > Run `valcraft:review` in plan mode on the feature triplet `specs/<feature>/spec.md`, `design.md`, and `tasks.md` at the head of branch `<spec PR branch>` (pull request `<n>` of `<owner/repo>` is context, not the target), against `<source>`.

   Material findings go back to the planner for remediation with commits citing the R-IDs, then `references/review-round.md` applies with `reviewer-<source>` as the reviewer. Merge only when no material finding is open. Post the summary, then merge the spec PR (foreman merges; the release-branch and mode rules above apply).

5. Report: feature ID and paths, tracker references, tasks with their clarification state, review outcome. End the run — clarification can take days; deliver starts only on the human's command.
