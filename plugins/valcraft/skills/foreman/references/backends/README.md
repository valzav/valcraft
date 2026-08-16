# Backends

A backend is how the foreman runs workers. The loop never touches a runner directly; it calls four primitives and reads two capability flags, and each backend reference says how its runner provides them. `foreman_backend` in the project block selects the reference.

## Primitives

| Primitive | Meaning                                                                                                                        |
| --------- | ------------------------------------------------------------------------------------------------------------------------------ |
| `spawn`   | Start a fresh worker of a role on a harness. Cold context, no inheritance from the foreman.                                    |
| `assign`  | Deliver an assignment envelope (`references/contracts.md`) to a worker.                                                        |
| `await`   | Learn that a worker finished, blocked, or died — and which. Returns one of `report`, `blocked`, `idle-without-report`, `dead`. |
| `status`  | Inspect a worker: liveness, and the text of a prompt it is blocked on. May be `none`.                                          |

Some backends fold `spawn` and `assign` into one operation; the reference says so.

## Capability flags

| Flag        | Values                     | Meaning                                                                                                                                                                                                             |
| ----------- | -------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `wake`      | `event` \| `poll`          | `event`: `await` re-invokes the foreman when it completes, so the foreman ends its turn after arming it. `poll`: the foreman must check on its own schedule.                                                        |
| `answer`    | `interactive` \| `respawn` | `interactive`: a blocked worker can receive an answer and continue. `respawn`: the worker is one-shot; a block or question ends it, and the foreman spawns a new worker with the decision included in the envelope. |
| `harnesses` | list                       | Which harnesses `spawn` offers. Two or more enable the second-harness rule for `planner` and `reviewer-2`; one means independence by fresh context alone.                                                           |
| `release`   | how workers end            | What the foreman does at step 10 to end a task's workers, and what it must not do.                                                                                                                                  |

The foreman degrades explicitly per flag. It never assumes an event wake, an interactive answer, or a second harness the reference does not declare.

## Await discipline

Applies to every backend, in this order:

1. **Confirm the assignment started.** After `assign`, use `status` (or the backend's equivalent) to see the worker processing before arming `await`. An idle worker with no report file means the delivery silently failed — re-assign instead of waiting.
2. **Check before waiting.** Read the worker's report file and `status` once before arming `await`. A worker that finished before the wait started never touches the file again; act on the report immediately.
3. **Arm `await` and end the turn** on an `event` backend; on a `poll` backend, poll on the interval the reference states and never wait in the foreground of an event backend.
4. **Act on the outcome.** `report` → check completeness (`references/contracts.md`), then act. `blocked` → blocked-worker rule below. `idle-without-report` → `status` to read the worker's last output; re-assign once, then escalate. `dead` → respawn once with the same envelope, then escalate. "Once" is the two-attempt rule in `references/hygiene.md` (owner's standing orchestrator rules).

## Blocked-worker rule

A worker blocked on a prompt is waiting on a permission request or a question. Read the prompt with `status`. Resolve it on the foreman's own judgement when the answer follows from the task: approve an action inside the task's scope and the worker's own workspace; answer a question the spec, design, plan, or assignment already settles. Deliver the answer per the `answer` flag (`interactive`: reply to the prompt and re-arm `await`; `respawn`: new worker, decision in the envelope, prior report path attached). Escalate to the human when the prompt is serious: an action outside the task's scope or workspace, anything destructive or irreversible, credentials or secrets, or a question the foreman would have to guess about. Name what it is stopping on. A denied `gh pr merge` from a worker is never resolved by approval — the foreman merges itself.

## Identity

Which account merges, comments, and pushes is set by the backend's environment (`GH_CONFIG_DIR`, git `user.*` in the workspace), not by the skill. Requirement: the foreman's `gh` identity has write on the repository; the human stays the release-branch and fast-track authorizer.

## Adding a backend

One file, `references/backends/<name>.md`, with: the four primitives, the four flags, the await discipline's backend-specific commands, PR-tracking hook if any, workspace notes (shared checkout vs per-worker worktree — the run directory is always an absolute path in the foreman's checkout), and the runner's known traps. Declare `n/a` for any eval scenario the backend cannot express and state the degradation.
