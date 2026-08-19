# valcraft

Agent skills for spec-driven delivery, packaged as one plugin for Claude Code, OpenAI
Codex, and OpenCode. At the center is an agentic **delivery loop** — plan → review →
implement → review → merge — run over fresh-context worker agents, inside one Claude Code
or Codex session or through an orchestrator over several instances. Around it: `cast`
scaffolds a project around specs that live in the repository (plain markdown with
checkbox tasks, or projected to GitHub Issues), `spec` turns PRDs into feature specs,
and `temper` learns from what shipped.

Status: alpha.

## Problems it addresses

| If you have seen this…                                              | valcraft's answer                                                                                                                                                                                                  |
| ------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| The agent forgets requirements between sessions and reinvents them. | `cast` scaffolds a lean spec structure inside the repository (`spec.md`, `design.md`, `tasks.md`) with stable IDs (`FR-`, `AC-`, `T-`, `ADR-`) that commits, tests, and reviews cite. Context lives with the code. |
| "Make X" turns into a pile of unreviewed code.                      | `cast` scaffolds and stops; `foreman` gates every task through an independent plan review and code review, and nothing merges on the implementer's own verification.                                               |
| One long session runs out of context or reports work it never did.  | `foreman` keeps its own context small — every worker starts cold, reports land on disk, and a run resumes from the tracker, git, and those reports.                                                                |
| Either you approve every step, or the agent runs away.              | Approval modes (`attended`, `unattended`) decide which decisions wait for you. Some always do: release-branch writes, feature close, and escalations.                                                              |
| Task tracking drifts from what the specs say.                       | The specs are canonical; the tracker is a projection of them — the simple option is `tasks.md` checkboxes in the repo, or GitHub Issues with generated bodies and blocked-by links.                                |
| The same mistakes recur project after project.                      | `temper` runs an evidence-graded retrospective over a shipped feature and proposes standing rules for `AGENTS.md`; nothing is promoted on a single unverified incident.                                            |
| Prompts and skills bloat until the model ignores them.              | `hone`, `distill`, and `msw` refine, reduce, and judge prompt artifacts against a stated contract.                                                                                                                 |

## Valcraft's SDD at a glance

Valcraft treats spec-driven development as a repository data model, not a session
ritual. Product intent, requirements, decisions, tasks, and evidence live in ordinary
files with stable IDs. Agents can resume from those artifacts without inheriting another
agent's conversation.

```text
product idea:
  -> cast: SDD project scaffold
    new feature or PRD:
      -> spec: feature contract or quick task
        -> foreman: coordinate delivery
          -> planner: write the task plan, then apply msw
          -> review: pass the task plan or return findings
          -> forge: implement the task and produce verification evidence
          -> review: pass the change or return reproduced findings
          -> foreman: merge and close the tracker task
```

`foreman` can coordinate the delivery stages in one loop; the same skills also run
individually when a human drives the work.

### Primitives

- **Git-owned contract.** Accepted ADRs, `specs/`, and derived project docs define what
  the change must do, in that precedence order. A chat message can select or clarify
  work, but it does not silently replace the repository contract.
- **Stable identity.** Features, requirements, acceptance criteria, tasks, decisions,
  and findings use IDs such as `FEAT-001`, `FR-001`, `AC-001`, `T-001`, `ADR-0001`, and
  `R-001`. A quick unit uses the qualified identity `Q-001 QT-001`. Plans, commits,
  reviews, and tracker records cite these IDs.
- **One unit of work.** Delivery operates on one feature task, one quick task, or one
  explicitly scoped plan at a time. Dependencies are part of the task contract, not
  inferred from conversation order.
- **Tracker as projection.** Git owns task definitions. Feature status can remain in
  `tasks.md` checkboxes or project to GitHub Issues; quick tasks always track locally.
  Tracker state never becomes a second source of requirements.
- **Readiness before execution.** A feature needs a complete and consistent spec,
  design, and task decomposition. A quick task carries the same minimum contract in one
  file. Missing product decisions stop implementation rather than becoming guesses.
- **Independent evidence.** Planning, implementation, and review use fresh contexts.
  `forge` verifies its work, but `review` independently decides whether the plan or code
  satisfies the contract. Findings close only when their reproductions pass.

### Artifacts and skill ownership

- **Project frame:** `AGENTS.md` records the standing development rules and tracker
  mode; `docs/product-brief.md` records product intent and boundaries. `cast` creates or
  retrofits them, and every delivery skill reads the applicable rules.
- **Decision record:** `docs/architecture/adr/NNNN-*.md` captures consequential
  technical decisions and their consequences. `cast` establishes the ADR structure;
  `forge` and `review` treat accepted ADRs as the highest project authority.
