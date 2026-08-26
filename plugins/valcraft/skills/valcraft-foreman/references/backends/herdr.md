# Backend: `herdr`

Foreman runs inside a [Herdr](https://herdr.dev) pane and dispatches workers as fresh coding agents in one named project session. A Review worker with material findings may remain for its closure check under [Review continuity](#review-continuity). Require the `herdr` binary, `HERDR_ENV=1`, the configured session constraint, and every configured harness.

The controller runs inside the project's Herdr session, and that session is the one its own pane belongs to. Read `foreman.herdr.session` and the complete `foreman.herdr.workers` map from the resolved configuration. A non-null session is an assertion, not a pointer. When it is null, use whichever session contains the controller's pane. A controller started in a different session stops instead of retargeting another socket.

Workers share Foreman's checkout and canonical task branch. Isolation comes from a fresh worker per dispatch and serial execution, not from a worktree, so the shared-checkout rules in [`subagents.md`](subagents.md#shared-checkout) apply unchanged.

## Flags

| Flag | Value |
| --- | --- |
| `wake` | `foreground` — `agent prompt --wait` blocks for the worker's turn; a lost handle re-arms with standalone `agent wait` |
| `answer` | `interactive` through `agent send-keys` |
| `harnesses` | Claude, Codex, and Cursor as configured per role; a missing configured harness fails readiness |
| `release` | `herdr pane close <pane-id>` for the worker's own recorded pane; never `session stop`, `session delete`, or any pane the run does not own |
| `review continuity` | kept active — a Review worker with material findings waits in its pane and receives its closure check and any second full round as follow-up prompts; released after the round's final report |
| workspace | Foreman's checkout on the canonical task branch, shared and serial |

## Role configuration

Resolve every dispatch from the matching `foreman.herdr.workers` entry:

| Named state role | Worker key | Must differ from |
| --- | --- | --- |
| Draft | `draft` | `plan_review` |
| PlanReview | `plan_review` | `draft` |
| Forge | `forge` | `code_review` |
| CodeReview | `code_review` | `forge` |
| Land | `land` | `evidence_review` |
| EvidenceReview | `evidence_review` | `land` |
| Temper | `temper` | `retro_review` |
| RetroReview | `retro_review` | `temper` |

The Tune contract guarantees each reviewer uses a different harness from its producer. Revalidate those four pairs during readiness. Never substitute a harness, model, or effort; delegate an invalid map to Tune and resume only after `Status: done`.

## Readiness

Fail before run creation or task selection when any of these does not hold. Never fall back to another backend.

1. `HERDR_ENV=1`, and `herdr --version` reports release 0.8.2 or newer — the verified source of the primitives this contract depends on: `agent_prompt_stalled` from `agent prompt --wait`, `herdr pane close`, and the pane `agent_session` identity reported by `herdr pane get`. An older or unreadable version fails readiness; never degrade to a partial contract.
2. The controller is inside a running Herdr session: `HERDR_SOCKET_PATH` is set and `herdr status server` answers on it. Resolve that socket to its session name through `herdr session list --json` (`socket_path` → `name`; the default session is named `default`) and record the name in `state.md`. When `foreman.herdr.session` is non-null, the resolved name must equal it; on a mismatch fail readiness naming both, and never re-target another session's socket.
3. Every harness named by the worker map is startable in that session, and each reviewer-producer harness pair differs.
4. This controller holds the project's lease.

### The inherited socket is the session

Herdr injects `HERDR_SOCKET_PATH` into every pane, and a socket override outranks `HERDR_SESSION`. Because the controller runs inside the project session, the inherited value is already the right one: use it unchanged for every `herdr` call and confirm it once with `herdr status server`. Never export `HERDR_SESSION` or another socket path to reach a different session — a controller that does so reads one session and spawns in another, with no error from either.

### Controller lease

Allow one controller per project pool. Claim atomically because two controllers can pass a readiness check simultaneously. Create the lock from its owner token so an interruption cannot leave an ownerless lock:

1. Create `.valcraft/foreman/` in the project checkout when absent. Readiness precedes run-directory creation.
2. Read this controller's identity with `herdr pane current`. Write session, workspace id, pane id, the pane's `agent_session` value, and claim time to `.valcraft/foreman/controller.owner.<pane-id>`. Fail readiness when `agent_session` cannot be resolved.
3. Claim generation 1 with `ln .valcraft/foreman/controller.owner.<pane-id> .valcraft/foreman/controller.lock.1`. The hard link fails atomically when the target exists. On failure, resolve the existing generation through step 5.
4. Release only as the recorded owner, at run end: confirm the highest generation's token carries this controller's pane id and `agent_session` value, then remove that generation.
5. The holder is the highest-numbered `.valcraft/foreman/controller.lock.<n>`. It is live only when `herdr pane get <pane-id>` resolves the recorded pane and reports the recorded `agent_session` value. Pane existence alone is insufficient because an ordinary shell can remain after its agent exits. For a live holder, fail readiness naming the owner and remove nothing.
6. For a dead holder, claim generation `n+1` with `ln .valcraft/foreman/controller.owner.<pane-id> .valcraft/foreman/controller.lock.<n+1>`. Never remove or move generation `n` before claiming; another reclaimer may already hold a newer live generation. A failed link loses the race and stops. The winner first records the dead-owner observation, observed generation, and reclaim decision in `state.md`, then records the successful `n+1` claim and removes lower generations. Do not advance the run until both records are present.

After the claim succeeds — generation 1 or a reclaimed generation — title the controller pane with `herdr pane report-metadata <pane-id> --source valcraft-foreman --title <title>`, where `<title>` is `foreman · <session>` and `<session>` is the session name recorded at readiness, so the orchestrator column is identifiable beside its workers. Pass the title as one argument value. Title only after the claim: a controller that loses the race or fails readiness leaves no `foreman` title behind.

## Physical identity

The physical worker is the returned pane id in the recorded session, plus the live agent name. A name alone is not an identity: it follows the pane's current occupant and is released when that agent exits, so a reused name can address a different process.

Derive the agent name from the canonical logical identity and dispatch ordinal, normalized to Herdr's `[a-z][a-z0-9_-]{0,31}` contract, and collision-check it against `agent list` and every `workers.md` row before use. Record session, workspace, tab, pane, agent name, harness, dispatch ordinal, and report path.

## Spawn

Record each transition in `state.md` before attempting the next, so an interrupted call can be reconciled without creating a second worker.

1. **Checkout verified** — at a task's start the shared checkout is clean, on the canonical task branch, at the recorded predecessor SHA. Dirt, another branch, or another head stops the dispatch before any worker is spawned. On that stop, record the branch, the exact head, and the staged, unstaged, and untracked state in `state.md`, and preserve them. Known attribution never waives this task-start gate, including dirt left by a worker whose own recovery is already closed. Never clean, stash, reset, switch, or fetch through dirt.

   A replacement for a dead or replaced worker is the separate existing-task path named in [`../loop.md`](../loop.md) and does not pass this gate: it inherits the predecessor's commits and dirt to inventory them. It requires the completed inventory and a closed predecessor under [Release and recovery](#release-and-recovery) instead.
2. **Report path claimed** — the assigned path is unique and absent.
3. **Pane returned** — the tab keeps one layout: the orchestrator's pane is the full-height left column, and every worker pane lives in one right column, stacked. Choose the split by what is live:
   - no worker pane is live: `herdr pane split --pane <orchestrator-pane-id> --direction right --cwd <checkout> --no-focus`, which creates the right column;
   - one or more worker panes are live (a kept Review worker, a preserved pane not yet moved out): `herdr pane split --pane <live-worker-pane-id> --direction down --cwd <checkout> --no-focus`, from the most recently returned live worker pane, so the new pane stacks under it and the orchestrator keeps its full height.

   Never split the orchestrator's pane while a worker pane is live: that opens a second column and narrows every pane. Read and record `.result.pane.pane_id` before the next call. Release and recovery use the returned pane id. After an interrupted split, inventory `herdr pane list` for an unattributed pane on this checkout and adopt or close it before splitting another.

   Title the returned pane so the operator can read the layout: `herdr pane report-metadata <pane-id> --source valcraft-foreman --title <title>`, where `<title>` is `<role> · <task> · <harness>`: the logical worker name, with the Review role distinguished by mode as `review:plan` or `review:code`; the canonical task identity; and the configured harness. The task identity is untrusted tracker and repository text: pass the title as one argument value and never interpolate it into shell text. A reported title outranks a manual pane name in the split border, so it is the field that is actually read. `--source` scopes the title to the `valcraft-foreman` source; only a caller reporting that source can change or clear it. The title is display-only and never a gate: record a failed report as an observation and continue the dispatch. It survives `pane move --new-tab`, so a preserved pane keeps its title under its new id.

   A preserved pane — a dead worker kept for inventory — must not keep shrinking the tab: move it out with `herdr pane move <pane-id> --new-tab --no-focus` and record the new id; the agent name follows the process and the pane id changes, so update `workers.md` from `.result.move_result.pane.pane_id`.
4. **Agent ready** — translate the configured worker entry to native harness arguments and pass every value as a distinct argument after `--`:
   - Claude: `herdr agent start <agent-name> --kind claude --pane <pane-id> -- --model <model> --effort <effort>`.
   - Codex: `herdr agent start <agent-name> --kind codex --pane <pane-id> -- --model <model> -c model_reasoning_effort=<effort>`.
   - Cursor: construct the catalog model argument `<model>-<effort>`, then run `herdr agent start <agent-name> --kind cursor --pane <pane-id> -- --model <catalog-model>`.

   Construct an argument vector. Build Cursor's catalog model argument as data, never through shell interpolation. Never interpolate a model or effort into shell text. Record harness, model, and effort with the physical identity. A start that returns `agent_not_ready` leaves the name usable: read the pane before deciding.
5. **Revision recorded** — the dispatched skill's `version` content hash from the plugin's `skills/index.json`, per [`../../templates/run-dir.md`](../../templates/run-dir.md).

A worker that blocks during startup is not a failure. Herdr reports it as `blocked` and `agent list` shows it; clear only a prompt the committed contract settles for a directory this run owns.

## Assign and await

Record the assignment checkpoint in `state.md` **before** submission so recovery can distinguish submitted intent without resending unknown work.

`agent prompt --wait` then carries the assignment and the first foreground await together. `agent prompt` takes the prompt as a positional argument, so pass the envelope as one argument value:

```sh
herdr agent prompt <agent-name> <envelope> --wait --timeout <ms>
```

Keep `--timeout` below the controller's own command limit. A Claude Code controller's shell tool kills a command that outlives that limit (2 minutes by default; both tetris drills saw it as exit 144), which turns an ordinary await into a lost handle and a reconciliation instead of a plain `wait_timeout` re-arm. Re-arming is cheap; reconciliation is not. The same bound applies to standalone `agent wait`.

The envelope carries tracker, repository, and report text this run treats as untrusted. Inside a double-quoted shell string, `$(…)`, backticks, and `${…}` in that text execute in the **controller's** shell before Herdr receives the prompt. Build the call as an argument vector, or single-quote with no expansion. Never interpolate the envelope into a double-quoted command string, and never let a quoting choice alter its bytes.

### Delivery is not confirmed by a successful return

Submitted text can fail to reach the agent while its occupant remains settled, even though an identical later prompt may succeed.

`--wait` requires an observed state change after submission before matching a settled state and reports `agent_prompt_stalled` when none follows. Herdr owns that window.

Delivery is confirmed by an observed `working` state for the exact occupant, or by the attributed report. Treat `agent_prompt_stalled`, and any settled occupant with neither, as unconfirmed: record `dispatch_error` and reconcile the pre-call checkpoint against the exact worker and report path under the established two-attempt rule. Never resubmit an assignment whose delivery is unknown. `idle_without_report` applies only after delivery was confirmed.

A submission to an already-blocked agent is rejected with `agent_blocked` before any input is sent. That is not a delivery failure and consumes no attempt: the occupant holds a host prompt, so record `permission_blocked`, answer or escalate under [Permission prompts](#permission-prompts), then submit.

### Return precedence

On every wake, resolve in this order and record exactly one return:

1. A signal bound to a physical identity whose assignment already reached a terminal return is **not** a return. Record it as an observation against the released worker and continue awaiting the active one.
2. An attributed change to the assigned report path — `report_available`.
3. A current host prompt on the recorded pane, or a submission rejected with `agent_blocked` — `permission_blocked`.
4. A settled occupant (`idle` or `done`) whose delivery was confirmed, with no report — `idle_without_report`.
5. `agent_not_found`, or a pane whose occupant is not the recorded one — `dead`.
6. `agent_prompt_stalled`, a settled occupant whose delivery was never confirmed, or a transport or command failure — `dispatch_error`.
7. The host timeout with the same worker still active — `wait_timeout`, nonterminal; re-arm in the same parent turn.

`working`, `unknown`, and absence from a live-name list never prove completion. `done` is Herdr's word for idle after unseen work, not for success.

### After a lost foreground handle

Re-arm without resending. Standalone `agent wait` observes the same worker to its settled state, and a worker that already settled returns immediately rather than hanging:

```sh
herdr agent wait <agent-name> --timeout <ms>
```

Reconcile the recorded assignment checkpoint against the report and the exact occupant first. An assignment recorded as submitted is never submitted again on the strength of a missing return alone.

## Review continuity

Herdr keeps a pane's agent and conversation alive after a turn, so this backend keeps a Review worker for its own round as [`../hygiene.md`](../hygiene.md#workers) allows. Preserve Review independence and shared-checkout serialization as follows.

1. **Who is kept.** Keep only a Review worker (`plan-reviewer`, `code-reviewer`, `retro-reviewer`) whose accepted report returned material findings. This exception does not apply to a reviewer that passed, a producer (Draft, Forge, Temper), or Land. Remediation always uses a fresh producer to avoid anchoring on its prior choice.
2. **What waiting means.** The kept worker is settled (`idle` or `done`) and executes nothing. Between its report and its next prompt it touches no Git state, so the producer's remediation still runs alone in the shared checkout. Do not read from, prompt, or `send-keys` the waiting worker while the producer is active.
3. **Each follow-up is a new assignment.** The closure check and any second full round take the next assignment id and dispatch ordinal, a fresh and absent report path, and their own `workers.md` row and assignment checkpoint. The physical identity — pane id and agent name — is the initial dispatch's, recorded again on the new row and marked continued. The agent name keeps its original ordinal; only the report path advances.
4. **Revalidate before the follow-up prompt.** Require `herdr pane get <pane-id>` to resolve the recorded pane, `agent_session`, and settled occupant. A missing pane, different occupant, or null session means the kept worker is gone. Record that as an observation rather than a backend return because no assignment is active. Skip dead-worker inventory because the settled reviewer touched no Git state and the producer's commits are already recorded. Close the pane if it still exists and confirm it no longer resolves to the recorded name. Dispatch the closure check as a fresh physical worker with the same logical identity through [Spawn](#spawn), without the task-start gate because the producer's head is the expected mid-round state. Continuity is optional.
5. **Memory is not evidence.** The follow-up envelope carries the resolution report path, the R-IDs, and the exact new head, and requires the inspection [`../review-round.md`](../review-round.md) names: each resolving commit and locator, and that R-ID's reproduction re-run against the new head. A closure that cites only its earlier reading of the finding is incomplete.
6. **Release.** After the round's final report — a closure check with no open material finding, a second-round closure, or an escalation — release the pane as usual. A kept worker whose round ends in escalation is released with the escalation, not held for an owner decision.

Submission, delivery confirmation, and return precedence are unchanged for a follow-up prompt; `agent prompt --wait` to the kept name is the same call with the same unconfirmed-delivery rule.

## Permission prompts

Read the blocked prompt with `herdr agent read <agent-name> --source recent-unwrapped`, revalidate that the pane still holds the recorded occupant and that the prompt is the one observed, then answer with `herdr agent send-keys <agent-name> <key>`. Re-arm the await over the answered prompt the same way an escalated gate does, with `--until idle --until done`: a bare wait matches the `blocked` state the answer has not yet cleared and returns the prompt a second time. Escalate the exact prompt when the occupant changed, the prompt changed, or the answer would widen scope. See [`README.md`](README.md#permission-prompts) for the authority rule.

### An escalated gate stays under observation

Escalation names the gate; it does not end the await. The operator can answer the prompt in the worker's own pane, and the worker then finishes with no message to the controller — in the second tetris drill a Forge worker completed twenty-five minutes before the operator told the controller so. After escalating, keep awaiting the same physical worker with `herdr agent wait <agent-name> --until idle --until done --timeout <ms>`, bounded as above and re-armed in the same parent turn. The explicit states are required. Without `--until`, Herdr 0.8.2 matches `idle`, `done`, or `blocked`, so a bare wait on an already-blocked worker returns immediately and re-arming it in the same parent turn spins instead of waiting for the operator. A terminal return that arrives while the gate is open resolves it: record the gate as answered in the pane, with the observed state change and the attributed report, and continue under return precedence. A gate still standing when the bounded await returns `wait_timeout` stays at the gate; re-arm and keep waiting for the operator. A different prompt raised after the operator answers matches neither requested state, so the bounded timeout surfaces it: on that wake, return precedence records `permission_blocked` for the new gate. A worker that left `blocked` without a report is `idle_without_report`, not a resolved gate.

## Release and recovery

Release runs `herdr pane close <pane-id>` for the accepted worker's own recorded pane and touches no Git state. The shared checkout and canonical branch are the durable record. A worker's reported pane title needs no cleanup because it dies with the pane. The orchestrator's own title outlives the run: clear it at run end with `herdr pane report-metadata <pane-id> --source valcraft-foreman --clear-title`, which is honored only from this source.

A dead or replaced worker leaves its commits, dirt, and partial report in place for the replacement to inventory; the next task start is gated on a clean checkout. Follow [`README.md`](README.md#dead-worker-recovery) for the inventory.

Then close the predecessor before the replacement starts. Every role shares one checkout, so a predecessor that is merely unresponsive can still be writing to the files its replacement is about to inventory and change. Close its recorded pane id, then confirm that id no longer resolves to the recorded agent name. A predecessor that cannot be closed as its exact recorded identity blocks replacement and escalates; never start a second worker in the shared checkout while the first may still be live.

Only then dispatch the same logical worker under a new pane, agent name, and report path. Reject a predecessor's late report or lifecycle signal after replacement.

Never run `herdr update`, `herdr server stop`, or `session stop` during a run: an update terminates pane processes, and stopping the session kills every worker including the orchestrator's own pane.

## PR tracking

None. Forge owns task-PR creation, Temper creates no PR because its retrospective is a local gitignored report, and Review and Land receive exact targets through their assignments.

## Land execution

Apply the shared authority rule in [`README.md`](README.md#permission-prompts) with these transport mappings:

| Field | Mapping |
| --- | --- |
| Execution capability | `shared backend permission` |
| Permission signal | Herdr `blocked` agent state on the recorded pane |
| Permission return | `permission_blocked` |
| Producer failure | `Land report` |
