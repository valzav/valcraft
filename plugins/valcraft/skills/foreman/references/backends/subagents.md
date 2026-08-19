# Backend: `subagents`

Use the active host's native subagent tools. The host selects its mapping; project
configuration does not add another backend.

## Flags

| Flag | Claude Code | Codex |
| --- | --- | --- |
| `wake` | `event` | `foreground` |
| `answer` | `respawn` | `respawn` |
| `harnesses` | active session harness | active session harness |
| `release` | worker ends on return | worker ends on return |
| workspace | shared checkout | shared checkout |

Fresh context supplies Review independence. Do not override a model unless explicit
project configuration names one.

## Dispatch

Claude Code uses a fresh Agent dispatch named from the logical worker identity. Record
the returned handle as the physical identity.

Codex uses `spawn_agent` with `fork_turns: "none"`. Convert the complete logical name
to lowercase underscore form, preserving every identity digit. For example,
`drafter-F001-T002` becomes `drafter_f001_t002` and
`forge-Q1000-QT001` becomes `forge_q1000_qt001`. A respawn appends the next unused
dispatch discriminator and calls `spawn_agent` again; never use `followup_task` on the
old physical worker. Record both task name and returned agent id.

The native call folds spawn and assign together. The worker's final channel carries
only the assigned report path and producer terminal status line.

## Claude Code event wake

Establish the completion notification with dispatch before ending the parent turn. On
wake, attribute the return to the dispatched physical worker, record it, and apply the
six-return contract. A semantic blocked or question producer report is
`report_available`. A delivery failure before the worker acted is `dispatch_error`.
Worker death is `dead`.

Do not foreground wait, schedule polling, or inspect the report file for completion.

## Codex foreground wake

Keep the parent turn active. Before each `wait_agent`, consume a completion already
delivered for the assigned agent. Resolve the result only for that physical agent:

- completion with a report path is `report_available`;
- a permission prompt is `permission_blocked`;
- a completed agent without a report is `idle_without_report`;
- a dispatch failure is `dispatch_error`;
- terminal worker failure is `dead`;
- a foreground timeout is `wait_timeout`.

When `wait_timeout` returns and the assigned agent remains active, record it and re-arm
`wait_agent` in the same turn. Do not send a final answer, working-status message,
continue prompt, interval, retry cap, or report-file poll. Absence from live status
without another terminal return advances nothing.

## Shared checkout

Workers run serially. The run directory is the absolute `.foreman/<run-id>/` path in
the shared checkout. Before a new task, Foreman's Ready recovery requires a clean
checkout and records branch, exact HEAD, staged, unstaged, and untracked state. Never
clean, stash, reset, fetch, switch, synchronize, or create a branch through dirt.

On death, inventory the shared checkout in place. A fresh replacement verifies and
resumes attributable work. Unresolved attribution or an unreconciled external effect
blocks replacement.

## Land execution

Apply the shared authority rule in [`README.md`](README.md#permission-prompts) with these
transport mappings:

| Field | Mapping |
| --- | --- |
| Execution capability | `shared backend permission` |
| Permission signal | native host permission prompt or host-enforced denial |
| Permission return | `permission_blocked` |
| Producer failure | `Land report` |

## PR tracking

None. Forge owns task-PR creation. Temper owns retrospective-PR creation. Review and
Land receive exact targets through their assignments.
