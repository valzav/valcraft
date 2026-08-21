# Backend: `herdr`

Foreman runs inside a [Herdr](https://herdr.dev) pane and dispatches each worker as a fresh coding agent in a pane of one named project session. Require the `herdr` binary, `HERDR_ENV=1`, the project's named session, and both mapped harnesses.

Workers share Foreman's checkout and canonical task branch. Isolation comes from a fresh worker per dispatch and serial execution, not from a worktree, so the shared-checkout rules in [`subagents.md`](subagents.md#shared-checkout) apply unchanged.

## Flags

| Flag | Value |
| --- | --- |
| `wake` | `foreground` — `agent prompt --wait` blocks for the worker's turn; a lost handle re-arms with standalone `agent wait` |
| `answer` | `interactive` through `agent send-keys` |
| `harnesses` | Claude and Codex, assigned per role by the table below; a missing mapped harness fails readiness |
| `release` | close the worker's own workspace; never `session stop`, `session delete`, or any pane the run does not own |
| workspace | Foreman's checkout on the canonical task branch, shared and serial |

## Role-to-harness assignment

Each Review runs on the model that did not produce its target.

| Role | Harness | Role | Harness |
| --- | --- | --- | --- |
| Draft | Codex | Land | Claude |
| PlanReview | Claude | Temper | Claude |
| Forge | Claude | RetroReview | Codex |
| CodeReview | Codex | EvidenceReview | Codex |

Never substitute the other harness for a missing one; that silently removes the independence this backend exists to provide.

## Readiness

Fail before run creation or task selection when any of these does not hold. Never fall back to another backend.

1. `HERDR_ENV=1` and `herdr --version` reports the release the project requires.
2. The project's named session exists and is running.
3. Both mapped harnesses are startable in that session.
4. This controller holds the project's lease.

### Address the session by socket path

Herdr injects `HERDR_SOCKET_PATH` into every pane, and a socket override outranks `HERDR_SESSION`. An orchestrator that exports only the session name reads **its own** session and receives a plausible, wrong answer with no error. Resolve the path explicitly and confirm the returned `socket:` matches:

```sh
export HERDR_SOCKET_PATH="$HOME/.config/herdr/sessions/<project-session>/herdr.sock"
herdr status server        # verify the reported socket is the one just set
```

### Controller lease

One controller per project pool. A readiness check alone cannot enforce this — two controllers pass it simultaneously — so claim atomically:

1. `mkdir .foreman/controller.lock` in the project checkout. Failure means another controller holds it.
2. Write the owner's session, workspace, and pane id into the lock directory.
3. Release only as the recorded owner, at run end.
4. A lock whose owner pane is absent from the named session is stale: record the observation and the reclaim in `state.md`, then take it. Never remove a lock whose owner pane is still live.

## Physical identity

The physical worker is the returned pane id in the recorded session, plus the live agent name. A name alone is not an identity: it follows the pane's current occupant and is released when that agent exits, so a reused name can address a different process.

Derive the agent name from the canonical logical identity and dispatch ordinal, normalized to Herdr's `[a-z][a-z0-9_-]{0,31}` contract, and collision-check it against `agent list` and every `workers.md` row before use. Record session, workspace, tab, pane, agent name, harness, dispatch ordinal, and report path.

## Spawn

Record each transition in `state.md` before attempting the next, so an interrupted call can be reconciled without creating a second worker.

1. **Checkout verified** — the shared checkout is clean, on the canonical task branch, at the recorded predecessor SHA. Dirt, another branch, or another head stops the dispatch. Never clean, stash, reset, switch, or fetch through dirt.
2. **Report path claimed** — the assigned path is unique and absent.
3. **Workspace returned** — `herdr workspace create --cwd <checkout> --no-focus`; read `.result.root_pane.pane_id`.
4. **Agent ready** — `herdr agent start <agent-name> --kind <claude|codex> --pane <pane-id>`. A start that returns `agent_not_ready` leaves the name usable: read the pane before deciding.
5. **Revision recorded** — the dispatched skill's `version` content hash from the plugin's `skills/index.json`, per [`../../templates/run-dir.md`](../../templates/run-dir.md).

A worker that blocks during startup is not a failure. Herdr reports it as `blocked` and `agent list` shows it; clear only a prompt the committed contract settles for a directory this run owns.

## Assign and await

`agent prompt --wait` carries the assignment and the first foreground await together:

```sh
herdr agent prompt <agent-name> "<envelope>" --wait --timeout <ms>
```

### Delivery is not confirmed by a successful return

`agent prompt` can return `agent_prompted` while the text never reaches the agent's composer and the occupant never leaves its settled state. The loss is intermittent and silent, and an identical later prompt may land.

After every submission, require one of: an observed `working` state for the exact occupant, or the attributed report. A settled occupant with neither is `dispatch_error` — reconcile against the exact worker and report under the established two-attempt rule. Never resubmit an assignment whose delivery is unknown.

### Return precedence

On every wake, resolve in this order and record exactly one return:

1. A signal bound to a physical identity whose assignment already reached a terminal return is **not** a return. Record it as an observation against the released worker and continue awaiting the active one.
2. An attributed change to the assigned report path — `report_available`.
3. A current host prompt on the recorded pane — `permission_blocked`.
4. A settled occupant (`idle` or `done`) with no report — `idle_without_report`.
5. `agent_not_found`, or a pane whose occupant is not the recorded one — `dead`.
6. A transport or command failure — `dispatch_error`.
7. The host timeout with the same worker still active — `wait_timeout`, nonterminal; re-arm in the same parent turn.

`working`, `unknown`, and absence from a live-name list never prove completion. `done` is Herdr's word for idle after unseen work, not for success.

### After a lost foreground handle

Re-arm without resending. Standalone `agent wait` observes the same worker to its settled state, and a worker that already settled returns immediately rather than hanging:

```sh
herdr agent wait <agent-name> --timeout <ms>
```

Reconcile the recorded assignment checkpoint against the report and the exact occupant first. An assignment recorded as submitted is never submitted again on the strength of a missing return alone.

## Permission prompts

Read the blocked prompt with `herdr agent read <agent-name> --source recent-unwrapped`, revalidate that the pane still holds the recorded occupant and that the prompt is the one observed, then answer with `herdr agent send-keys <agent-name> <key>`. Escalate the exact prompt when the occupant changed, the prompt changed, or the answer would widen scope. See [`README.md`](README.md#permission-prompts) for the authority rule.

## Release and recovery

Release closes the accepted worker's own workspace and touches no Git state. The shared checkout and canonical branch are the durable record.

A dead or replaced worker leaves its commits, dirt, and partial report in place for the replacement to inventory; the next task start is gated on a clean checkout. Follow [`README.md`](README.md#dead-worker-recovery) for the inventory, then dispatch the same logical worker under a new pane, agent name, and report path. Reject a predecessor's late report or lifecycle signal after replacement.

Never run `herdr update`, `herdr server stop`, or `session stop` during a run: an update terminates pane processes, and stopping the session kills every worker including the orchestrator's own pane.

## PR tracking

None. Forge owns task-PR creation, Temper owns retrospective-PR creation, and Review and Land receive exact targets through their assignments.

## Land execution

Apply the shared authority rule in [`README.md`](README.md#permission-prompts) with these transport mappings:

| Field | Mapping |
| --- | --- |
| Execution capability | `shared backend permission` |
| Permission signal | Herdr `blocked` agent state on the recorded pane |
| Permission return | `permission_blocked` |
| Producer failure | `Land report` |
