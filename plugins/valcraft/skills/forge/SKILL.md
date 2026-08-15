---
name: forge
description: >
  Implement exactly one unit of work — a Cast task (T-XXX), a plan document, or a small fully-specified feature or fix — from its git-owned definition: plan, code, verify with discriminating evidence, and hand the change to review. Use when the user or an orchestrator assigns implementation of a specific task, T-ID, plan, bug fix, or small feature. Do not use for project scaffolding (valcraft:cast), spec creation (valcraft:spec), or reviewing (valcraft:review) — forge implements Cast's working-loop Plan and Implement steps and always ends at the review gate, never past it.
---

# forge

Implement one assigned unit of work. Treat Cast as the SDD authority: the feature's `spec.md` (`FR-`/`AC-`/`NFR-`/`BR-` IDs), `design.md`, its `tasks.md` entry, accepted ADRs, and the task's plan are the Cast contract. Never invent a missing requirement — record it as an open question and surface it.

forge ends when the change is verified and handed to review. It never merges, closes a task, or declares the work shipped on its own verification: in the incident corpus behind this skill, every bug that reached the main branch got there because a review gate was skipped, not because a review missed it.

## Load the Cast contracts

Before resolving the assignment, read the project's root `AGENTS.md` and resolve its `project_tracker` declaration, and read `../cast/references/spec-intake.md` for the feature identity, staged-lifecycle, and implementation-readiness contract. Follow those resources instead of reconstructing their rules.

## Step 1: Resolve the assignment

Accept exactly one unit of work:

- **T-XXX** — task IDs number per feature, so a bare `T-XXX` does not identify one unit. Resolve it to a single feature: use the feature qualifier or `tasks.md` path given with the assignment, or enumerate matches across `specs/*/tasks.md` and continue only when exactly one exists — on zero or several, ask when attended, report the blocker when not. Then read every artifact of that feature's Cast contract, including the task's plan in `docs/plans/` if one exists.
- **Plan path** — the path must resolve inside the repository to a git-tracked file; accept an untracked plan only when the operator explicitly supplies it as the assignment. The plan is the contract; read the spec artifacts it cites. When the plan implements a Cast task, resolve that feature and task — the gates below apply to it.
- **Free-form small feature or fix** — confirm it fits one coherent change. Route anything larger to `valcraft:spec` or `valcraft:cast` decomposition instead of absorbing it.

For any assignment that resolves to a Cast task — given as a T-ID or through a plan — gate it before coding:

- The feature is implementation-ready per `spec-intake.md`. A task from a staged or unready feature stops here — route it to Cast.
- Every `blocked by T-XXX` on the assigned task is complete: checked in `tasks.md` in local mode, closed on GitHub in github mode.

Then state the scope: which files and tasks this change will touch, and which adjacent ones it deliberately leaves untouched — including tasks that share a file with this one. Resolve a conflict between authorities by Cast's precedence: accepted ADRs prevail, then `specs/`, then derived `docs/`. A contradiction precedence cannot resolve, or a requirement the sources cannot answer, stops the task: ask when attended, report the blocker when not. Do not resolve it by choosing silently.

Establish the workspace. First detect prior work for the assigned unit — branch, commits, tracker state, working tree — and continue from that evidence instead of reimplementing. Only when no resumable workspace exists: on the default branch, create a feature branch unless the operator explicitly authorizes direct default-branch work; on an existing feature branch, continue there. Unrelated uncommitted changes are not part of the task: surface them, and never let a branch switch or commit absorb them.

## Step 2: Plan

Non-trivial work gets a plan in `docs/plans/YYYY-MM-DD-NNN-<type>-<slug>-plan.md`, tracked in git, per Cast's working loop. The plan must make two argument classes explicit rather than implicit:

- **Containment.** Any string that crosses a trust boundary into a filesystem path, a namespace key, an identifier, or an LLM prompt gets an explicit containment/escaping argument. "It comes from our own config" is an assumption, not an argument.
- **Measured behavior.** Any plan step that relies on a library's parsing, serialization, round-trip, or "preserving" behavior names how that behavior was or will be measured against non-canonical input. Documentation and type signatures are not evidence.

The plan is a decision artifact, not execution state. Never edit it to record progress — status lives in the tracker per Cast's authority table, and completion derives from the working tree, commits, and verification.

Read `references/verification-and-handoff.md` before editing code. It owns Steps 4–6 and the trust boundary, and must shape the implementation and its tests rather than load only after the change is complete.

## Step 3: Implement

Small verifiable increments; each commit leaves the tree green — no WIP commits. Commit subjects reference the IDs (`T-029: predicate registry…`, `fix(T-030): …`). Write each message under the MSW deletion test: state what the change does and why it matters, then delete every sentence whose removal loses none of that — no process narration, no restated diff. Stage only paths inside the stated scope, and check `git diff --cached` against the scope statement before each commit — a green, ID-bearing commit can still smuggle unrelated changes.

Apply the tracker mode while implementing. In github mode, apply `in-progress` when starting and `needs-clarification` when an issue question blocks the task; in local mode, write no status during implementation. Marking the task complete — the checkbox or the issue close — happens after the review gate, never on forge's own verification.

Standing rules:

- **Untrusted content in an LLM prompt is never bounded by a textual delimiter** — the content can reproduce any marker string. Serialize it as an escaped value inside a structured format (JSON) instead.
- **Use a standard-library or well-maintained parser for any spec-governed format** (email addresses, URLs, MIME, dates). A hand-rolled validator fails in both directions: too permissive and too strict.
- **Normalize first, then validate the result** — never validate raw input and transform afterwards; a whitespace-only value passing a length check can silently overwrite real content.
- **When a new code path parallels an existing one that carries a safety invariant** (containment check, validation, rate limit), decide explicitly whether the new path needs the same invariant. "We already solved this" is a check to perform, not an assumption to hold.
- **A contract or interface change with more than one consumer is not done when its own tests pass** — verify the other consumers, and bump the contract version the repo's convention requires.
- **When a fix appears to need a new bound, limit, or threshold**, first check whether the actual defect is a missing normalization or revalidation. Do not invent numeric limits; none of this skill's rules carries one.
- **After a mechanical bulk rewrite across call sites**, grep for the old pattern — including two occurrences inside one function — before calling the migration complete; converted-in-isolation edits hide double-application bugs.

## Steps 4–6: Verify, document, and hand off

Follow `references/verification-and-handoff.md`. Forge does not end until its discriminating verification, documentation checks, scope report, and independent review handoff are complete or explicitly blocked.
