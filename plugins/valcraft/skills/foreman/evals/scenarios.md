# Foreman scenarios × backends

## Native-subagent continuation

One portable `subagents` backend selects its primitive mapping from the active host.
These nine scenarios cover the host-specific continuation contract added for Codex while
preserving Claude Code's event-driven contract.

| Scenario | Codex | Claude Code | Eval |
| --- | --- | --- | --- |
| Foreground wait; no final while active | Keep the parent turn active after fresh dispatch and await the assigned worker in the foreground. | `n/a` — event wake does not foreground-wait. | 17 `codex-foreground-await-keeps-parent-active` |
| Timeout while worker remains active | Resolve the return through assigned-worker state and re-arm in the same turn. | `n/a` — the Agent event has no foreground timeout. | 18 `codex-timeout-active-worker-rearms-await` |
| Completion with `trigger_turn:false` | Consume it in the active turn, validate the report, and advance. | `n/a` — the completion event re-invokes the parent. | 19 `codex-trigger-turn-false-completion-advances` |
| Completion before first await | Consume the available completion message before waiting; live-status absence alone is not success. | The event is delivered regardless of timing. | 20 `codex-early-completion-before-first-await` |
| Legitimate human gate | After processing terminal worker output, a named approval or escalation gate may end the turn in either approval mode. | Same rule. | 21 `codex-human-gate-may-end-turn` |
| Initial and respawn identity | Feature and `Q-NNN QT-XXX` dispatches are fresh, use `fork_turns: "none"`, and map unique physical handles to complete logical identities. | Initial and respawn Agent calls are fresh and keep the complete logical name. | 22 `codex-initial-and-respawn-identities-stay-fresh` |
| Blocked, question, dead, error, or non-live without terminal evidence | Route the first four through existing rules; never treat the last as success. | Route returned status through the same rules. | 23 `codex-terminal-routing-preserves-existing-rules` |
| Event notification and re-invocation | `n/a` — Codex consumes completion in the active turn. | Establish the Agent completion notification before ending; the host re-invokes Foreman. | 24 `claude-code-event-continuation-preserved` |
| No added polling policy | No external orchestrator, scheduled/report polling, interval, retry cap, or working-status requirement. | No scheduled polling; await the native event. | 25 `native-subagents-add-no-polling-policy` |

Evals 2, 4, 7, 11, and 12 also state both host continuations at existing dispatch and
respawn points instead of ending unconditionally after dispatch.

## Existing backend drills

The factory drill scenarios remain shared loop coverage. AO rows require a live AO
project and therefore live in its backend reference rather than `evals.json`.

| Scenario | `subagents` | `ao` |
| --- | --- | --- |
| Silent assignment | A dispatch error or unusable terminal return follows the two-attempt rule. | Confirm processing before arming the wait. |
| Early finish | Codex eval 20; Claude Code's event arrives regardless of timing. | Read status and the report once before arming; use the authorized checksum snapshot. |
| Blocked, resolvable from task | Eval 4 `worker-question-settled-by-spec`. | `answer: interactive`. |
| Blocked, needs escalation | Eval 5 `worker-blocked-escalates`. | Same rule. |
| Merge denied | Eval 8 `merge-denied-reports-command-and-waits`. | Same loop rule. |
| Partial mutation failure | Eval 9 `partial-batch-failure-reconciles-before-retry`. | Same intake rule. |
| Review-round cap | Eval 3 `two-round-cap-escalates`. | Same loop rule. |

Evals 1, 6, 10, and 11 cover the missing project block, release-branch human wait,
closure check, and feature-close temper dispatch. Evals 12–16 cover quick-task identity,
selection, validation, close, and physical-handle mapping.
