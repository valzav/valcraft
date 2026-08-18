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
| Silent assignment | A dispatch or delivery failure before the worker acts follows the two-attempt rule. | Confirm processing before arming the wait. |
| Early finish | Codex eval 20; Claude Code's event arrives regardless of timing. | Read status and the report once before arming; use the authorized checksum snapshot. |
| Blocked, resolvable from task | Eval 4 `worker-question-settled-by-spec`. | `answer: interactive`. |
| Blocked, needs escalation | Eval 5 `worker-blocked-escalates`. | Same rule. |
| Merge denied | Eval 8 `merge-denied-reports-command-and-waits`. | Same loop rule. |
| Partial mutation failure | Eval 9 `partial-batch-failure-reconciles-before-retry`. | Same intake rule. |
| Review-round cap | Eval 3 `two-round-cap-escalates`. | Same loop rule. |

Evals 1, 6, 10, and 11 cover the missing project block, release-branch human wait,
closure check, and feature-close temper dispatch. Evals 12–16 cover quick-task identity,
selection, validation, close, and physical-handle mapping.

## Attributed resume and artifact dates

These scenarios cover recovery state that is shared across backends. The backend
reference controls how Foreman inspects the workspace; the assignment and checkpoint
contracts control attribution and verification.

| Scenario | Expected distinction | Eval |
| --- | --- | --- |
| Instruction scope versus attestation | A quoted operator instruction authorizes only its named action; an operator attestation keeps its source and remains evidence. | 26 `assignment-context-preserves-provenance-and-scope` |
| Observation verification or discard | Every Foreman observation keeps its probe locator; a replacement verifies or discards it against the authoritative source. | 27 `replacement-verifies-or-discards-foreman-observations` |
| Recoverable worker death | Branch, exact commit, PR, report, working tree, and accessible workspace are inventoried before a fresh replacement resumes existing work. | 28 `dead-worker-recovers-branch-commit-pr-and-report` |
| Unsafe worker death | Unattributed dirty shared state, inaccessible worker-only changes, or unreconciled external effects escalate without restart. | 29 `unsafe-dead-worker-state-escalates` |
| Date precedence | Applicable repository policy wins, then an explicit operator date, then the artifact's actual creation date. | 30 `artifact-date-authority-precedence` |
| Midnight crossing | The run ID stays fixed while an artifact created after midnight resolves a new creation date. | 31 `midnight-run-keeps-id-and-resolves-new-artifact-date` |

Recovery preserves the active wake mapping: Codex remains foreground and Claude Code
remains event-driven on `subagents`; AO remains event-driven. These scenarios add no
polling schedule, interval, or retry rule.

## Default synchronization and exact final-head coverage

These ten scenarios cover the task-start synchronization gate and the merge gate. The
same final-head check classifier applies to normal task PRs, the pending record-and-close
flow, and retrospective PRs.

| Scenario | Expected distinction | Eval |
| --- | --- | --- |
| Four synchronization relations | Equal proceeds; clean origin-ahead fast-forwards; local-ahead waits without explicit push authority and reconciles with it; diverged stops. | 34 `default-branch-synchronization-classifies-four-relations` |
| Dirty shared checkout | Any staged, unstaged, or untracked state stops before fetch, switch, synchronization, or task-branch creation, even when attributable; dead-worker recovery remains separate. | 35 `dirty-shared-checkout-stops-before-synchronization` |
| Exact local tick exception | Only the selected task's exact unchecked-to-checked transition bypasses another review; adjacent text does not. | 36 `exact-local-task-tick-is-the-only-review-bypass` |
| Other final-head deltas | Documentation, rename, generated-file, and merge deltas each require scoped review. | 37 `all-other-final-head-deltas-require-scoped-review` |
| Passing versus pending/failing | Applicable required checks must pass on the exact final SHA; running or failing waits. | 38 `final-head-required-checks-pass-or-wait` |
| Required run absent | A configured or required check that did not trigger is `missing-required`, not `none-applicable`. | 39 `required-check-that-did-not-trigger-is-missing-required` |
| PR and external applicability | A PR-introduced workflow and an external required check count even when the default branch has no workflow. | 40 `introduced-workflow-and-external-requirement-determine-applicability` |
| Older-head result | A passing result on an older SHA cannot authorize the final SHA. | 41 `older-head-check-result-cannot-authorize-final-head` |
| No applicable checks | After every source is queried and none applies, record `none-applicable` and use the normal merge-approval row. | 42 `none-applicable-uses-normal-merge-approval-row` |
| Applicability source unavailable | An unavailable repository-rule, external-required-check, or workflow source stops before classification. | 43 `unavailable-applicability-source-stops-classification` |
