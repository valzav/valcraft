# Backend: `ao`

Foreman runs in an Agent Orchestrator project. Every worker receives an isolated worktree on a unique physical branch. Require the installed `ao` CLI, tmux, and an exact project id.

## Flags

| Flag | Value |
| --- | --- |
| `wake` | authorized background `poll` that wakes Foreman with one backend return |
| `answer` | `interactive` through `ao send` |
| `harnesses` | project-supported harnesses; use a distinct harness for Review when available |
| `release` | terminate the worker session after its accepted report; never run project-wide cleanup |
| `review continuity` | kept active — a Review worker with material findings keeps its session and worktree and receives its closure check and any second full round through `ao send`; released after the round's final report |
| workspace | isolated worktree on the assigned physical branch |

## Physical identity

Keep the full canonical logical identity in the assignment and `workers.md`. Map role families only for the physical alias prefix:

- Draft: `d`;
- Forge: `f`;
- every Review mode: `r`;
- Land: `l`;
- Temper: `t`.

Do not define aliases for retired role families or for producer-owned substeps. Only the five role families above receive AO alias prefixes.

For dispatch ordinal zero, hash the UTF-8 canonical logical identity with SHA-256. For later dispatches, hash `<logical identity>\ndispatch:<ordinal>`. Form `<role>-<hex-prefix>` from the lowercase hexadecimal digest with as many characters as fit AO's 20-character name contract. If current project sessions or any `workers.md` row already owns the result, rehash `<dispatch preimage>\ncollision:<n>` until it is unused. Preserve all prior rows.

## Physical branch guard

Derive a unique physical branch from the physical alias. Resolve one workspace seed before worker creation:

- For a git-backed workflow target, verify the predecessor's exact full SHA and canonical remote ref from the accepted producer report. Use that SHA as the workspace seed.
- For a workflow target whose branch, PR, commit, and target SHA are all `none`, verify the live remote `HEAD` symref and host-reported default branch agree. Fetch that ref. Use its exact SHA only as the workspace seed. Keep the workflow target's git identity `none`.

Then apply the physical guard:

1. Record the workspace seed SHA and whether it is predecessor or transport-only state.
2. Inspect local refs and `git worktree list --porcelain`.
3. When the physical branch is absent, create it at the workspace seed SHA.
4. When it exists only as this not-yet-spawned dispatch's recorded branch, require its head to equal the workspace seed SHA exactly.
5. Stop before spawn when the branch is stale, belongs to another dispatch, or is already checked out in any worktree.

Never reset, reuse another dispatch's branch, force-push, or publish the physical branch as the canonical task ref. A transport-only seed is never completion evidence, a Review target, or a replacement for the workflow target's `none` fields. Draft, Forge, and task-PR Land revalidate the canonical remote ref before a non-force transfer.

## Dispatch and assignment

Run:

```sh
ao spawn --project <project-id> --harness <harness> --name <physical-alias> --branch <physical-branch>
```

Record the returned session id, alias, branch, workspace seed SHA and kind, logical identity, and dispatch ordinal in `workers.md`. Assign the envelope with:

```sh
ao send --session <session-id> --message "<envelope>"
```

Confirm visible processing with `tmux capture-pane -p -t <session-id>`. An idle composer without delivered assignment evidence is `dispatch_error`; retry under the established two-attempt rule.

## Await

Before arming, read AO status once and consume any already available attributed report. Then use the owner's standing 30-second AO poll schedule. The background waiter snapshots the assigned report by checksum and maps only the active session:

```sh
S="<session-id>"; R="<assigned-report-path>"
snap() { cksum "$R" 2>/dev/null || echo none; }
B=$(snap); seen=${SEEN:-0}
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

Run the waiter in the background and end the parent turn only after it is armed. On wake, attribute and record its exact return before another action. A command failure before the waiter starts is `dispatch_error`. AO does not emit `wait_timeout`; that return belongs only to foreground backends. The waiter is a background process, so the controller's own shell command limit does not bound it; never run it in the foreground, where that limit would kill it into a lost handle.

The 30-second interval is the owner's standing orchestrator rule from `orchestrator-template.md` (2026-08-15 revision); it is not a Foreman-derived retry limit.

For a blocked prompt, inspect the smallest tmux window needed. Send an allowed answer with `AO_SESSION_ID= ao send --session <id> --message "<answer>"`, then re-arm await. Never write directly to tmux.

### An escalated gate stays under observation

Escalation names the gate; it does not end the await. The operator can answer the prompt in the worker's own tmux window, and the worker then finishes with no message to the controller. After escalating, re-arm the same waiter on the same session with `SEEN=1`: delivery was confirmed before the block, and a waiter that starts at `seen=0` never emits `idle_without_report` for a session that leaves `blocked` and settles without the poll observing `working`. A `report_available` that arrives while the gate is open resolves it: record the gate as answered in the session, with the status change and the attributed report, and continue under return precedence. A session that left `blocked` and settled `idle` without a report is `idle_without_report`, not a resolved gate. A session still `blocked` when the waiter next wakes stays at the gate; re-arm and keep waiting for the operator.

## Review continuity

AO keeps a worker session and its worktree alive after a turn, so this backend keeps a Review worker active for its own round, as [`../hygiene.md`](../hygiene.md#workers) allows.

1. **Who is kept.** Only a Review worker (`r`-alias) whose accepted report returned material findings. A Review report with verdict `pass`, every producer (Draft, Forge, Temper), and Land are released or handled as before: a producer's remediation is always a fresh session, alias, and physical branch.
2. **What waiting means.** The kept session is `idle` and executes nothing; its worktree stays at the head it reviewed. Do not send to or inspect it while the producer is active.
3. **Each follow-up is a new assignment.** The closure check and any second full round take the next assignment id and dispatch ordinal, a fresh and absent report path, and their own `workers.md` row and assignment checkpoint. The physical identity — session id, alias, and physical branch — is the initial dispatch's, recorded again on the new row and marked continued. The alias keeps its original preimage; only the report path advances.
4. **Revalidate before the follow-up send.** `ao session ls --project <project-id> --json` must still list the recorded session id, `idle`, under the recorded alias. A missing or replaced session is an observation, not a backend return: the kept worker has no active assignment. Record it with the status evidence, skip the dead-worker inventory, and dispatch the closure check as a fresh physical worker with the same logical identity through the ordinary dispatch steps.
5. **The worktree is stale by construction.** The kept reviewer's worktree sits at the head it reviewed, and the producer's resolution landed on the canonical ref. The follow-up envelope carries the resolution report path, the R-IDs, and the exact new head, and requires the reviewer to fetch the canonical ref and inspect each resolving commit and locator at that head, re-running the R-ID's reproduction there. Memory of the first review, and the old worktree contents, are not evidence.
6. **Release.** After the round's final report — a closure check with no open material finding, a second-round closure, or an escalation — terminate the session as usual.

Delivery confirmation and return precedence are unchanged for a follow-up `ao send`.

## Workspace and recovery

Workers write reports to the absolute run path in Foreman's checkout. On death, inspect the dead worktree, refs, exact SHAs, canonical remote state, PR or tracker effects, report path, and working-tree state. A safe replacement gets another alias and physical branch at the verified workspace seed. It recovers verified work without repeating an external effect. Reject the predecessor's later report after replacement.

Project-wide session cleanup can delete a live orchestrator workspace. Foreman never runs it. Report pending reclamation to the operator after no orchestrator session is live.

## PR tracking

After accepting a Forge or Temper report that names an existing PR, associate that PR with the producer session using AO's claim-PR command. Do not infer a PR from state or claim one for Review or Land.

## Land execution

Apply the shared authority rule in [`README.md`](README.md#permission-prompts) with these transport mappings:

| Field | Mapping |
| --- | --- |
| Execution capability | `shared backend permission` |
| Permission signal | AO blocked permission prompt |
| Permission return | `permission_blocked` |
| Producer failure | `Land report` |
