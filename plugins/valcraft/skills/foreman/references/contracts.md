# Assignment envelope and report contracts

The foreman speaks to workers in one shape and accepts answers in one shape. This reference defines both. The report contracts belong to the skills that produce them — this file links to them and lists only the foreman-specific additions.

## Assignment envelope

Every assignment the foreman sends has these parts, in this order:

1. **Cold start.** "You start with no prior context. Read, in this order: the skill named below through its skill invocation; the repository's root `AGENTS.md`; then only the artifacts named in the assignment. Do not read the run directory except the files named here."
2. **Identity.** Role name, feature, task, tracker reference when one exists, branch name when one exists.
3. **The assignment.** The step text from `references/loop.md`, with every placeholder resolved to an absolute path or exact value. The feature's `tasks.md` path is always present — it is the unique feature selector.
4. **Report instruction.** "When your assignment is complete or you are blocked, write your report to `<run dir>/<role>-<feature>-<task>.md` (append if it exists), then stop. The report is the full contract of the skill you ran — `valcraft:forge`'s handoff or `valcraft:review`'s report — followed by a `Status:` line: `done`, `blocked: <one line>`, or `question: <one line>`." Backends that carry a return channel (a subagent's final text) receive only the report path and the status line there.
5. **Trust boundary.** The paragraph from `SKILL.md`, verbatim.

State only what the skill cannot know: the run, the target, the inputs. Rules the skill owns are not restated in the envelope — change them in the skill.

## Report contracts

The report a worker writes is the producing skill's own report, unchanged; this file links to where each contract is defined and adds only what the foreman needs on top of it. The foreman reads a report once, in full, when acting on it; afterwards it references the report by path and re-reads only what a decision needs. It never pastes a report into another assignment — it passes the path.

| Producer                    | Contract (authoritative)                                                                                                                                                                   | Foreman-specific additions                                                                                                                                                    |
| --------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| planner (step 2)            | `../../msw/SKILL.md` — the msw report for the plan file                                                                                                                                    | the plan's absolute path; open questions the plan could not settle; the `Status:` line                                                                                        |
| `valcraft:review`           | `../../review/SKILL.md` — "Report": the `## Review report` block (Mode and change class, Verdict, Findings, Reproductions, Checks performed, Not examined)                                 | the `Status:` line                                                                                                                                                            |
| reviewer (closure check)    | `../../review/SKILL.md` — shared rule 6 (close only by re-run); the `## Review report` block re-emitted with the resolution column updated for the listed R-IDs                            | the re-run command and its output per listed R-ID; no new findings; the `Status:` line                                                                                        |
| `valcraft:forge`            | `../../forge/references/verification-and-handoff.md` — "Step 6": the `## Forge handoff` block (Changed, Verification evidence, Scope, Open questions and deferred findings, Review target) | `### Review target` names the branch or range the step 8 reviewer pins; the `Status:` line                                                                                    |
| worker (steps 4, 9)         | `../../review/SKILL.md` — shared rules 3, 4, 6 (R-IDs, remediation plan, closure by re-run)                                                                                                | one line per R-ID with its resolution; the plan's absolute path (step 4) or the remediation plan path and resolution commits (step 9)                                         |
| `valcraft:temper` (step 11) | `../../temper/references/report-format.md` — the report file, sections, incident records, routing table                                                                                    | the report's absolute path; the PR URL; one line per routed proposal (tier, `L-NNN`, rule statement); the `Status:` line                                                      |
| planner (decompose)         | `../../cast/SKILL.md`, `../../spec/SKILL.md` — their run reports                                                                                                                           | every Cast proposal and mutation preview as an exact record, each marked `recorded — proceeded` or `waiting`; feature ID and paths; the spec PR reference; the `Status:` line |

Completeness means: the linked contract's report is present as that skill defines it, plus the additions in the right column. For the forge and review blocks the test is mechanical: every heading present, in order, none empty (`none` is a value). A report file appended across rounds holds several blocks; the check applies to the last block in the file, followed by its `Status:` line — an earlier complete block never satisfies a later append. The foreman judges presence, not quality — quality is the reviewer's job.

## Rejection

A report that carries a verdict, a summary, or a "done" without the required content — or a forge or review block with a heading missing — is incomplete. The foreman does not act on it: it sends the same worker one assignment — "Your report at `<path>` is missing `<named parts>`. Append the full `<skill>` contract and stop." — and awaits again. On a one-shot backend the respawn carries the same instruction. A second incomplete report is an escalation (the two-attempt rule in `references/hygiene.md`).

## Status line semantics

- `done` — act on the report.
- `blocked: …` — a permission prompt or an external condition; apply the blocked-worker rule in `references/backends/README.md`.
- `question: …` — the worker needs a decision. Answer it when the spec, design, plan, or the assignment already settles it; otherwise route it through held-task handling in the intake reference or escalate.
