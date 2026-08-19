# Backend: `ao` — Agent Orchestrator sessions

The foreman is an AO orchestrator session (a Claude Code session spawned by AO with these rules). Workers are AO sessions in the same project, each in its own worktree. Requires the `ao` CLI, tmux, and an AO project id (`<project-id>`).

## Flags

| Flag        | Value                                                                                                                                   |
| ----------- | --------------------------------------------------------------------------------------------------------------------------------------- |
| `wake`      | `event` — via a background Bash wait, below                                                                                             |
| `answer`    | `interactive` — `ao send` into the dialog                                                                                               |
| `harnesses` | `claude-code`, `codex` — second-harness rule applies: `planner` and `reviewer-2` on `codex`, `reviewer-1` and `worker` on `claude-code` |
| `release`   | `ao session kill <id>` per worker at step 10; the foreman never runs `ao session cleanup` (below)                                       |

## Primitives

- `spawn`: AO session names are at most 20 characters. Keep the canonical logical name in the assignment and `workers.md`; never truncate it or cap its numeric width. Derive a physical alias independently as `<role-token>-<digest-prefix>`, where the role token is `p`, `r1`, `w`, or `r2` and the lowercase hexadecimal digest is over the canonical logical identity. Use as many digest characters as fit the 20-character contract. Before `ao session new`, compare the alias with current project sessions and `workers.md`. If another canonical identity owns it, derive a new digest from the canonical identity plus a collision discriminator and check again; never reuse a colliding alias. Then run `ao session new --project <project-id> --agent <harness> --name <physical-alias>` with no initial prompt. This maps `Q-1000 QT-001` without truncation; a forced first-alias collision yields another alias.
- `assign`: `ao send --session <id> --message "<envelope>"`. Then confirm the worker visibly started: `tmux capture-pane -p -t <id>` (no `-S`) shows the composer processing. An idle empty composer plus no report file means the send silently failed (the same trap as slash commands) — re-send.
- `await`: run this as a background Bash command (`run_in_background: true`) and end the turn; its exit re-invokes the foreman with the outcome. `R` is the worker's report path in the run directory.

  ```sh
  S=<worker-session-id>; R="<run dir>/<logical report name>.md"
  snap() { cksum "$R" 2>/dev/null || echo none; }
  B=$(snap); seen=0
  while :; do
    [ "$(snap)" != "$B" ] && { echo report; break; }
    st=$(ao session ls --project <project-id> --json | jq -r --arg s "$S" '.data[]|select(.id==$s)|.status')
    [ -z "$st" ] && { echo dead; break; }
    [ "$st" = blocked ] && { echo blocked; break; }
    [ "$st" = working ] && seen=1
    [ "$st" = idle ] && [ "$seen" = 1 ] && { echo idle-without-report; break; }
    sleep 30
  done
  ```

  The snapshot is a content checksum, not an mtime: a report appended in the same second as the baseline leaves whole-second mtime unchanged, and `stat -f %m` reads nothing on a machine with GNU coreutils. The 30 s poll interval is the owner's standing orchestrator rule (`orchestrator-template.md`, 2026-08-15 revision). Apply the await discipline in `README.md` before arming: read the report file and `ao session ls` once.

- `status`: `ao session ls --project <project-id> --json` for liveness; `tmux capture-pane -p -t <id>` for the prompt text — no `-S` for a liveness check, `-S -50` when hunting a prompt, `-S -200` only when reconstructing a failure. Never write to tmux.

## Answering a blocked worker

`AO_SESSION_ID= ao send --session <id> --message "<answer>"`. Inside the orchestrator session `AO_SESSION_ID` is set, and a plain `ao send` prefixes the message with `[from <session-id>]`, which a dialog does not accept. Then re-arm `await`.

## Workspaces and the run directory

Every AO worker has its own worktree, so a repository-relative `.foreman/` path differs per worker. The run directory is the absolute path inside the foreman's checkout; every envelope carries it, and workers write reports there by absolute path. Step 4's "copy the plan into your worktree" clause is live on this backend.

AO's own mailbox (`~/.ao-mail/<project-id>/<session-id>.md`) is not the wire format. If AO tooling needs it, a worker may mirror its report there; the run directory is the source.

On worker death, inspect the dead session's worktree before spawning a replacement. Record its path and accessibility, current branch, refs, exact commit SHAs, report path, and staged, unstaged, and untracked state as Foreman observations with probe locators. Reconcile any tracker or change-request effect separately. If the worktree is accessible, the replacement verifies the inventory there, resumes committed work through the recorded refs, and recovers verified uncommitted changes from the dead worktree into its fresh worktree without reimplementing them. If uncommitted worker-only state is inaccessible, or an external effect remains unreconciled, escalate; do not restart the assignment or run cleanup. The event wake remains unchanged after a safe replacement dispatch.

## PR-tracking hook

After step 7: `ao session claim-pr <worker-session-id> <pr-url>` so AO tracks CI and review state. AO nudges the worker about CI failures on its own; intervene only if the worker stalls.

## Merges

The worker's permission classifier denies `gh pr merge`; the foreman merges from its own session (`references/loop.md`, step 10). After a human merge, the human tells the foreman to verify and continue.

## Never run `ao session cleanup`

It reclaims the workspace of every terminated session in the project, and every orchestrator session shares one worktree path keyed by the branch rather than the session id. Once an earlier orchestrator session is terminated, cleanup deletes that shared directory — the foreman's own working directory — and the next turn fails with `invalid cwd: No such file or directory`. Tell the human that worker worktrees are pending reclamation and that only they can run `ao session cleanup`, while no orchestrator session is live.

## Rules and respawn

AO resolves orchestrator rules at spawn: after changing Foreman overrides or these references, respawn the orchestrator session. A changed orchestrator harness is picked up only by a new orchestrator session created from the AO app UI (`ao session restore` does not bring one back). Apply project config with `ao project set-config <project-id> --orchestrator-rules "…" --default-branch <foreman_default_branch> --orchestrator-agent claude-code` — set-config replaces the whole config, so pass every flag. The orchestrator rules text is one line: "Run `valcraft:foreman` for this project."

## Eval scenario coverage

All seven drill scenarios are expressible on this backend (`evals/scenarios.md`); they run against a live AO project, not inside the eval harness.
