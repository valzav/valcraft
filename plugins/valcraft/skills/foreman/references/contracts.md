# Assignment envelope and report contracts

The foreman speaks to workers in one shape and accepts answers in one shape. This reference defines both. The report contracts belong to the skills that produce them — this file links to them and states what the foreman requires; it never restates their rules.

## Assignment envelope

Every assignment the foreman sends has these parts, in this order:

1. **Cold start.** "You start with no prior context. Read, in this order: the skill named below through its skill invocation; the repository's root `AGENTS.md`; then only the artifacts named in the assignment. Do not read the run directory except the files named here."
2. **Identity.** Role name, feature, task, tracker reference when one exists, branch name when one exists.
3. **The assignment.** The step text from `references/loop.md`, with every placeholder resolved to an absolute path or exact value. The feature's `tasks.md` path is always present — it is the unique feature selector.
4. **Report instruction.** "When your assignment is complete or you are blocked, write your report to `<run dir>/<role>-<feature>-<task>.md` (append if it exists), then stop. The report is the full contract of the skill you ran — `valcraft:forge`'s handoff or `valcraft:review`'s report — followed by a `Status:` line: `done`, `blocked: <one line>`, or `question: <one line>`." Backends that carry a return channel (a subagent's final text) receive only the report path and the status line there.
5. **Trust boundary.** The paragraph from `SKILL.md`, verbatim.

State only what the skill cannot know: the run, the target, the inputs. Rules the skill owns are not restated in the envelope — change them in the skill.

## Report contracts

The foreman reads a report once, in full, when acting on it; afterwards it references the report by path and re-reads only what a decision needs. It never pastes a report into another assignment — it passes the path.

| Producer            | Required content                                                                                                                                                                                           | Source of the contract                                                              |
| ------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------- |
| planner (step 2)    | Absolute plan path; confirmation that `valcraft:msw` ran on it; open questions.                                                                                                                            | `../../msw/SKILL.md`                                                                |
| `valcraft:review`   | Mode; verdict (`pass`, `material findings`, `blocked`); the finding table (`R-NNN \| severity \| claim \| evidence \| resolution`); reproduction commands; checks-performed record; what was not examined. | `../../review/SKILL.md` — "Report"                                                  |
| `valcraft:forge`    | What changed by ID; verification evidence with real command output; the scope statement; open questions and deferred findings; the pinned review target (branch or range) for step 8.                      | `../../forge/references/verification-and-handoff.md` — "Step 6: Hand off to review" |
| worker (steps 4, 9) | Plan path or PR reference; each R-ID with its resolution; for step 9, the remediation plan path and resolution commit subjects.                                                                            | `../../review/SKILL.md` — shared rules 3, 4, 6                                      |
| planner (decompose) | Feature ID and paths; each Cast approval point as an exact proposal; the spec PR reference.                                                                                                                | `../../cast/SKILL.md`, `../../spec/SKILL.md`                                        |

## Rejection

A report that carries a verdict, a summary, or a "done" without the required content is incomplete. The foreman does not act on it: it sends the same worker one assignment — "Your report at `<path>` is missing `<named parts>`. Append the full `<skill>` contract and stop." — and awaits again. On a one-shot backend the respawn carries the same instruction. A second incomplete report is an escalation.

## Status line semantics

- `done` — act on the report.
- `blocked: …` — a permission prompt or an external condition; apply the blocked-worker rule in `references/backends/README.md`.
- `question: …` — the worker needs a decision. Answer it when the spec, design, plan, or the assignment already settles it; otherwise route it through held-task handling in the intake reference or escalate.
