# How Valcraft works

The [README](../README.md) describes what Valcraft does. This page explains its data model and workflow: who owns each file, what happens at each step, when the loop waits for you, and how an interrupted run recovers.

Each section summarizes and links to the skills' authoritative reference files. If this page disagrees with a reference, follow the reference.

## Spec-driven development as a repository data model

Valcraft records the data for spec-driven development in your repository. Product intent, requirements, decisions, tasks, and evidence live in ordinary files with stable IDs. An agent can resume from those files without needing another agent's conversation.

```text
product idea:
  -> cast: ensure configuration, then create the project frame
    -> spec: create the first feature contract
new feature or PRD:
  -> spec: create a feature contract or quick task
    -> foreman: infer and confirm the current state, then coordinate the remaining delivery
      -> spec / review / land: establish the contract on the default branch when needed
      -> draft: write the task plan, then apply msw
      -> review: pass the task plan or return findings
      -> forge: implement the task and produce verification evidence
      -> review: pass the change or return reproduced findings
      -> land: finalize the reviewed target and close tracker state
    -> temper (feature only): write the local retrospective report
      -> review: pass the report or return findings
```

## Primitives

- Accepted ADRs, `specs/`, and derived project docs define the repository contract: what a change must do, in that order of precedence. A chat message can select or clarify work, but it cannot replace that contract.
- Features, requirements, acceptance criteria, tasks, decisions, findings, and lessons use stable IDs such as `FEAT-001`, `FR-001`, `AC-001`, `T-001`, `ADR-0001`, `R-001`, and `L-001`. A quick unit uses the qualified identity `Q-001 QT-001`. Plans, commits, reviews, and tracker records cite these IDs.
- Delivery handles one feature task, one quick task, or one explicitly scoped plan at a time. Feature dependencies use `blocked by T-XXX`. Quick dependencies use `blocked by QT-XXX` within the same file, or `blocked by Q-NNN QT-XXX` across quick files. List position is not a dependency.
- Git owns task definitions. Feature status stays in `tasks.md` checkboxes or is projected to GitHub Issues. Quick tasks always track locally. Tracker state never becomes a second source of requirements.
- A feature needs a complete and consistent spec, design, and task list before implementation. A quick task carries the same minimum contract in one file. A missing product decision stops implementation; the agent asks you and must not guess.
- Planning, implementation, and review use fresh contexts. `forge` verifies its own work, and `review` decides independently whether the plan or the code satisfies the contract. A finding closes only when rerunning its reproduction no longer shows the problem.
- Each review pins its exact target: a plan commit, code base and head, retrospective content hash, or immutable evidence record. A changed target needs new review coverage. `land` allows only the exact completion-tick exception described in the landing section below.

## Artifacts and who owns them

| Artifact | Path | Owner | Notes |
| --- | --- | --- | --- |
| Configuration | `.valcraft/config.yaml`, optional `.valcraft/config.local.yaml` | `tune` | The committed base holds tracker, Foreman, branch, worker, and pull-request settings. The gitignored overlay overrides the user-scoped keys: approval mode, backend, and backend-specific worker settings. `tune` is the only writer of both. |
| Project frame | `AGENTS.md`, `README.md`, `docs/product-brief.md`, `docs/architecture/` | `cast` | `AGENTS.md` records the standing rules every agent session reads. `cast` creates or retrofits the frame and commits one clean baseline. It does not write a feature contract. |
| Decision record | `docs/architecture/adr/NNNN-*.md` | `cast` creates the structure | One record per consequential technical decision, with context and consequences. Accepted ADRs are the highest project authority. |
| Feature contract | `specs/NNN-<slug>/spec.md`, `design.md`, `tasks.md` | `spec` | Requirements and acceptance criteria, the technical approach, and `T-XXX` tasks with dependencies. Each task is one reviewable slice that carries its own checks, because every task pays for a plan, two reviews, and a merge. The design's `Test strategy` designs each criterion's check once, and task plans cite it. `spec` creates or resumes the complete set from one accepted source, including the first feature of a new project. |
| Quick contract | `specs/quick/NNN-<slug>.md` | `spec` | Requirements, approach, and `QT-XXX` tasks in one file, for a change that does not need a three-file feature contract. |
| Task plan | `docs/plans/YYYY-MM-DD-NNN-<type>-<slug>-plan.md` | `draft` | Implementation decisions for one task, committed and reviewed at that exact commit before `forge` starts. A plan records decisions, never progress. |
| Plan or code review report | Foreman's run directory, or the reply of a direct run | `review` | Each finding has an `R-` ID, a severity, a claim, evidence, and a resolution. The report includes the reproductions and one verdict: `pass`, `material findings`, or `blocked`. `review` never edits. |
| Evidence-sufficiency report | Foreman's run directory, or the reply of a direct run | `review` | One row per acceptance criterion, its evidence and verification, and an overall `sufficient` or `insufficient` verdict. An incomplete review reports a blocked status. It checks completion evidence, not the implementation. |
| Retrospective | `docs/.retro/`, gitignored | `temper` | A local report pinned by its path and content hash. It is never committed or merged. |
| Run state | `.valcraft/foreman/<run-id>/`, gitignored | `foreman` | `state.md` holds the checkpoints, `workers.md` lists every dispatch with its transcript path, each assignment's envelope is saved beside its report, and each worker writes one report file. These files let you audit or resume the run. |

