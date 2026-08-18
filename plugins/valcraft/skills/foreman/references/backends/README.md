# Backends

A backend is how the foreman runs workers. The loop never touches a runner directly; it calls four primitives and reads two capability flags, and each backend reference says how its runner provides them. `foreman_backend` in the project block selects the reference.

## Primitives

| Primitive | Meaning                                                                                                                        |
| --------- | ------------------------------------------------------------------------------------------------------------------------------ |
| `spawn`   | Start a fresh worker of a role on a harness. Cold context, no inheritance from the foreman.                                    |
| `assign`  | Deliver an assignment envelope (`references/contracts.md`) to a worker.                                                        |
| `await`   | Learn that a worker finished, blocked, or died — and which. A foreground wait may also return a nonterminal timeout.          |
| `status`  | Inspect a worker: liveness, and the text of a prompt it is blocked on. May be `none`.                                          |

Some backends fold `spawn` and `assign` into one operation; the reference says so.

## Capability flags

| Flag        | Values                     | Meaning                                                                                                                                                                                                             |
| ----------- | -------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `wake`      | `event` \| `foreground` \| `poll` | `event`: `await` re-invokes the foreman after the parent turn ends. `foreground`: `await` returns inside the active parent turn. `poll`: the foreman checks on the backend reference's schedule.              |
| `answer`    | `interactive` \| `respawn` | `interactive`: a blocked worker can receive an answer and continue. `respawn`: the worker is one-shot; a block or question ends it, and the foreman spawns a new worker with the decision included in the envelope. |
| `harnesses` | list                       | Which harnesses `spawn` offers. Two or more enable the second-harness rule for `planner` and `reviewer-2`; one means independence by fresh context alone.                                                           |
| `release`   | how workers end            | How the foreman ends a task's workers (step 10) and the temper worker (step 11), and what it must not do.                                                                                                           |

## Await discipline

Applies to every backend, in this order:

1. **Confirm the assignment started.** After `assign`, use `status` (or the backend's equivalent) to see the worker processing before arming `await`. An idle worker with no report file means the delivery silently failed — re-assign instead of waiting.
2. **Check before waiting.** Inspect `status` and any completion already delivered for the assigned worker before arming `await`. Act on an early terminal outcome immediately. Absence from live status alone never proves completion or success.
3. **Apply the wake mapping.** On `event`, arm `await` and end the turn. On `foreground`, call `await` inside the active turn and resolve every return through the assigned worker's state before re-arming or advancing. On `poll`, use only the schedule the backend reference authorizes.
4. **Act on the outcome.** `report` → read and check completeness (`references/contracts.md`), then act. `blocked` or `question` → blocked-worker rule below. `idle-without-report` → `status` to read the worker's last output; re-assign once, then escalate. A dispatch error before the worker could act → retry once with the same envelope, then escalate (two-attempt rule). `dead` → apply recovery below before any replacement dispatch. A foreground timeout with the assigned worker still active is nonterminal: re-arm `await` in the same turn.

Never poll a report file for completion on an `event` or `foreground` backend. A `poll` backend follows only its own authorized reference.

## Dead-worker recovery

A dead worker may have left useful work or an external effect. Before dispatching a replacement, inventory every state class the backend can inspect:

- git refs, branches, commits, and exact commit SHAs;
- tracker or change-request references and their current external state;
- the assigned report path, its existence, and whether its latest block is complete;
- staged, unstaged, and untracked working-tree state; and
- the dead worker's accessible workspace state, as defined by the backend reference.

Record each result in `state.md` as a `Foreman observation` with its probe locator and observation time. Record `none observed` when a probe succeeds and finds nothing; record `inaccessible` or `unreconciled` when it cannot settle the state. These observations are a recovery inventory, not facts and not permission to repeat a write.

Escalate before replacement when uncommitted worker-only state is inaccessible, dirty shared-checkout state cannot be attributed safely, or an external effect cannot be reconciled. Preserve the workspace; do not clean it, switch away, recreate a change request, or retry an external write.

When recovery is safe, spawn a fresh worker under the backend's existing attempt rule. Add the recovery inventory and prior report path to the assignment as attributed context. Require the replacement to inspect the authoritative git, tracker, report, working-tree, and accessible-workspace sources; record in its report whether it verified or discarded each observation; then resume the verified existing work. The foreman records those dispositions in `state.md` after accepting the report. The replacement must not recreate a branch, commit, change request, external write, or complete report section that already exists. After dispatch, use the backend's existing wake mapping without change.

## Blocked-worker rule

A worker blocked on a prompt is waiting on a permission request or a question. Read the prompt with `status`. Resolve it when the answer follows from the task and its committed artifacts and the action stays inside the task's scope and the worker's own workspace; deliver the answer per the `answer` flag (`interactive`: reply and re-arm `await`; `respawn`: new worker, decision in the envelope, prior report path attached). Escalate — naming what it is stopping on — when resolving would take the human: an action outside that scope or workspace, anything destructive or irreversible, credentials or secrets, a question the foreman would have to guess about. A worker's denied `gh pr merge` is never approved — the foreman merges (`references/loop.md`, step 10).

## Identity

Which account merges, comments, and pushes is set by the backend's environment (`GH_CONFIG_DIR`, git `user.*` in the workspace), not by the skill. Requirement: the foreman's `gh` identity has write on the repository; the human stays the release-branch and fast-track authorizer.

## Adding a backend

One file, `references/backends/<name>.md`, with: the four primitives, the four flags, the await discipline's backend-specific commands, PR-tracking hook if any, workspace notes (shared checkout vs per-worker worktree — the run directory is always an absolute path in the foreman's checkout), and the runner's known traps. Declare `n/a` for any eval scenario the backend cannot express and state the degradation.
