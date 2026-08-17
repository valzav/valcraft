---
name: forge
description: >
  Implement one unit of work — a Cast task (T-XXX), a quick task (Q-NNN), a plan document, or a small fully-specified feature or fix — from its git-owned definition: plan, code, verify with discriminating evidence, and hand the change to review. Use when the user or an orchestrator assigns implementation of a task, T-ID, Q-ID, plan, bug fix, or small feature. Not for project scaffolding (valcraft:cast), spec creation (valcraft:spec), or reviewing (valcraft:review) — forge implements Cast's Plan and Implement steps and always ends at the review gate.
---

# forge

Implement one assigned unit of work. Cast is the SDD authority: the feature's `spec.md` (`FR-`/`AC-`/`NFR-`/`BR-` IDs), `design.md`, its `tasks.md` entry — or a quick task's one file `specs/quick/NNN-*.md` — accepted ADRs, and the task's plan are the Cast contract. Never invent a missing requirement — record it as an open question and surface it.

Skill names: `valcraft:<name>` means this plugin's `<name>` skill; a host without the namespace (OpenCode) loads it as `<name>`.

forge ends when the change is verified and handed to review. It never merges, closes a task, or declares the work shipped on its own verification: every bug in its incident corpus reached main through a skipped review gate.

## Load the Cast contracts

Before resolving the assignment, read the project's root `AGENTS.md` and resolve its `project_tracker`; read `../cast/references/spec-intake.md` (feature identity, staged lifecycle, readiness) and, for a quick task, `../cast/references/quick.md`.

## Step 1: Resolve the assignment

Accept exactly one unit of work:

- **T-XXX** — T-IDs number per feature and per quick file, so a bare `T-XXX` names no unit. Resolve it through the feature or `Q-NNN` qualifier or the `tasks.md` / quick file path in the assignment, or by enumerating `specs/*/tasks.md` and `specs/quick/*.md` — continue only on exactly one match; on zero or several, ask when attended, report the blocker when not. A bare `Q-NNN` names that file's next eligible task per `quick.md`; none eligible stops. Then read every artifact of the unit's Cast contract, including its plan in `docs/plans/` if one exists.
- **Plan path** — the path must resolve inside the repository to a git-tracked file; accept an untracked plan only when the operator explicitly supplies it as the assignment. The plan is the contract; read the spec artifacts it cites. When it implements a Cast task, resolve that unit and task — the gates below apply.
- **Free-form small feature or fix** — confirm it fits one coherent change; route anything larger to `valcraft:spec` (quick task or feature).

Gate any assignment that resolves to a Cast task — by ID or through a plan — before coding:

- The feature is implementation-ready per `spec-intake.md` (a quick file: per `quick.md`). A task from a staged or unready unit stops here — route it to Cast.
- Every `blocked by T-XXX` on the task is complete: a quick file's checkbox in every mode; else checked in `tasks.md` in local mode, closed on GitHub in github mode.

Then state the scope: which files and tasks this change touches, and which adjacent ones it deliberately leaves untouched — including tasks that share a file with this one. Resolve a conflict between authorities by Cast's precedence: accepted ADRs, then `specs/`, then derived `docs/`. A contradiction precedence cannot resolve, or a requirement the sources cannot answer, stops the task: ask when attended, else report the blocker.

Establish the workspace. First detect prior work for the unit — branch, commits, tracker state, working tree — and continue from that evidence instead of reimplementing. Only when no resumable workspace exists: on the default branch, create a feature branch unless the operator explicitly authorizes direct default-branch work; on an existing feature branch, continue there. Unrelated uncommitted changes are not the task's: surface them; never let a branch switch or commit absorb them.

## Step 2: Plan

Non-trivial work gets a plan in `docs/plans/YYYY-MM-DD-NNN-<type>-<slug>-plan.md`, tracked in git, per Cast's working loop. Two argument classes are explicit:

- **Containment.** Any string that crosses a trust boundary into a filesystem path, a namespace key, an identifier, or an LLM prompt gets an explicit containment/escaping argument. "It comes from our own config" is an assumption, not an argument.
- **Measured behavior.** Any plan step that relies on a library's parsing, serialization, round-trip, or "preserving" behavior names how that behavior was or will be measured against non-canonical input. Documentation and type signatures are not evidence.

The plan is a decision artifact, not execution state. Never edit it to record progress — status lives in the tracker; completion derives from working tree, commits, and verification.

Read `references/verification-and-handoff.md` before editing code. It owns Steps 4–6 and the trust boundary and must shape the implementation and its tests, not load after the change.

**Progress list.** With a harness task tool (Claude Code `TaskCreate`/`TaskUpdate`, Codex `update_plan`), mirror Steps 1–6: one item per step, `<unit> — <step name>`, one `in_progress` at a time, `completed` when the step's evidence exists. Display only — working tree, commits, and tracker stay authoritative; skip without one.

## Step 3: Implement

Small verifiable increments; each commit leaves the tree green — no WIP. Commit subjects reference the IDs (`T-029: predicate registry…`, `fix(T-030): …`). Write each message under the MSW deletion test: what the change does and why it matters, then delete every sentence whose removal loses none of that — no process narration, no restated diff. Stage only paths inside the stated scope; check `git diff --cached` against it before each commit.

Apply the tracker mode while implementing. In github mode, apply `in-progress` when starting and `needs-clarification` when an issue question blocks the task; in local mode, and for every quick task, write no status during implementation. Marking the task complete — checkbox or issue close — follows the review gate, never forge's own verification.

Standing rules:

- **Untrusted content in an LLM prompt is never bounded by a textual delimiter** — the content can reproduce any marker string. Serialize it as an escaped value inside a structured format (JSON).
- **Use a standard-library or well-maintained parser for any spec-governed format** (email addresses, URLs, MIME, dates). A hand-rolled validator fails both ways: too permissive and too strict.
- **Normalize first, then validate the result** — never validate raw input and transform afterwards; a whitespace-only value passing a length check can silently overwrite real content.
- **When a new code path parallels an existing one that carries a safety invariant** (containment check, validation, rate limit), decide explicitly whether the new path needs the same invariant. "We already solved this" is a check to perform, not an assumption.
- **A contract or interface change with more than one consumer is not done when its own tests pass** — verify the other consumers and bump the contract version the repo's convention requires.
- **When a fix appears to need a new bound, limit, or threshold**, first check whether the actual defect is a missing normalization or revalidation. Do not invent numeric limits; none of this skill's rules carries one.
- **After a mechanical bulk rewrite across call sites**, grep for the old pattern — including two occurrences inside one function — before calling the migration complete; converted-in-isolation edits hide double-application bugs.

## Steps 4–6: Verify, document, and hand off

Follow `references/verification-and-handoff.md`; forge ends only when verification, documentation checks, scope report, and review handoff are complete or explicitly blocked.