- **Feature contract:** `specs/NNN-<slug>/spec.md` owns requirements and acceptance
  criteria, `design.md` owns the technical realization, and `tasks.md` owns `T-XXX`
  decomposition and dependencies. `spec` creates the feature spec from one PRD; `cast`
  completes and validates the triplet; `foreman`, `forge`, and `review` deliver against
  it.
- **Quick contract:** `specs/quick/NNN-<slug>.md` combines requirements, approach, and
  `QT-XXX` tasks for a change that does not need a feature triplet. `spec` creates it;
  the normal delivery and review skills use it as the complete contract.
- **Delivery plan:** `docs/plans/*-plan.md` records implementation decisions for
  non-trivial work or remediation decisions for review findings. `msw` pressure-tests
  the plan, `review` checks it before implementation, and `forge` executes it. Progress
  remains in the tracker rather than being written back into the plan.
- **Evidence and learning:** `forge` produces a verification handoff; `review` produces
  stable `R-XXX` findings and reproduced evidence; `foreman` stores worker reports in
  its ignored run directory while coordinating closure. After work ships, `temper`
  writes an append-only report under `docs/retro/` and proposes durable rules.

## Workflows

### 1. The full loop: `cast` → `spec` → `foreman`

The default path for a new project or a new body of work.

1. **`/valcraft:cast`** — for a fresh project: README, `AGENTS.md`, product brief, ADR
   index, and a populated `specs/001-mvp/` triplet. For an existing project: a retrofit
   that adds the missing pieces and normalizes existing specs and tasks. Either way you
   choose the tracker — `local` (checkboxes in `tasks.md`) or `github` (Issues) — and
   Cast ends with a report and next steps; it never implements.
2. **`/valcraft:spec`** — for each new feature, give `spec` one PRD (a local file or a
   GitHub issue); it writes the next feature spec, and `cast` then adds that feature's
   `design.md` and `tasks.md`. For a change too small for a triplet, `spec` proposes a
   **quick task** instead — one file `specs/quick/NNN-<slug>.md` (`Q-NNN`) with
   requirements, approach, and `QT-XXX` checkbox tasks; you choose. Quick dependencies
   are `blocked by QT-XXX` within one file or `blocked by Q-NNN QT-XXX` across files.
   Before continuing, enrich the product brief and specs with any context or use cases
   that the scaffold had to record as assumptions.
3. **`/valcraft:foreman`** — say "start sprint" whenever the project is ready.
   No setup-time Foreman configuration is required: it defaults to native subagents and
   unattended mode, derives the repository's default branch when invoked, and treats a
   missing release branch as no separate release branch.
   For each task, in order: pick → plan (`msw`) → plan review → implement (`forge`) → PR →
   code review → fix → merge → close. When the feature closes, `temper` writes the
   retrospective. "deliver quick" runs the same loop over `specs/quick/`; `foreman` can
   also decompose a PRD end to end ("new PRD #N").

   Add `foreman_*` keys to `AGENTS.md` only when the project needs explicit overrides.
   Manual Forge remains available without changing the scaffold.

   `foreman` can use native subagents on either host. Claude Code wakes the parent turn
   when a worker completes; Codex keeps the parent turn active and waits for the worker
   in the foreground. Agent Orchestrator remains a separate backend whose workers can be
   Claude Code and Codex sessions.

### 2. Manual loop, one task at a time

Same contracts, you drive:

1. `/valcraft:cast`, then `/valcraft:spec` as above.
2. `/valcraft:forge T-XXX` (or `Q-NNN QT-XXX`; bare `Q-NNN` selects its next eligible
   task) — plans the task when it needs a plan,
   implements it, and ends at the review handoff, never at "done". To gate the plan
   first, run `/valcraft:review` in plan mode on it before forge implements.
3. `/valcraft:review` in a fresh context, code mode on the PR or diff; resolve findings
   by `R-ID`, then merge yourself.
4. `/valcraft:temper` over the feature directory when it ships.

## Prompt tooling

- **`hone`** — refine a prompt, skill, or `AGENTS.md` against the current Claude and Codex
  prompting guides; deletion first, every addition justified.
- **`distill`** — reduce a prompt or skill to goal, steps, constraints, and testable
  behaviors; a study or a leaner drop-in copy.