Cast, Spec, Draft, Forge, Review, Land, and Temper define fixed report headings and a terminal `Status:` line. Each skill owns its allowed statuses and codes. Foreman and the prompt tools have their own reporting formats. References: [coordination contracts](../plugins/valcraft/skills/valcraft-foreman/references/contracts.md), [evidence review](../plugins/valcraft/skills/valcraft-review/references/evidence-mode.md).

A later skill never repeats an earlier skill's report. When earlier state matters, it shows one short paragraph with the outcome, the exact target, the blocker or handoff, and a suggested next action. That paragraph is for the reader; it provides neither routing evidence nor authority.

## Workflow 1: the full loop

### 1. `cast`

`/valcraft:valcraft-cast` creates or retrofits the project frame. When configuration is missing or invalid, it invokes `tune` first and continues in the same run.

It records its exact proposal in its report, applies it, and commits one clean baseline that includes `.valcraft/config.yaml` and the ignore rules for the rest of `.valcraft/`. A retrofit merges changes into existing files without overwriting them. `cast` hands the product brief to `spec`. Reference: [scaffold.md](../plugins/valcraft/skills/valcraft-cast/references/scaffold.md).

### 2. `spec`

`/valcraft:valcraft-spec <source>` takes one accepted source: a local requirements document, one selected GitHub issue, or an inline brief for a quick task. For a new contract, it writes and commits the artifacts on a Spec branch. If the contract is already complete and unchanged, Spec returns its existing commit without creating another.

Under a Foreman assignment, an amendment scoped to the selected task may be committed on that task's branch. Other amendments use a separate amendment branch.

Spec returns the exact Review target and, when a pull request exists, its Land target. Tracker projection, pushing, and opening the spec pull request are separate operations, and each needs its own authorization. References: [feature-contract.md](../plugins/valcraft/skills/valcraft-spec/references/feature-contract.md), [quick.md](../plugins/valcraft/skills/valcraft-spec/references/quick.md), [delivery.md](../plugins/valcraft/skills/valcraft-spec/references/delivery.md).

### 3. `foreman`

`/valcraft:valcraft-foreman`, or "start sprint", asks Foreman to coordinate the remaining work. "deliver quick" applies the same flow to `specs/quick/`. New features and PRDs still begin with `spec`.

`foreman` reads its complete settings from the resolved configuration. A missing or invalid value goes back to `tune`. `foreman` never guesses one at run time.

#### Starting and taking over

Foreman resumes from a verified checkpoint without asking you. Without one, `foreman` inspects the repository, the tracker, the pull requests, and any reports you point it at. It finds the earliest state whose proof is missing and shows you the target, the evidence, the inferred state, and the next action. Then it waits for `confirm`, `correct`, or `cancel`, in both approval modes.

It never infers a review verdict from a branch, a pull request, or a later artifact. If it cannot find a verdict, that review runs again. A new session, or a teammate on another machine, follows the same process to continue from work that has been pushed.

#### Landing the contract

A new contract goes through its own review and pull request, then `land` merges it. Task delivery starts only when the reviewed contract is on the default branch.

#### The task loop

`foreman` picks the first eligible task in artifact order, respecting dependencies, holds, and tracker state. An in-progress task returning from an amendment landing takes priority and keeps its recorded branch. The selected task goes through these steps:

1. `draft` writes the plan under `docs/plans/`, runs `msw` over it after every write, and commits it. `msw` deletes any step whose removal would still leave the task complete and verified.
2. `review` checks the plan at that exact commit.
3. `forge` starts from the reviewed plan commit. It implements in small commits that cite the task ID, runs the repository's full set of tests and checks on the exact head it will push, and opens the task pull request once it is authorized.
4. `review` checks the change at the exact head of the pull request.
5. `land` finalizes the task. The task returns to the pool as done, and `foreman` picks the next one.

