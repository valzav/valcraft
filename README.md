# valcraft

Agent skills for spec-driven delivery, packaged as one plugin for Claude Code and OpenAI
Codex, and as a skills source for OpenCode. At the center is an agentic **delivery
loop** — plan → review → implement → review → merge — run over fresh-context worker
agents, inside one Claude Code session or through an orchestrator over several Claude
Code and Codex instances. Around it: `cast` scaffolds a project around specs that live in
the repository (plain markdown with checkbox tasks, or projected to GitHub Issues), `spec`
turns PRDs into feature specs, and `temper` learns from what shipped.

Status: alpha.

## Problems it addresses

| If you have seen this…                                              | valcraft's answer                                                                                                                                                                                                  |
| ------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| The agent forgets requirements between sessions and reinvents them. | `cast` scaffolds a lean spec structure inside the repository (`spec.md`, `design.md`, `tasks.md`) with stable IDs (`FR-`, `AC-`, `T-`, `ADR-`) that commits, tests, and reviews cite. Context lives with the code. |
| "Make X" turns into a pile of unreviewed code.                      | `cast` scaffolds and stops; `foreman` gates every task through an independent plan review and code review, and nothing merges on the implementer's own verification.                                               |
| One long session runs out of context or reports work it never did.  | `foreman` keeps its own context small — every worker starts cold, reports land on disk, and a run resumes from the tracker, git, and those reports.                                                                |
| Either you approve every step, or the agent runs away.              | Approval modes (`attended`, `gated`, `delegated`) decide which decisions wait for you. Some always do: release-branch writes, feature close, and escalations.                                                      |
| Task tracking drifts from what the specs say.                       | The specs are canonical; the tracker is a projection of them — the simple option is `tasks.md` checkboxes in the repo, or GitHub Issues with generated bodies and blocked-by links.                                |
| The same mistakes recur project after project.                      | `temper` runs an evidence-graded retrospective over a shipped feature and proposes standing rules for `AGENTS.md`; nothing is promoted on a single unverified incident.                                            |
| Prompts and skills bloat until the model ignores them.              | `hone`, `distill`, and `msw` refine, reduce, and judge prompt artifacts against a stated contract.                                                                                                                 |

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
   requirements, approach, and checkbox tasks; you choose. Enrich the product brief and
   specs with the context and use cases the scaffold had to mark as assumptions before
   you go further.
3. **`/valcraft:foreman`** — add the foreman block to `AGENTS.md`
   (`plugins/valcraft/skills/foreman/templates/project-block.md`) and say "start sprint".
   For each task, in order: pick → plan (`msw`) → plan review → implement (`forge`) → PR →
   code review → fix → merge → close. When the feature closes, `temper` writes the
   retrospective. "deliver quick" runs the same loop over `specs/quick/`; `foreman` can
   also decompose a PRD end to end ("new PRD #N").

   `foreman` runs from a Claude Code session: as a plain session whose workers are
   subagents, or as an Agent Orchestrator session whose workers are Claude Code and Codex
   sessions. In Codex the skill is installed and triggers, but no Codex-native worker
   backend exists yet.

### 2. Manual loop, one task at a time

Same contracts, you drive:

1. `/valcraft:cast`, then `/valcraft:spec` as above.
2. `/valcraft:forge T-NNN` (or `Q-NNN`) — plans the task when it needs a plan,
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

| Skill     | Claude Code         | Codex               | OpenCode  |
| --------- | ------------------- | ------------------- | --------- |
| `cast`    | `/valcraft:cast`    | `$valcraft:cast`    | `cast`    |
| `spec`    | `/valcraft:spec`    | `$valcraft:spec`    | `spec`    |
| `forge`   | `/valcraft:forge`   | `$valcraft:forge`   | `forge`   |
| `review`  | `/valcraft:review`  | `$valcraft:review`  | `review`  |
| `foreman` | `/valcraft:foreman` | `$valcraft:foreman` | `foreman` |
| `temper`  | `/valcraft:temper`  | `$valcraft:temper`  | `temper`  |
| `hone`    | `/valcraft:hone`    | `$valcraft:hone`    | `hone`    |
| `distill` | `/valcraft:distill` | `$valcraft:distill` | `distill` |
| `msw`     | `/valcraft:msw`     | `$valcraft:msw`     | `msw`     |

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
