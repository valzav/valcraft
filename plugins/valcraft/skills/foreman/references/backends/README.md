# Backends

A backend runs fresh workers; it never changes skill ownership. Missing `foreman_backend` selects native `subagents`.

## Primitives and flags

| Primitive | Meaning |
| --- | --- |
| `spawn` | Start one fresh physical worker for the canonical logical identity. |
| `assign` | Deliver the assignment envelope and exact report path. |
| `await` | Return one of the six backend returns. |
| `status` | Inspect only liveness or a blocked prompt. |

Backends declare `wake` (`event`, `foreground`, or authorized `poll`), `answer` (`interactive` or `respawn`), available harnesses, release behavior, and workspace ownership.

## Await discipline

1. Confirm assignment delivery with backend status or its equivalent.
2. Before waiting, consume any terminal return already delivered for the active physical worker.
3. Record exactly one return in `state.md`: `report_available`, `permission_blocked`, `idle_without_report`, `dispatch_error`, `dead`, or `wait_timeout`.
4. Bind it to the assignment id, logical worker, physical worker, and report path.
5. Apply [`../contracts.md`](../contracts.md)'s backend transition. Only `report_available` permits opening the assigned report.

`report_available`, `idle_without_report`, `dispatch_error`, and `dead` end the current await. `permission_blocked` waits for an allowed answer or escalation. `wait_timeout` is nonterminal and valid only for foreground waiting; if the worker remains active, re-arm await in the same parent turn.

Never poll a report file on event or foreground backends. Never treat absence from a live-only status list as success. A producer's semantic `Status: blocked` arrives under `report_available`, never `permission_blocked`.

A signal from a physical worker whose assignment has already reached a terminal return is not a backend return. Record it in `state.md` as an observation with the released worker's identity and ignore it. Never treat it as `idle_without_report`; that return applies only to an active assignment.

## Dead-worker recovery

Before replacement, record the `dead` return and inventory:

- git refs, branches, commits, and exact SHAs;
- current tracker and PR state;
- assigned report path and completeness;
- staged, unstaged, and untracked state; and
- the dead worker's accessible workspace state.

Record each probe, locator, observation time, and result in `state.md`. Escalate when worker-only state is inaccessible, shared-checkout dirt cannot be reconciled, or an external effect remains ambiguous. Preserve the workspace.

A safe replacement receives the same logical identity, a fresh physical identity and report path, the prior inventory, and exact predecessor target. It verifies or discards each observation before resuming. Never recreate an existing branch, commit, PR, external write, or report section. Reject every late predecessor return or report after the replacement becomes active.

## Permission prompts

For backend `permission_blocked`, read the prompt with `status`. Answer only when the committed task contract settles it and the action stays within the worker's assigned role, workspace, and target-bound authority. Otherwise escalate with the exact prompt. Use the backend's `answer` behavior; a respawn always receives a new physical identity.

No prompt can grant merge authority to Foreman or another producer. Shared session or project permission may make Land's assigned operation executable, but it grants no mutation authority. Land acts only with exact trusted target-bound authorization and immediate authoritative revalidation. A host permission prompt or host-enforced denial is `permission_blocked`; a tool or credential failure observed inside Land uses Land's `external_blocked` or `partial_completion` report route.

## Backend conformance

Every concrete backend declares Land execution and names an eval that reads that exact backend contract. The static coordination checker rejects an unregistered backend or a row whose eval does not load its reference.

| Backend | Reference | Land execution eval |
| --- | --- | --- |
| `subagents` | [`subagents.md`](subagents.md) | Foreman eval 68 |
| `ao` | [`ao.md`](ao.md) | Foreman eval 69 |
| `herdr` | [`herdr.md`](herdr.md) | Foreman eval 72 |

## Active transport deviations

Keep only deviations that change dispatch, await, wake, or workspace behavior.

| Backend | Active deviation | Changed primitive | Coverage key | Discriminating eval |
| --- | --- | --- | --- | --- |
| Claude Code native | completion event wakes the parent after it ends the turn | wake/await | `transport:claude-event-wake` | Foreman eval 7 |
| Codex native | parent remains active and uses foreground `wait_agent`; timeout re-arms without a user message | wake/await | `transport:codex-foreground-wake` | Foreman eval 18 |
| Native subagents | all roles share the parent checkout | workspace | `transport:native-shared-workspace` | Foreman eval 35 |
| Agent Orchestrator | authorized background polling converts AO session state to one backend return | wake/await | `transport:poll-wake` | Foreman eval 63 |
| Agent Orchestrator | a git-backed dispatch uses an isolated physical branch seeded from the predecessor SHA | dispatch/workspace | `transport:isolated-branch` | Foreman eval 62 |
| Agent Orchestrator | a no-git workflow target uses a transport-only branch seeded from the verified default-branch SHA | dispatch/workspace | `transport:no-git-workspace` | Foreman eval 67 |
| Herdr | submission can settle without delivering; `agent_prompt_stalled`, or a settled occupant with neither an observed `working` state nor the report, is unconfirmed | dispatch/await | `transport:herdr-unconfirmed-delivery` | Foreman eval 73 |
| Herdr | the assignment envelope is passed as one argument value, never interpolated into a shell command string | dispatch | `transport:herdr-argv-envelope` | Foreman eval 84 |
| Herdr | each role is pinned to a fixed harness so every Review runs on the model that did not produce its target | dispatch | `transport:herdr-cross-model-roles` | Foreman eval 74 |
| Herdr | all roles share the orchestrator's checkout and canonical task branch | workspace | `transport:herdr-shared-checkout` | Foreman eval 75 |
| Herdr | a Review worker with material findings is kept active and receives its closure check in the same pane; producers are always fresh | dispatch/await | `transport:herdr-review-continuity` | Foreman eval 85 |
| Herdr | an escalated permission gate stays under foreground observation; an operator answer in the worker's pane resolves it through the worker's terminal return | await | `transport:herdr-gate-observed-in-pane` | Foreman eval 87 |

The corresponding backend reference owns commands. Remove a row when the transport no longer deviates; do not preserve historical notes here.

## Adding a backend

Define the four primitives, six returns, flags, workspace model, Land execution, active deviations with eval ids, and recovery access. An authorized Land worker must be able to execute ordinary default-branch merge and tracker operations; shared backend permission is sufficient execution capability. Return a host permission prompt or host-enforced denial as `permission_blocked`. Preserve producer-owned failures as producer reports. Declare any other unsupported scenario as `n/a` with the exact degradation.