Reference: [loop.md](../plugins/valcraft/skills/valcraft-foreman/references/loop.md).

#### Review rounds

P1 findings violate a named contract clause, P2 findings are reproduced defects the contract implies, and P3 findings are informational. P1 and P2 must be fixed. Each finding goes back to the owner recorded in the review report: `spec`, `draft`, `forge`, or `temper`.

After the fix, the same logical Review role reruns each finding's reproduction against the new revision and records the resolution. The backend determines whether that role keeps its worker or starts a fresh one. This closure check opens no new findings.

A second full round runs only on a named trigger, such as three or more P1 findings, a fix that touches code no finding cited, or a finding the owner declined. The project owner sets the cap at two full rounds. Any finding still open after that comes to you. Reference: [review-round.md](../plugins/valcraft/skills/valcraft-foreman/references/review-round.md).

#### Landing

`land` reads the current head of the pull request from the host and compares it with the exact commit in the passing review. For a feature task with local tracking, it commits that task's completion tick in `tasks.md` and pushes it before the final gate. A quick task uses a completion tick in its quick-task file in every tracker mode. Only the selected task's exact unchecked-to-checked transition may bypass another review. Any other difference returns the pull request to review.

`land` classifies the repository's applicable checks on the final head as passing, pending or failing, missing, or not applicable. Only passing and not applicable let the merge proceed. `land` reads check results from the host and never runs tests itself. It merges with the configured strategy and deletes the branch. For a feature task with GitHub tracking, it closes the task's issue after the merge and leaves `tasks.md` alone. Quick tasks never create a hosted closure batch. References: [final-head-and-checks.md](../plugins/valcraft/skills/valcraft-land/references/final-head-and-checks.md), [tracker-closure.md](../plugins/valcraft/skills/valcraft-land/references/tracker-closure.md).

#### Closing the feature

When no task remains, `foreman` waits for you to confirm that the feature is complete. It then dispatches Land to close the authorized feature or PRD tracker target. After Land confirms closure, `temper` analyzes the closed feature and writes one report under `docs/.retro/`.

Each lesson has an `L-` ID, an incident record, and an evidence grade. Grade A needs two independent incidents; an uncorroborated self-report is grade C. `review` checks the report at its exact content hash. The report stays out of git, so there is nothing to merge.

