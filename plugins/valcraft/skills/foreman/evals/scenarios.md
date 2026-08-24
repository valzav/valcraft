# Foreman scenario coverage

Behavioral evals prove the state machine. The future coordination drift check only proves that declared contracts remain linked.

## Named states and producer routing

| Scenario | Eval |
| --- | --- |
| Resume exact Draft, Review, Forge, and PR evidence into PlanReview, Implementing, CodeReview, and Landing | 57 |
| Prepared Draft, Forge, and Temper heads resume the same producer before Review | 65 |
| Incomplete producer report is re-requested without Foreman reconstruction | 2 |
| Review closure check and established round cap remain intact | 3, 10 |
| Declared product question routes to the owner; unsafe permission prompt escalates | 4, 5 |
| Cross-task causal owner and durable future-owner routing remain intact | 49, 50, 51 |
| Feature confirmation routes Land, Temper, Review, Land | 64 |
| New PRD routes directly to Spec outside Foreman | 56 |

## Backend returns and recovery

| Scenario | Eval |
| --- | --- |
| Six backend returns remain separate from producer semantic status | 58 |
| Codex foreground active wait and timeout re-arm without user prompt | 17, 18 |
| Fresh native physical identities preserve complete logical identities | 22 |
| Dead, dispatch failure, blocked prompt, and missing terminal evidence remain distinct | 23 |
| Dirty shared checkout stops new-task synchronization; dead recovery remains separate | 35 |
| Late predecessor report is rejected after replacement | 59 |

Claude Code's event completion is covered by eval 7. Codex's foreground continuation is covered by eval 18. External-orchestrator polling and isolated branch behavior are covered by evals 63 and 62. These ids appear in the active-deviation registry.

## External orchestrators

| Scenario | Eval |
| --- | --- |
| Role-family physical aliases preserve canonical logical identity | 16 |
| Spawn command carries project, harness, physical alias, and exact physical branch | 62 |
| Stale or already-checked-out physical branch stops before spawn | 62 |
| Canonical task ref is revalidated and never force-pushed | 62 |
| Checksum and session polling maps attributed observations to backend returns before report access | 63 |
| No-git external completion uses a transport-only default-branch seed without inventing target git identity | 67 |
| Every active transport deviation names changed behavior and discriminating eval | 63 |

## Herdr

| Scenario | Eval |
| --- | --- |
| Land executes under shared session permission; a blocked agent state is `permission_blocked` and a credential failure stays a Land report | 72 |
| A successful `agent prompt` return is not delivery; a settled occupant without a working observation or report is `dispatch_error` | 73 |
| Every role resolves to its mapped harness; a missing mapped harness fails readiness instead of substituting the other | 74 |
| A dirty shared checkout stops the dispatch; release closes only the worker's own Herdr pane and changes no Git state | 75 |
| Seven Herdr observations map to the six returns; `unknown` proves nothing and `done` is not success | 76 |
| An unknown submission reconciles report, occupant, and state before anything is sent | 77 |
| A partial spawn resumes its recorded pane instead of splitting a second one | 78 |
| A released worker's late signal is an observation and its late report is rejected on attribution | 79 |
| The controller lease is an atomic hard-link claim, owner-bound on release, live only while the recorded pane still holds the recorded agent session, and reclaimed by claiming the next generation | 80 |
| Every dispatch records the skill's content hash, or says unavailable rather than substituting | 81 |
| Pending checks hold one Land assignment across foreground re-arms; `owner_decision_required` parks at AwaitOwner | 82 |
| Retrospective remediation uses a fresh physical worker and report path while editing the same gitignored `docs/.retro` file in place | 83 |

## Land boundary

| Scenario | Eval |
| --- | --- |
| Release target remains a human gate and Foreman performs no landing mutation | 6 |
| Unattended local and GitHub landing works under shared native or external execution permission | 60 |
| Prepared Land authority resumes through a fresh physical dispatch while Landing remains active | 58, 60 |
| Native subagents, AO, and Herdr each satisfy Land execution conformance | 68, 69, 72 |
| Future backends require a dedicated registered Land execution eval | 68, 69, 72 |
| Host permission prompts remain backend `permission_blocked`; Land owns execution failures | 8, 58 |
| Pending checks keep the same Land assignment active | 66 |
| External completion routes Land evidence to fresh Review and back to Land | 44, 45, 46, 47 |

External-completion evals characterize routing ownership: Land records and closes, Review judges sufficiency, and Foreman only validates and transitions.

## Runtime configuration and quick work

| Scenario | Eval |
| --- | --- |
| Missing keys select native subagents, unattended, live default branch, and no separate release branch | 1 |
| Live default-branch authorities and stop conditions | 54 |
| Missing release branch disables release-only flows without changing ordinary delivery | 55 |
| Quick selection, completion, validation, and qualified identities | 12, 13, 15, 16 |
| Herdr keeps a Review worker with material findings for its closure check; producers stay fresh; a dead kept pane falls back to a fresh physical worker | 85 |
| Herdr project session is the controller's own pane's session; `foreman.herdr.session` is a nullable assertion; no re-targeting | 86 |
| Herdr escalated permission gate stays under observation; an operator answer in the pane resolves it; await timeouts stay below the controller's command limit | 87 |
| AO keeps a Review worker for its closure check and refetches the canonical ref; a missing session falls back to a fresh one | 88 |
| AO escalated permission gate stays under the re-armed waiter; an operator answer in tmux resolves it | 89 |
| Herdr worker panes stack in one right column; the orchestrator keeps the full-height left column | 90 |
