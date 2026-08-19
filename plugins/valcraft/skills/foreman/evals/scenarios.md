# Foreman scenarios × backends

## Native-subagent continuation

One portable `subagents` backend selects its primitive mapping from the active host.
These four scenarios discriminate the host-specific Codex continuation contract from
the pre-change event-only contract.

| Scenario | Codex | Claude Code | Eval |
| --- | --- | --- | --- |
| Foreground wait; no final while active | Keep the parent turn active after fresh dispatch and await the assigned worker in the foreground. | `n/a` — event wake does not foreground-wait. | 17 `codex-foreground-await-keeps-parent-active` |
| Timeout while worker remains active | Resolve the return through assigned-worker state and re-arm in the same turn. | `n/a` — the Agent event has no foreground timeout. | 18 `codex-timeout-active-worker-rearms-await` |
| Initial and respawn identity | Feature and `Q-NNN QT-XXX` dispatches are fresh, use `fork_turns: "none"`, and map unique physical handles to complete logical identities. | Initial and respawn Agent calls are fresh and keep the complete logical name. | 22 `codex-initial-and-respawn-identities-stay-fresh` |
| Blocked, question, dead, error, or non-live without terminal evidence | Route the first four through existing rules; never treat the last as success. | Route returned status through the same rules. | 23 `codex-terminal-routing-preserves-existing-rules` |

Evals 2, 4, 7, 11, and 12 also state both host continuations at existing dispatch and
respawn points instead of ending unconditionally after dispatch.

## Existing backend drills

The factory drill scenarios remain shared loop coverage. AO rows require a live AO
project and therefore live in its backend reference rather than `evals.json`.

| Scenario | `subagents` | `ao` |
| --- | --- | --- |
| Silent assignment | A dispatch or delivery failure before the worker acts follows the two-attempt rule. | Confirm processing before arming the wait. |
| Blocked, resolvable from task | Eval 4 `worker-question-settled-by-spec`. | `answer: interactive`. |
| Blocked, needs escalation | Eval 5 `worker-blocked-escalates`. | Same rule. |
| Merge denied | Eval 8 `merge-denied-reports-command-and-waits`. | Same loop rule. |
| Partial mutation failure | Eval 9 `partial-batch-failure-reconciles-before-retry`. | Same intake rule. |
| Review-round cap | Eval 3 `two-round-cap-escalates`. | Same loop rule. |

Evals 1, 6, 10, and 11 cover missing-key runtime defaults, an explicit release-branch
human wait, closure check, and feature-close temper dispatch. Evals 12, 13, 15, and 16
cover quick-task selection, close, validation, and physical-handle mapping.

## Runtime configuration

| Scenario | Expected distinction | Eval |
| --- | --- | --- |
| No Foreman keys | Default to native subagents and unattended, derive the default branch from agreeing live remote and hosting-service sources, and treat release as unconfigured without changing Cast approval. | 1 `missing-foreman-keys-use-runtime-defaults` |
| Default branch | Use an unambiguous live remote HEAD symref or host-reported default for the same repository; unavailable or disagreeing live sources stop. Cached `origin/HEAD` only corroborates. | 54 `default-branch-resolution-uses-authoritative-precedence` |
| No release branch | Ordinary default-branch merges use the normal approval row; fast-track and direct release writes are unavailable. | 55 `missing-release-branch-disables-release-only-flows` |
| Independent Cast approval | Missing Foreman approval defaults to unattended while missing Cast approval remains attended; Foreman relays and waits on every Cast gate raised during decompose. | 56 `decompose-relays-independent-cast-approval` |

## Default synchronization and exact final-head coverage

This scenario discriminates the task-start clean-checkout gate from the pre-change
contract.

| Scenario | Expected distinction | Eval |
| --- | --- | --- |
| Dirty shared checkout | Any staged, unstaged, or untracked state stops before fetch, switch, synchronization, or task-branch creation, even when attributable; dead-worker recovery remains separate. | 35 `dirty-shared-checkout-stops-before-synchronization` |

## External completion and causal finding routing

These seven scenarios cover Foreman's narrow record-and-close path and the routing of
findings whose causal owner is another task. Record and close does not replay normal
planning or a full review cycle; causal routing does not waive existing review gates.

| Scenario | Expected distinction | Eval |
| --- | --- | --- |
| Local external completion | Store attributed evidence per criterion beside the feature task; merge the evidence-and-tick PR only after fresh sufficiency review and the shared final-head gate. | 44 `local-external-completion-records-criterion-evidence` |
| Quick external completion | Store evidence beside the canonical `Q-NNN QT-XXX` task in its quick file and use the same local close gates. | 45 `quick-external-completion-keeps-evidence-in-quick-file` |
| GitHub external completion | Write attributed evidence and close through serialized task-issue batches without inventing a git target. | 46 `github-external-completion-uses-attributed-serialized-close` |
| Incomplete criterion | A weak or missing criterion makes the overall verdict insufficient and leaves the task open. | 47 `insufficient-external-completion-evidence-keeps-task-open` |
| Current-diff causation | A cross-task inconsistency caused by the current diff lands now under ordinary review gates. | 49 `current-diff-caused-cross-task-finding-lands-now` |
| Blocking versus unrelated owner | A blocking owner lands now; a verified durable unrelated-owner deferral lets the current exact-final-head/check gate proceed and reaches the future planner after restart. | 50 `blocking-owner-lands-now-unrelated-owner-survives-restart` |
| No review-round exemption | Small, adjacent, cross-task, and record-and-close remediation retains every existing second-round trigger. | 51 `cross-task-remediation-has-no-blanket-round-two-exemption` |
