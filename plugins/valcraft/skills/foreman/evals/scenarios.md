# Foreman scenario coverage

Behavioral evals prove the state machine. The future coordination drift check only
proves that declared contracts remain linked.

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

Claude Code's event completion is covered by eval 7. Codex's foreground continuation is
covered by eval 18. Agent Orchestrator's authorized poll and isolated branch behavior are
covered by evals 63 and 62. These ids appear in the active-deviation registry.

## Agent Orchestrator

| Scenario | Eval |
| --- | --- |
| Role-family physical aliases preserve canonical logical identity | 16 |
| Spawn command carries project, harness, physical alias, and exact physical branch | 62 |
| Stale or already-checked-out physical branch stops before spawn | 62 |
| Canonical task ref is revalidated and never force-pushed | 62 |
| AO checksum and session polling maps attributed observations to backend returns before report access | 63 |
| AO no-git external completion uses a transport-only default-branch seed without inventing target git identity | 67 |
| Every active transport deviation names changed behavior and discriminating eval | 63 |

## Land boundary

| Scenario | Eval |
| --- | --- |
| Release target remains a human gate and Foreman performs no landing mutation | 6 |
| Shared native or AO permission cannot substitute for per-dispatch Land capability | 60 |
| Land semantic operator action arrives under `report_available` and enters OperatorAction | 58, 60 |
| Pending checks keep the same Land assignment active | 66 |
| External completion routes Land evidence to fresh Review and back to Land | 44, 45, 46, 47 |

External-completion evals characterize routing ownership: Land records and closes,
Review judges sufficiency, and Foreman only validates and transitions.

## Runtime configuration and quick work

| Scenario | Eval |
| --- | --- |
| Missing keys select native subagents, unattended, live default branch, and no separate release branch | 1 |
| Live default-branch authorities and stop conditions | 54 |
| Missing release branch disables release-only flows without changing ordinary delivery | 55 |
| Quick selection, completion, validation, and qualified identities | 12, 13, 15, 16 |
