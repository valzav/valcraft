# Hygiene

## Context

The foreman's context is a working resource; the loop survives one context window only if it stays small.

- Hold loop state only: task, step, report paths, gate decisions, executed batches. Rebuild everything else from the tracker, git, and the run directory on every command.
- Never read a spec, design, plan, or diff the worker can read instead. The foreman reads a report once when acting on it, then references it by path; assignments carry paths, not content.
- Every `gh` read names explicit fields (`--json … --jq …`); never fetch default-shaped issue or PR JSON. Backend inspection (`status`) uses the smallest window the backend reference allows.

## Naming

- Workers: `<role>-<F>-<T>` — `planner-F004-T012`, `reviewer-1-F004-T012`, `worker-F004-T012`, `reviewer-2-F004-T012`; temper: `temper-<F>` (`temper-F004`); decompose: `planner-<source>`, `reviewer-<source>` (`planner-prd225`, `planner-q3-prd`), where `<source>` is the source id derived in `references/decompose.md` — never a raw path. Feature and task are both present because T-IDs restart per feature. A quick task fills the feature slot with `Q<NNN>` (`worker-Q007-T001`). Backends with a name-length limit declare it; the pattern above fits 20 characters and is never lengthened.
- Branches: `feat/f004-t012-<slug>` (quick: `feat/q007-t001-<slug>`) from `origin/<foreman_default_branch>`; retro report `retro/f004-<slug>`; fast-track from `origin/<foreman_release_branch>`.
- Commits and PRs reference `T-XXX`, the covered `FR-`/`AC-` IDs, and `ADR-` where a decision applies, under the MSW deletion test.
- Reports: `<run dir>/<role>-<F>-<T>.md`. Run directory: `templates/run-dir.md`.

## Sessions and workers

- One worker per role per task. Reuse `reviewer-1-*` across the plan-review round, its closure check, and any second round, and `worker-*` across steps 4, 6, 7, and 9 when the backend keeps workers alive; on a one-shot backend each round is a respawn that carries the prior report path.
- Release a task's workers at the end of step 10 and the temper worker at the end of step 11, per the backend; never leave workers running into the next task.
- Cleanup of workspaces belongs to the backend reference — some backends forbid the foreman from running it.

## Rounds and escalation

- One review round per stage by default; a closure check on resolved R-IDs is not a round. A second full round runs only on a trigger in `references/review-round.md`. Two rounds is the cap; the third is an escalation to the human: name the open finding, tell the worker to stop and report. The cap overrides any worker-internal round budget (MSW's fuse does not grant a worker extra rounds).
- **Two-attempt rule.** Escalate after two failed attempts at anything — an assignment that did not start, a report that stays incomplete, a batch that fails twice, a review round that leaves a material finding open — instead of looping. Authority: the owner's standing orchestrator rules (`orchestrator-template.md` Hygiene, 2026-08-15 revision). Every "once, then escalate" elsewhere in this skill is this rule.

## Human overrides

`references/approval-modes.md`, "Rules that hold in every mode": "no gates", "confirm picks", and mid-run mode changes.
