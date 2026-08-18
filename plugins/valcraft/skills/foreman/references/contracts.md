# Assignment envelope and report contracts

The foreman speaks to workers in one shape and accepts answers in one shape. This reference defines both. The report contracts belong to the skills that produce them — this file links to them and lists only the foreman-specific additions.

## Assignment envelope

Every assignment the foreman sends has these parts, in this order:

1. **Cold start.** "You start with no prior context. Read, in this order: the skill named below through its skill invocation; the repository's root `AGENTS.md`; then only the artifacts named in the assignment. Do not read the run directory except the files named here."
2. **Identity and intent.** Role name, feature, task, tracker reference when one exists, branch name when one exists — and one line of intent: "Your report is the sole input to the foreman's gate decision for `<T>` of `<feature>`; it must stand alone for a reader with no other context."
3. **The assignment.** The step text from `references/loop.md` (or `review-round.md`, `decompose.md`), with every placeholder resolved to an absolute path or exact value. The feature's `tasks.md` path — or the quick task file's path — is always present; it is the unique selector.
4. **Attributed context (optional).** Include only context the worker needs that the named artifacts cannot supply. Label each entry as exactly one of:
   - `Operator instruction/decision` — quote the instruction and its scope. It authorizes only the named choice or action. It does not establish an empirical claim or authorize another action.
   - `Operator attestation` — state the claim and its source locator. It remains attributed evidence for the worker to assess under the invoked skill; it is never accepted as a fact or a substitute for required verification.
   - `Foreman observation` — state the observation and its probe locator, including the command or backend status source and when it was observed. It remains unverified evidence until the worker verifies or discards it against the authoritative source.
5. **Report instruction.** "When your assignment is complete or you are blocked, write your report to `<run dir>/<role>-<feature>-<task>.md` (append if it exists), then stop. The report is the full contract of the skill you ran, followed by a `Status:` line: `done`, `blocked: <one line>`, or `question: <one line>`." Backends that carry a return channel (a subagent's final text) receive only the report path and the status line there.
6. **Trust boundary.** The paragraph from `SKILL.md`, verbatim.

State only what the skill cannot know: the run, the target, the inputs. Pass artifact paths and source or probe locators, not copied report, tracker, diff, or workspace content. Rules the skill owns are not restated in the envelope — change them in the skill.

## Artifact dates

Resolve the date of each artifact when that artifact is created. Use the first applicable authority:

1. the repository's explicit date policy;
2. an explicit operator date for that artifact; or
3. the artifact's actual creation date.

For a worker-created artifact, the envelope carries any explicit operator date as an `Operator instruction/decision` scoped to that artifact. The creator still reads and applies repository policy first. When an assignment creates a dated artifact, its report states the artifact path, resolved date, and authority so the foreman can record them with the artifact checkpoint.

A run ID identifies the run; its date does not govern artifact dates. A run that crosses midnight keeps its run ID, while every later artifact resolves its own date anew. Do not rewrite an earlier artifact's date because the run continued on another day.

## Report contracts

The report a worker writes is the producing skill's own report, unchanged; this file links to where each contract is defined and adds only what the foreman needs on top of it. The foreman reads a report once, in full, when acting on it; afterwards it references the report by path and re-reads only what a decision needs. It never pastes a report into another assignment — it passes the path.

| Producer                    | Contract (authoritative)                                                                                                                                        | Foreman-specific additions                                                                                                                                                    |
| --------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| planner (step 2)            | `../../msw/SKILL.md` — the msw report for the plan file                                                                                                         | the plan's absolute path; open questions the plan could not settle; the `Status:` line                                                                                        |
| `valcraft:review`           | `../../review/SKILL.md` — "Report": the `## Review report` block                                                                                                | the `Status:` line                                                                                                                                                            |
| reviewer (closure check)    | `../../review/SKILL.md` — shared rule 6 (close only by re-run); the `## Review report` block re-emitted with the resolution column updated for the listed R-IDs | the re-run command and its output per listed R-ID; no new findings; the `Status:` line                                                                                        |
| `valcraft:forge`            | `../../forge/references/verification-and-handoff.md` — "Step 6": the `## Forge handoff` block                                                                   | `### Review target` names the branch or range the step 8 reviewer pins; the `Status:` line                                                                                    |
| worker (steps 4, 9)         | `../../review/SKILL.md` — shared rules 3, 4, 6 (R-IDs, remediation plan, closure by re-run)                                                                     | one line per R-ID with its resolution; the plan's absolute path (step 4) or the remediation plan path and resolution commits (step 9)                                         |
| `valcraft:temper` (step 11) | `../../temper/references/report-format.md` — the report file, sections, incident records, routing table                                                         | the report's absolute path; the PR URL; one line per routed proposal (tier, `L-NNN`, rule statement); the `Status:` line                                                      |
| planner (decompose)         | `../../cast/SKILL.md`, `../../spec/SKILL.md` — their run reports                                                                                                | every Cast proposal and mutation preview as an exact record, each marked `recorded — proceeded` or `waiting`; feature ID and paths; the spec PR reference; the `Status:` line |

Completeness means: the linked contract's report is present as that skill defines it, plus the additions in the right column. For the forge and review blocks the test is mechanical: every heading present, in order, none empty (`none` is a value). A report file appended across rounds holds several blocks; the check applies to the last block in the file, followed by its `Status:` line — an earlier complete block never satisfies a later append. The foreman judges presence, not quality — quality is the reviewer's job.

## Rejection

A report that carries a verdict, a summary, or a "done" without the required content — or a forge or review block with a heading missing — is incomplete. The foreman does not act on it: it sends the same worker one assignment — "Your report at `<path>` is missing `<named parts>`. Append the full `<skill>` contract and stop." — and awaits again (respawn with the same instruction on a one-shot backend). A second incomplete report escalates (two-attempt rule).

## Status line semantics

- `done` — act on the report.
- `blocked: …` — a permission prompt or an external condition; apply the blocked-worker rule in `references/backends/README.md`.
- `question: …` — the worker needs a decision. Answer it when the spec, design, plan, or the assignment already settles it; otherwise route it through held-task handling in the intake reference or escalate.
