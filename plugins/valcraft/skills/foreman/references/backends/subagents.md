# Backend: `subagents` — native host subagents

The foreman and workers run through the active host's native subagent tools. This remains one portable backend: the active host selects the primitive mapping; project configuration does not.

## Flags

| Flag        | Value                                                                                                                                                                         |
| ----------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `wake`      | Claude Code: `event`; Codex: `foreground`                                                                                                                                     |
| `answer`    | `respawn` — a subagent is one-shot; a block or question ends it                                                                                                               |
| `harnesses` | one (the session's model). Independence comes from fresh context: each role is a new agent with no inherited context, and the second-harness rule is satisfied by that alone. |
| `release`   | none needed — a subagent ends when it returns; never leave one waiting on a message                                                                                           |

## Primitives

- `spawn` + `assign` are one native subagent call with a fresh general-purpose worker. The assignment carries the canonical logical identity and report path. Do not pass a model override unless explicit project configuration names one.
  - Claude Code: use the Agent tool with the logical worker name and no fork. Record that name as the physical handle.
  - Codex: use `spawn_agent` with `fork_turns: "none"`. Derive a unique lowercase_underscore `task_name` from the complete logical worker identity: `planner-F001-T002` → `planner_f001_t002`; `worker-Q1000-QT001` → `worker_q1000_qt001`. Preserve every identity digit. When that name already belongs to a dispatch in the current agent tree or `workers.md`, append the next unused lowercase_underscore dispatch discriminator. Record both returned agent id and `task_name` as the physical handle. Every respawn is another fresh `spawn_agent`, never `followup_task` on the returned agent.
- `await` follows the active host mapping below. On Codex, use native `wait_agent`; resolve its return for the assigned agent before another action. The worker's final text carries only the report path and `Status:` line; the report remains on disk.
- `status`: Claude Code has none between dispatch and its event. On Codex, use `list_agents` plus available completion messages for the assigned agent; never infer a terminal outcome from its absence in a live-only listing.

## Await discipline on this backend

Do not add an external orchestrator, scheduled or periodic polling, report-file polling,
a wait interval, a retry cap, or a user-visible working-status requirement.

### Claude Code — event

The Agent dispatch establishes a completion notification before the foreman ends the parent turn. The host re-invokes the foreman when the notification arrives. Consume its status, validate a `done` report, and continue the loop. On `blocked` or `question`, follow the existing rule and respawn with the decision and prior report path. On a dispatch or delivery failure before any evidence that the worker acted, apply the two-attempt rule. On `dead`, apply the recovery inventory in `README.md`. Do not foreground-wait or schedule polling.

### Codex — foreground

Keep the parent turn active after `spawn_agent` and await the assigned agent in the foreground. Before the first wait, consume any status or completion message already delivered; this covers completion between dispatch and await without report-file polling.

Resolve every wait return through the assigned agent's state:

- A timeout while the assigned agent remains active is nonterminal. Re-arm foreground await in the same turn. Do not send a final response, a working-status message, or a continue prompt.
- A completion delivered with `trigger_turn: false` is expected because the parent turn is already active. Consume it, read and validate the report, record the terminal state, and continue the loop.
- `blocked` and `question` follow the existing resolution or escalation rules. A respawn is a fresh agent with the decision and prior report path.
- A dispatch error before the worker could act follows the two-attempt rule. `dead` follows the recovery inventory in `README.md`. Absence from live status without a completion or other terminal evidence is not success and cannot advance the loop.

## Workspace and the run directory

Foreman and workers share one checkout. Consequences:

- The run directory is `<checkout>/.foreman/<run-id>/`; the envelope still carries the absolute path.
- Workers run serially, so `valcraft:forge`'s branch switch happens in the shared
  checkout under the foreman. The foreman reads no repository files during a task, so
  this is safe.
- Step 0 owns shared-checkout recovery. Before any fetch, switch, synchronization, or
  task-branch creation, Foreman requires a clean checkout and records the current branch
  and exact HEAD. Any staged, unstaged, or untracked change stops in place, whether or
  not its owner is known. After a merge, the next task returns through step 0's four-way
  default-branch classification instead of assuming a pull is safe.
- Step 4's "copy the plan into your worktree" clause is inert — same path, same checkout.
- `valcraft:review`'s revert-the-fix check uses a disposable `git worktree` of its own; the reviewer removes it before returning.

On worker death, the shared checkout is the accessible worker workspace. Inventory its current branch, refs, exact commit SHAs, report path, and staged, unstaged, and untracked state in place. Do not clean, reset, switch, or stash it. If the dirty state is attributable and recoverable, the fresh replacement verifies it and resumes in the same checkout. If attribution is unresolved, or an external effect cannot be reconciled, escalate before replacement. This recovery step does not change Claude Code's event wake or Codex's foreground wake.

Dead-worker replacement is recovery of an existing task, not permission to pass step 0's
clean task-start gate or to fetch, switch, synchronize, or create another branch while
the shared checkout is dirty.

## Merges

The foreman merges (`references/loop.md`, step 10); the classifier that can deny it here is this session's own permission mode.

## PR-tracking hook

None. Check results are read at steps 9 and 10, then correlated with the exact PR head
under `loop.md`'s shared applicability classifier. A check listing alone cannot prove
`none-applicable`; repository rules, external required checks, and workflows on the
default branch or introduced by the PR are separate sources.

## Eval scenario coverage

The host-specific native-subagent scenarios and the existing backend drills are mapped to eval ids in `evals/scenarios.md`. Codex expresses foreground timeout and early-completion cases. Claude Code's event delivers completion regardless of timing. Both hosts express blocked, escalation, merge-denial, partial-mutation, and review-round cases through the shared loop rules.
