# Backend: `subagents` — Claude Code Agent tool

The foreman is a plain Claude Code session; workers are subagents started with the Agent tool. Zero infrastructure: this is how `valcraft:foreman` runs when the user invokes it directly.

## Flags

| Flag        | Value                                                                                                                                                                         |
| ----------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `wake`      | `event` — the subagent's completion notification re-invokes the foreman                                                                                                       |
| `answer`    | `respawn` — a subagent is one-shot; a block or question ends it                                                                                                               |
| `harnesses` | one (the session's model). Independence comes from fresh context: each role is a new agent with no inherited context, and the second-harness rule is satisfied by that alone. |
| `release`   | none needed — a subagent ends when it returns; never leave one waiting on a message                                                                                           |

## Primitives

- `spawn` + `assign` are one Agent call: `subagent_type` a general-purpose agent (never `fork` — a fork inherits the foreman's context and breaks the cold-start invariant), `name` = `<role>-<F>-<T>`, `prompt` = the assignment envelope, run in the background. Do not pass a `model` override unless the project block names one.
- `await`: the task-completion notification. Arm nothing; end the turn after the Agent call. Because the notification carries the agent's final text, the envelope's report instruction limits that text to the report path and the `Status:` line — the report itself is on disk in the run directory.
- `status`: `none`. There is no mid-run inspection. A subagent that needs a permission or an answer returns with `Status: blocked: …` or `Status: question: …` and its report so far.

## Await discipline on this backend

Steps 1–2 of `README.md`'s await discipline collapse: an Agent call either starts or errors, and the notification arrives whether or not the report file was written. Step 4 applies unchanged: on `report`, check completeness; on `blocked`/`question`, respawn a new agent of the same role with the decision in the envelope and the prior report path attached; on an agent that returns nothing usable, respawn once with the same envelope, then escalate.

## Workspace and the run directory

Foreman and workers share one checkout. Consequences:

- The run directory is `<checkout>/.foreman/<run-id>/`; the envelope still carries the absolute path.
- Workers run serially, so `valcraft:forge`'s branch switch happens in the shared checkout under the foreman. The foreman reads no repository files during a task, so this is safe; after the step 10 merge, the foreman returns the checkout to `foreman_default_branch` (`git switch <branch> && git pull --ff-only`) before picking the next task.
- Step 4's "copy the plan into your worktree" clause is inert — same path, same checkout.
- `valcraft:review`'s revert-the-fix check uses a disposable `git worktree` of its own; the reviewer removes it before returning.

## Merges

The foreman runs `gh pr merge` itself. If this session's permission mode denies it, report the exact command and wait for the human.

## PR-tracking hook

None. CI state is read with `gh pr checks <n> --json name,state --jq …` at step 9 and step 10.

## Eval scenario coverage

The scenario × backend matrix with eval ids is `evals/scenarios.md`.

| Scenario                          | Coverage                                                                                                                                              |
| --------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------- |
| Silent assignment                 | `n/a` — an Agent call cannot silently not start; degradation: an agent that returns no report is treated as `idle-without-report` and respawned once. |
| Early finish before await         | `n/a` — the notification is delivered regardless of timing.                                                                                           |
| Blocked, resolvable from the task | expressible — respawn with the decision.                                                                                                              |
| Blocked, needs escalation         | expressible.                                                                                                                                          |
| Merge denied by classifier        | expressible — the foreman's own permission mode.                                                                                                      |
| Partial mutation failure          | expressible (`github` intake).                                                                                                                        |
| Two-round review cap              | expressible; the closure check and any second round are respawns of the same reviewer name.                                                           |
