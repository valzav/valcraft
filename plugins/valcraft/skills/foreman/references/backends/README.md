# Backends

A backend runs fresh workers; it never changes skill ownership. Missing
`foreman_backend` selects native `subagents`.

## Primitives and flags

| Primitive | Meaning |
| --- | --- |
| `spawn` | Start one fresh physical worker for the canonical logical identity. |
| `assign` | Deliver the assignment envelope and exact report path. |
| `await` | Return one of the six backend returns. |
| `status` | Inspect only liveness or a blocked prompt. |

Backends declare `wake` (`event`, `foreground`, or authorized `poll`), `answer`
(`interactive` or `respawn`), available harnesses, release behavior, and workspace
ownership.

## Await discipline

1. Confirm assignment delivery with backend status or its equivalent.
2. Before waiting, consume any terminal return already delivered for the active physical
   worker.
3. Record exactly one return in `state.md`:
   `report_available`, `permission_blocked`, `idle_without_report`, `dispatch_error`,
   `dead`, or `wait_timeout`.
4. Bind it to the assignment id, logical worker, physical worker, and report path.
5. Apply [`../contracts.md`](../contracts.md)'s backend transition. Only
   `report_available` permits opening the assigned report.

`report_available`, `idle_without_report`, `dispatch_error`, and `dead` end the current
await. `permission_blocked` waits for an allowed answer or escalation. `wait_timeout`
is nonterminal and valid only for foreground waiting; if the worker remains active,
re-arm await in the same parent turn.

Never poll a report file on event or foreground backends. Never treat absence from a
live-only status list as success. A producer's semantic `Status: blocked` arrives under
`report_available`, never `permission_blocked`.

## Dead-worker recovery

Before replacement, record the `dead` return and inventory:

- git refs, branches, commits, and exact SHAs;
- current tracker and PR state;
- assigned report path and completeness;
- staged, unstaged, and untracked state; and
- the dead worker's accessible workspace state.

Record each probe, locator, observation time, and result in `state.md`. Escalate when
worker-only state is inaccessible, shared-checkout dirt cannot be reconciled, or an
external effect remains ambiguous. Preserve the workspace.

A safe replacement receives the same logical identity, a fresh physical identity and
report path, the prior inventory, and exact predecessor target. It verifies or discards
each observation before resuming. Never recreate an existing branch, commit, PR,
external write, or report section. Reject every late predecessor return or report after
the replacement becomes active.

## Permission prompts

For backend `permission_blocked`, read the prompt with `status`. Answer only when the
committed task contract settles it and the action stays within the worker's assigned
role, workspace, and target-bound authority. Otherwise escalate with the exact prompt.
Use the backend's `answer` behavior; a respawn always receives a new physical identity.

No prompt can grant merge permission to Foreman or another producer. Land may merge
only after its own per-dispatch Land-scoped capability probe passes. Shared native
parent permission and Agent Orchestrator project permission are insufficient.

## Active transport deviations

Keep only deviations that change dispatch, await, wake, or workspace behavior.

| Backend | Active deviation | Changed primitive | Coverage key | Discriminating eval |
| --- | --- | --- | --- | --- |
| Claude Code native | completion event wakes the parent after it ends the turn | wake/await | `transport:claude-event-wake` | Foreman eval 7 |
| Codex native | parent remains active and uses foreground `wait_agent`; timeout re-arms without a user message | wake/await | `transport:codex-foreground-wake` | Foreman eval 18 |
| Native subagents | all roles share the parent checkout | workspace | `transport:native-shared-workspace` | Foreman eval 35 |
| Agent Orchestrator | authorized background polling converts AO session state to one backend return | wake/await | `transport:ao-poll-wake` | Foreman eval 63 |
| Agent Orchestrator | a git-backed dispatch uses an isolated physical branch seeded from the predecessor SHA | dispatch/workspace | `transport:ao-isolated-branch` | Foreman eval 62 |
| Agent Orchestrator | a no-git workflow target uses a transport-only branch seeded from the verified default-branch SHA | dispatch/workspace | `transport:ao-no-git-workspace` | Foreman eval 67 |

The corresponding backend reference owns commands. Remove a row when the transport no
longer deviates; do not preserve historical notes here.

## Adding a backend

Define the four primitives, six returns, flags, workspace model, capability probe,
active deviations with eval ids, and recovery access. Declare an unsupported scenario
as `n/a` with the exact degradation.
