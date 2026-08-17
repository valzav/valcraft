# Drill scenarios × backends

The seven scenarios come from the SelectiveCRM factory drill (2026-08-15). Each maps to
an eval in `evals.json` where the harness can express it, and to a backend-declared
`n/a` with its degradation where it cannot. Backend rows for `ao` cannot run inside the
eval harness — they need a live AO project — so they are covered by the `ao` reference
and by real runs, not by `evals.json`.

| Scenario                                   | `subagents`                                                                                                                  | `ao`                                                                                                                       |
| ------------------------------------------ | ---------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------- |
| Silent assignment (worker idle, no report) | `n/a` — an Agent call cannot silently not start; degradation: no report → `idle-without-report`, respawn once, then escalate | expressible; rule: confirm the pane shows processing before arming the wait (`ao.md`, `assign`)                            |
| Early finish (report before await armed)   | `n/a` — the completion notification is delivered regardless of timing                                                        | expressible; rule: read the report and `ao session ls` once before arming; checksum snapshot, not mtime (`ao.md`, `await`) |
| Blocked worker, resolvable from the task   | eval 4 `worker-question-settled-by-spec`                                                                                     | expressible; `answer: interactive` via `AO_SESSION_ID= ao send`                                                            |
| Blocked worker, needs escalation           | eval 5 `worker-blocked-escalates`                                                                                            | expressible; same rule                                                                                                     |
| Merge denied by permission classifier      | eval 8 `merge-denied-reports-command-and-waits`                                                                              | expressible; the worker's classifier denies (observed 2026-08-15); foreman merges itself, and its own denial is reported   |
| Partial mutation failure                   | eval 9 `partial-batch-failure-reconciles-before-retry` (`github` intake)                                                     | expressible; same intake rule                                                                                              |
| Two-round review cap                       | eval 3 `two-round-cap-escalates`                                                                                             | expressible; same loop rule                                                                                                |

Evals 1, 2, 6, 7, 10, and 11 cover foreman rules outside the drill list: missing project
block, verdict-only report rejection, release-branch merge waiting in `delegated` mode,
the cold-start planner dispatch, the closure check without a second review round, and the
temper dispatch at feature close.
