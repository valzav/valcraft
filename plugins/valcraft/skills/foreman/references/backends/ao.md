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

- `spawn`: `ao session new --project <project-id> --agent <harness> --name <role>-<F>-<T>` with no initial prompt. Session names are 20 characters or fewer; `reviewer-1-F004-T012` is exactly 20.
- `assign`: `ao send --session <id> --message "<envelope>"`. Then confirm the worker visibly started: `tmux capture-pane -p -t <id>` (no `-S`) shows the composer processing. An idle empty composer plus no report file means the send silently failed (the same trap as slash commands) — re-send.
- `await`: run this as a background Bash command (`run_in_background: true`) and end the turn; its exit re-invokes the foreman with the outcome. `R` is the worker's report path in the run directory.

  ```sh
  S=<worker-session-id>; R="<run dir>/<role>-<F>-<T>.md"
  B=$(date -r "$R" +%s 2>/dev/null || echo 0); seen=0
  while :; do
    [ "$(date -r "$R" +%s 2>/dev/null || echo 0)" -gt "$B" ] && { echo report; break; }
    st=$(ao session ls --project <project-id> --json | jq -r --arg s "$S" '.data[]|select(.id==$s)|.status')
    [ -z "$st" ] && { echo dead; break; }
    [ "$st" = blocked ] && { echo blocked; break; }
    [ "$st" = working ] && seen=1
    [ "$st" = idle ] && [ "$seen" = 1 ] && { echo idle-without-report; break; }
    sleep 30
  done
  ```

  Use `date -r`, not `stat -f %m`: on a machine with GNU coreutils `stat -f` means something else and the mtime read silently fails. Apply the await discipline in `README.md` before arming: read the report file and `ao session ls` once.

- `status`: `ao session ls --project <project-id> --json` for liveness; `tmux capture-pane -p -t <id>` for the prompt text — no `-S` for a liveness check, `-S -50` when hunting a prompt, `-S -200` only when reconstructing a failure. Never write to tmux.

## Answering a blocked worker

`AO_SESSION_ID= ao send --session <id> --message "<answer>"`. Inside the orchestrator session `AO_SESSION_ID` is set, and a plain `ao send` prefixes the message with `[from <session-id>]`, which a dialog does not accept. Then re-arm `await`.

## Workspaces and the run directory

Every AO worker has its own worktree, so a repository-relative `.foreman/` path differs per worker. The run directory is the absolute path inside the foreman's checkout; every envelope carries it, and workers write reports there by absolute path. Step 4's "copy the plan into your worktree" clause is live on this backend.

AO's own mailbox (`~/.ao-mail/<project-id>/<session-id>.md`) is not the wire format. If AO tooling needs it, a worker may mirror its report there; the run directory is the source.

## PR-tracking hook

After step 7: `ao session claim-pr <worker-session-id> <pr-url>` so AO tracks CI and review state. AO nudges the worker about CI failures on its own; intervene only if the worker stalls.

## Merges

The worker's permission classifier denies `gh pr merge` (observed live, 2026-08-15). The foreman merges from its own session. If the foreman's own classifier denies it, report the exact command to the human and wait; the human merges and tells the foreman to verify and continue.

## Never run `ao session cleanup`

It reclaims the workspace of every terminated session in the project, and every orchestrator session shares one worktree path keyed by the branch rather than the session id. Once an earlier orchestrator session is terminated, cleanup deletes that shared directory — the foreman's own working directory — and the next turn fails with `invalid cwd: No such file or directory`. Tell the human that worker worktrees are pending reclamation and that only they can run `ao session cleanup`, while no orchestrator session is live.

## Rules and respawn

AO resolves orchestrator rules at spawn: after changing the project block or these references, respawn the orchestrator session. A changed orchestrator harness is picked up only by a new orchestrator session created from the AO app UI (`ao session restore` does not bring one back). Apply project config with `ao project set-config <project-id> --orchestrator-rules "…" --default-branch <foreman_default_branch> --orchestrator-agent claude-code` — set-config replaces the whole config, so pass every flag. The orchestrator rules text is one line: "Run `valcraft:foreman` for this project."

## Eval scenario coverage

All seven scenarios in `evals/evals.json` are expressible on this backend.
