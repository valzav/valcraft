# Backend: `ao`

Foreman runs in an Agent Orchestrator project. Every worker receives an isolated
worktree on a unique physical branch. Require the installed `ao` CLI, tmux, and an exact
project id.

## Flags

| Flag | Value |
| --- | --- |
| `wake` | authorized background `poll` that wakes Foreman with one backend return |
| `answer` | `interactive` through `ao send` |
| `harnesses` | project-supported harnesses; use a distinct harness for Review when available |
| `release` | terminate the worker session after its accepted report; never run project-wide cleanup |
| workspace | isolated worktree on the assigned physical branch |

## Physical identity

Keep the full canonical logical identity in the assignment and `workers.md`. Map role
families only for the physical alias prefix:

- Draft: `d`;
- Forge: `f`;
- every Review mode: `r`;
- Land: `l`;
- Temper: `t`.

Do not define aliases for retired role families or for producer-owned substeps. Only the
five role families above receive AO alias prefixes.

For dispatch ordinal zero, hash the UTF-8 canonical logical identity with SHA-256. For
later dispatches, hash `<logical identity>\ndispatch:<ordinal>`. Form
`<role>-<hex-prefix>` with as many digest characters as fit AO's 20-character name
contract. If current project sessions or any `workers.md` row already owns the result,
rehash `<dispatch preimage>\ncollision:<n>` until it is unused. Preserve all prior rows.

## Physical branch guard

Derive a unique physical branch from the physical alias. Before worker creation:

1. Verify the predecessor's exact full SHA and canonical remote ref from the accepted
   producer report.
2. Inspect local refs and `git worktree list --porcelain`.
3. When the physical branch is absent, create it at the predecessor SHA.
4. When it exists only as this not-yet-spawned dispatch's recorded branch, require its
   head to equal the predecessor SHA exactly.
5. Stop before spawn when the branch is stale, belongs to another dispatch, or is
   already checked out in any worktree.

Never reset, reuse another dispatch's branch, force-push, or publish the physical branch
as the canonical task ref. Draft, Forge, and task-PR Land revalidate the canonical
remote ref before a non-force transfer.

## Dispatch and assignment

Run:

```sh
ao spawn --project <project-id> --harness <harness> --name <physical-alias> --branch <physical-branch>
```

Record the returned session id, alias, branch, predecessor SHA, logical identity, and
dispatch ordinal in `workers.md`. Assign the envelope with:

```sh
ao send --session <session-id> --message "<envelope>"
```

Confirm visible processing with `tmux capture-pane -p -t <session-id>`. An idle composer
without delivered assignment evidence is `dispatch_error`; retry under the established
two-attempt rule.

## Await

Before arming, read AO status once and consume any already available attributed report.
Then use the owner's standing 30-second AO poll schedule. The background waiter snapshots
the assigned report by checksum and maps only the active session:

```sh
S="<session-id>"; R="<assigned-report-path>"
snap() { cksum "$R" 2>/dev/null || echo none; }
B=$(snap); seen=0
while :; do
  [ "$(snap)" != "$B" ] && { echo report_available; break; }
  st=$(ao session ls --project <project-id> --json | jq -r --arg s "$S" '.data[]|select(.id==$s)|.status')
  [ -z "$st" ] && { echo dead; break; }
  [ "$st" = blocked ] && { echo permission_blocked; break; }
  [ "$st" = working ] && seen=1
  [ "$st" = idle ] && [ "$seen" = 1 ] && { echo idle_without_report; break; }
  sleep 30
done
```

Run the waiter in the background and end the parent turn only after it is armed. On
wake, attribute and record its exact return before another action. A command failure
before the waiter starts is `dispatch_error`. AO does not emit `wait_timeout`; that
return belongs only to foreground backends.

The 30-second interval is the owner's standing orchestrator rule from
`orchestrator-template.md` (2026-08-15 revision); it is not a Foreman-derived retry
limit.

For a blocked prompt, inspect the smallest tmux window needed. Send an allowed answer
with `AO_SESSION_ID= ao send --session <id> --message "<answer>"`, then re-arm await.
Never write directly to tmux.

## Workspace and recovery

Workers write reports to the absolute run path in Foreman's checkout. On death, inspect
the dead worktree, refs, exact SHAs, canonical remote state, PR or tracker effects,
report path, and working-tree state. A safe replacement gets another alias and physical
branch at the verified predecessor. It recovers verified work without repeating an
external effect. Reject the predecessor's later report after replacement.

Project-wide session cleanup can delete a live orchestrator workspace. Foreman never
runs it. Report pending reclamation to the operator after no orchestrator session is
live.

## PR tracking

After accepting a Forge or Temper report that names an existing PR, associate that PR
with the producer session using AO's claim-PR command. Do not infer a PR from state or
claim one for Review or Land.

## Land capability

AO project permission is shared and does not prove a per-dispatch Land-scoped grant.
Unless a future installed AO capability probe proves the exact Land dispatch alone can
merge, Land returns `report_available` with
`Status: blocked: operator_action_required — <prepared action>`. Foreman never merges.