- **`msw`** — apply the MSW Kernel to a markdown document: derive its contract, delete every
  claim the contract does not require, report what was cut and why. Kernel by "Fable at
  mega high monkey effort", published by
  [@aienginerd](https://x.com/aienginerd/status/2085342869850603672).

## Skills at a glance

| Skill                                              | Claude Code         | Codex               | OpenCode  |
| -------------------------------------------------- | ------------------- | ------------------- | --------- |
| `cast` — scaffold or retrofit a project            | `/valcraft:cast`    | `$valcraft:cast`    | `cast`    |
| `spec` — PRD or brief → feature spec or quick task | `/valcraft:spec`    | `$valcraft:spec`    | `spec`    |
| `forge` — implement one task                       | `/valcraft:forge`   | `$valcraft:forge`   | `forge`   |
| `review` — review a plan or a change               | `/valcraft:review`  | `$valcraft:review`  | `review`  |
| `foreman` — run the delivery loop                  | `/valcraft:foreman` | `$valcraft:foreman` | `foreman` |
| `temper` — retrospective over shipped work         | `/valcraft:temper`  | `$valcraft:temper`  | `temper`  |
| `hone` — refine a prompt artifact                  | `/valcraft:hone`    | `$valcraft:hone`    | `hone`    |
| `distill` — reduce a prompt to its essence         | `/valcraft:distill` | `$valcraft:distill` | `distill` |
| `msw` — MSW Kernel over a document                 | `/valcraft:msw`     | `$valcraft:msw`     | `msw`     |

Skills also trigger from natural requests ("new project", "review this PR",
"retrospective on feature 3"); the command is the explicit path. OpenCode has no plugin
namespace: its `skill` tool loads them by bare name, and a skill that says "run
`valcraft:review`" means the `review` skill there.

## Compared with other SDD frameworks

| Elsewhere                                                                                    | In valcraft                                                                                                                                                                                                                                                |
| -------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| An executable, scripts, and a setup step.                                                    | The skills are instruction-only: one plugin, no runtime dependency, and nothing to install into the project beyond the files `cast` writes.                                                                                                                |
| Specs and tasks live in the framework's own folders and formats.                             | Specs are ordinary files under `specs/`, tasks are checkboxes or GitHub Issues you already use, decisions are ADRs — readable and editable without the tool.                                                                                               |
| SDD is a session ritual, not a project rule; work done outside it drifts from the specs.     | `cast` writes the discipline into `AGENTS.md`, so every agent session — inside the loop or not — cites IDs, updates the affected spec or ADR in the same change, and reviews against the same contract; `cast` retrofits an existing project the same way. |
| Roles are personas and phases are ceremony — analyst hands off to PM hands off to architect. | valcraft's roles are skills with contracts (`spec`, `forge`, `review`, `temper`); independence comes from a fresh context per role, not a character sheet.                                                                                                 |
| A dozen generated documents and a traceability matrix nobody reads.                          | The skeleton is small; every other artifact is opt-in with a stated trigger. IDs and links give traceability; the skills trim generated verbosity before committing.                                                                                       |
| Adoption is all or nothing.                                                                  | Each skill runs alone: `review` on any PR or plan, `temper` on any range, `forge` on one task, `cast` to retrofit — the loop is there when you want it.                                                                                                    |

## Install

Claude Code:

```bash
claude plugin marketplace add valzav/valcraft
claude plugin install valcraft@valcraft
```

Codex (start a new session afterwards):

```bash
codex plugin marketplace add valzav/valcraft
codex plugin add valcraft@valcraft
```

OpenCode — add the skills source to `opencode.json` (project or global) and allow the
`skill` tool; OpenCode fetches `index.json` and caches every skill file, refreshing a
skill when its content changes:

```json
{
  "$schema": "https://opencode.ai/config.json",
  "skills": {
    "urls": [
      "https://raw.githubusercontent.com/valzav/valcraft/main/plugins/valcraft/skills/"
    ]
  },
  "permission": { "skill": "allow" }
}
```

The URL form needs the repository to be public (raw GitHub answers anonymous requests
only for public repositories). From a clone, use `"skills": { "paths":
["/path/to/valcraft/plugins/valcraft/skills"] }` instead. `foreman` has no OpenCode
worker backend yet; the other skills run as they do elsewhere.

## Update

Claude Code — third-party marketplaces do not auto-update; every push is a new version:

```bash
claude plugin marketplace update valcraft
claude plugin update valcraft@valcraft
```

Codex — refresh the marketplace snapshot and re-add, then start a new session:

```bash
codex plugin marketplace upgrade valcraft
codex plugin add valcraft@valcraft
```

OpenCode — nothing to run: the source is re-read at startup, and a skill whose
`version` in `index.json` changed is re-downloaded (raw GitHub caches for a few minutes).

## More

- [docs/development.md](docs/development.md) — live editing, repository layout,
  packaging, evals.
- [docs/glossary.md](docs/glossary.md) — the terms the skills share.

## Contributing

Pull requests are welcome. The `lint` workflow must pass, and every shipped `SKILL.md`
must stay at or below 8,000 UTF-8 bytes (the Codex limit; move detail into
`references/`). [docs/development.md](docs/development.md) covers live editing and
packaging.

## License

[MIT](LICENSE).