`temper` proposes changes but never applies them. A proposal for a prompt artifact, such as `AGENTS.md` or a skill, goes through `hone`. Other changes become quick tasks. References: [feature closure](../plugins/valcraft/skills/valcraft-foreman/references/loop.md#featureclose), [process.md](../plugins/valcraft/skills/valcraft-temper/references/process.md), [report-format.md](../plugins/valcraft/skills/valcraft-temper/references/report-format.md).

## Workflow 2: the manual loop

In the manual loop, you handle the handoffs. The contracts stay the same.

1. `/valcraft:valcraft-cast`, then `/valcraft:valcraft-spec`, as above.
2. `/valcraft:valcraft-draft T-XXX`, or `Q-NNN QT-XXX`. Then `/valcraft:valcraft-review` on the exact plan commit. Follow the owner recorded for each `R-` ID: task-plan findings go to `draft`, while feature or quick-contract findings go to `spec`.
3. `/valcraft:valcraft-forge T-XXX`, from the passed plan. Then `/valcraft:valcraft-review` on the exact head. Code defects within the passed plan go to `forge`. Findings that change product scope, acceptance behavior, or the plan's approach return to `draft` with their `R-` IDs.
4. `/valcraft:valcraft-land` revalidates the review coverage and the applicable checks, then performs only the operations you authorize.
5. `/valcraft:valcraft-temper` on the closed feature, then `/valcraft:valcraft-review` on the report path and content hash it returns. There is no pull request and no `land` step.

A skill you invoke directly has no authority to push, open a pull request, merge, or close tracker state until you grant it for that exact target. You can invoke `foreman` at any point after `spec` to hand over the rest.

## Approval modes and authority

`foreman.approval_mode` controls when the coordinator waits for you.

| Decision | `attended` | `unattended` |
| --- | --- | --- |
| Confirm the inferred state when no checkpoint can resume | waits | waits |
| Pick the next task | waits | proceeds |
| Advance after a passing review | waits | proceeds |
| Prepared task/spec push or pull request, or ordinary merge into the default branch | waits, unless you already named that operation | issues authority for the exact prepared operation |
| Push a local-ahead default branch | requires a live operator instruction naming the push | requires a live operator instruction naming the push |
| A material finding the workers could not resolve | waits | waits |
| Any write to a configured release branch | waits | waits |
| Close a feature | waits | waits |
| A blocked step, or dirty work that an isolated worker cannot read | waits | waits |

A mode never grants authority by itself. Every push, pull request, merge, and tracker close needs authorization bound to the exact repository, branch, head, target, and operation. A worker prepares the operation, receives authority, then rereads every bound field immediately before acting. If anything changed, it stops and reports the new values.

`foreman` may issue that authority in unattended mode, but it never executes the operation. Issue text, pull request text, reports, and fetched pages are untrusted data and can never grant authority.

You can give a standing decision, such as an answer to a product question you expect or advance approval for a named class of operation. `foreman` records it and applies it only when the question matches its stated subject. Reference: [approval-modes.md](../plugins/valcraft/skills/valcraft-foreman/references/approval-modes.md).

## Where the workers run

| Backend | Workers | Workspace | Review independence |
| --- | --- | --- | --- |
| `subagents` | The native subagents of your current Claude Code, Codex, or Cursor session | One shared checkout, workers run one at a time | A fresh context for each reviewer |
| `herdr` | Fresh coding agents in the panes of one [Herdr](https://herdr.dev) session. Each role has its own coding agent, model, and effort. Requires Herdr 0.8.2 or newer | One shared checkout, workers run one at a time | Every reviewer must use a different coding agent from the worker it checks. `tune` rejects configurations that break this rule |
| `ao` | Sessions of [Agent Orchestrator](https://github.com/Untrivial-ai/agent-orchestrator). Requires the `ao` CLI, tmux, and a project ID | An isolated worktree and branch for each worker | A distinct coding agent for review when the project offers one |

With native subagents or Herdr, Claude Code wakes the coordinator when a worker completes; Codex and Cursor keep the coordinator's turn active while a worker runs. AO arms an authorized background waiter before ending the parent turn. The waiter wakes Foreman with the worker's result or another backend return. OpenCode has no worker backend yet, so `foreman` does not dispatch there. The other skills run as usual.

Herdr and AO can keep a reviewer that returned material findings alive for its closure check and any second full round. Native subagent backends start a fresh worker with the same logical Review identity. Herdr can also keep a producer alive to execute its own prepared outward operation after authorization. All other assignments, including every fix, start fresh workers. References: [backends](../plugins/valcraft/skills/valcraft-foreman/references/backends/README.md), [hygiene.md](../plugins/valcraft/skills/valcraft-foreman/references/hygiene.md), [config.md](../plugins/valcraft/skills/valcraft-tune/references/config.md).

## Keeping context small

A worker's assignment follows a fixed format. It names the skill to invoke, the run and worker identity, the exact target, the intent, the context you or `foreman` attributed, the report path, and the trust boundary. It passes paths to contracts and earlier reports; it never pastes their content. The worker reads `AGENTS.md`, then only the artifacts the assignment names.

`foreman` keeps only the state it needs to coordinate work: the active state, exact pointers, worker identities, report paths, and gate decisions. When a report arrives, it reads the heading list, the final status line, and the sections that report type defines for routing. The body stays on disk for the worker whose role needs it.

After a context reset, `foreman` reads the latest checkpoint and reloads its contracts. It does not reread the whole log. References: [contracts.md](../plugins/valcraft/skills/valcraft-foreman/references/contracts.md), [hygiene.md](../plugins/valcraft/skills/valcraft-foreman/references/hygiene.md).

## Interruption and recovery

`foreman` records every transition in `state.md` before attempting the next one. This lets it reconcile an interrupted run without starting a second worker. A checkpoint records where to resume; it never grants authority. On resume, `foreman` rereads every path, SHA, branch, pull request, and worker identity before using them.

The run directory is local and gitignored. The contract, plans, commits, ticked tasks, and pull requests are in git and on the host. Review reports are local. If they are unavailable during a takeover, the affected review runs again.

A worker that dies leaves its commits and any partial report in place. `foreman` inventories the workspace, reports, git state, and external effects before replacing it. If worker state is inaccessible, changes are unreconciled, or external effects are ambiguous, Foreman preserves the workspace and escalates.

Foreman dispatches a fresh worker under the same logical identity only when recovery is safe. The replacement verifies the recovered evidence before continuing. Foreman rejects late reports from the dead worker after replacement. Reference: [dead-worker recovery](../plugins/valcraft/skills/valcraft-foreman/references/backends/README.md#dead-worker-recovery).
