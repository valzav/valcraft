# valcraft

Agent skills for spec-driven delivery, packaged as one plugin for Claude Code and OpenAI
Codex. Scaffold a project around specs that live in the repository (tracked as plain
markdown with checkbox tasks, or projected to GitHub Issues). Turn PRDs into feature
specs. Run each task through a plan → review → implement → review → merge loop over
fresh-context worker agents. Then learn from what shipped.

Status: alpha.

## Problems it addresses

| If you have seen this…                                              | valcraft's answer                                                                                                                                                                                                  |
| ------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| The agent forgets requirements between sessions and reinvents them. | `cast` scaffolds a lean spec structure inside the repository (`spec.md`, `design.md`, `tasks.md`) with stable IDs (`FR-`, `AC-`, `T-`, `ADR-`) that commits, tests, and reviews cite. Context lives with the code. |
| "Make X" turns into a pile of unreviewed code.                      | `cast` scaffolds and stops; `foreman` gates every task through an independent plan review and code review, and nothing merges on the implementer's own verification.                                               |
| One long session runs out of context or reports work it never did.  | `foreman` keeps its own context small — every worker starts cold, reports land on disk in `.foreman/`, and a run resumes from the tracker, git, and that directory.                                                |
| Either you approve every step, or the agent runs away.              | Approval modes (`attended`, `gated`, `delegated`) decide which decisions wait for you; irreversible acts — release-branch writes, feature close, escalations — wait in every mode.                                 |
| Task tracking drifts from what the specs say.                       | The specs are canonical; the tracker is a projection of them — the simple option is `tasks.md` checkboxes in the repo, or GitHub Issues with generated bodies and blocked-by links.                                |
| The same mistakes recur project after project.                      | `temper` runs an evidence-graded retrospective over a shipped feature and proposes standing rules for `AGENTS.md`; nothing is promoted on a single unverified incident.                                            |
| Prompts and skills bloat until the model ignores them.              | `hone`, `distill`, and `msw` refine, reduce, and judge prompt artifacts against a stated contract.                                                                                                                 |

## Workflows

### 1. The full loop: `cast` → `spec` → `foreman`

The default path for a new project or a new body of work.

1. **`/valcraft:cast`** — scaffold a fresh project (or retrofit an existing one): README,
   `AGENTS.md`, product brief, ADR index, and a populated `specs/001-mvp/` triplet.
   Choose the tracker: `local` (checkboxes in `tasks.md`) or `github` (Issues). Cast ends
   with a report and next steps; it never implements.
2. **Enrich, then `/valcraft:spec`** — add the context and use cases the scaffold had to
   mark as assumptions. `spec` turns a PRD (a local file or a GitHub issue) into the next
   canonical feature spec; `cast` stages its `design.md` and `tasks.md`.
3. **`/valcraft:foreman`** — add the foreman block to `AGENTS.md`
   (`plugins/valcraft/skills/foreman/templates/project-block.md`) and say "start sprint".
   For each task, in order: pick → plan (`msw`) → plan review → implement (`forge`) → PR →
   code review → fix → merge → close. When the feature closes, `temper` writes the
   retrospective. Workers are Claude Code subagents from a plain session, or Agent
   Orchestrator sessions. `foreman` can also decompose a PRD end to end ("new PRD #N").

### 2. Manual loop, one task at a time

Same contracts, you drive:

1. `/valcraft:cast`, then `/valcraft:spec` as above.
2. `/valcraft:forge T-NNN` — implement one task from its plan; ends at a fixed-shape
   handoff, never at "done".
3. `/valcraft:review` in a fresh context — plan mode before implementation, code mode on
   the PR or diff; resolve findings by `R-ID`, then merge yourself.
4. `/valcraft:temper` over the feature directory when it ships.

`review` and `temper` also run alone: review any plan, spec, PR, or diff against its Cast
contract; retrospect over a PR range or date window.

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

| Skill     | Claude Code         | Codex               |
| --------- | ------------------- | ------------------- |
| `cast`    | `/valcraft:cast`    | `$valcraft:cast`    |
| `spec`    | `/valcraft:spec`    | `$valcraft:spec`    |
| `forge`   | `/valcraft:forge`   | `$valcraft:forge`   |
| `review`  | `/valcraft:review`  | `$valcraft:review`  |
| `foreman` | `/valcraft:foreman` | `$valcraft:foreman` |
| `temper`  | `/valcraft:temper`  | `$valcraft:temper`  |
| `hone`    | `/valcraft:hone`    | `$valcraft:hone`    |
| `distill` | `/valcraft:distill` | `$valcraft:distill` |
| `msw`     | `/valcraft:msw`     | `$valcraft:msw`     |

Skills also trigger from natural requests ("new project", "review this PR",
"retrospective on feature 3"); the command is the explicit path.

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

## More

- [docs/development.md](docs/development.md) — live editing, repository layout,
  packaging, evals.
- [docs/glossary.md](docs/glossary.md) — the terms the skills share.

## License

[MIT](LICENSE).
