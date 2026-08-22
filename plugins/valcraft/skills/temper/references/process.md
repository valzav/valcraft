# Temper analysis, synthesis, and routing

Read this reference after corpus preflight and before examining evidence. It owns the shared disciplines, both mode workflows, and lesson routing.

## Shared disciplines

1. **Inventory before conclusions.** List every unit of work in the corpus with its examination depth before extracting any lesson, and close the report with an explicit statement of what was not examined.
2. **Reproduce before reporting.** An A- or B-grade candidate requires the complete verified incident record; an unverified incident supports only C-grade guidance.
3. **Attribute each escape to a stage.** Name the gate that should have caught it (Draft, implementation, plan Review, or code Review), record that gate's execution as **ran**, **skipped**, or **unknown**, and — when a later gate caught the incident — name which one. Assign ran or skipped only from positive evidence; the absence of a durable review record means unknown, not skipped. When the evidence permits the distinction, answer missing-gate versus failed-gate first — the two demand different fixes (add the gate versus sharpen its check) — and let the corpus, not a prior, say which dominated.
4. **Tensions versus contradictions are reported, not silently resolved.** Two candidates that pull in different directions but can both be followed are a tension: report the pair and the boundary between their domains. Two that cannot both be true are a contradiction: resolve it by evidence or report it unresolved.
5. **No thresholds from the corpus.** Report metrics as evidence; never turn a count, rate, or proportion from the corpus into a gate, target, or recommended limit. No count of lessons is a target in either direction — an empty report over a clean corpus is a valid result.

## Analyze mode

1. **Preflight the corpus** per `../SKILL.md`, and name the evidence sources available and absent for this corpus.
2. **Inventory.** One row per unit: what it was, its review history (rounds, finding IDs, clean passes), and the examination depth this run gives it.
3. **Examine.** For each unit examined deeply: what escaped its gates, what a gate caught, what the implementer self-caught, and what the evidence shows versus what the record claims. Write the strongest incidents up as case studies with verbatim citations and full incident records.
4. **Extract lesson candidates.** Each candidate gets a stable ID (`L-001`, `L-002`, …), a one-line rule statement, its incident records, its grade, and its stage attribution. Separate prompt-line candidates from structural findings — an observation about the process's design that no single rule fixes is reported as a structural finding, not forced into rule shape.
5. **Route each candidate** per the routing section below and write the report.

## Synthesize mode

The input is two or more analyze reports. Read only the reports; re-open an underlying corpus only to settle a contradiction between reports.

1. **Collapse derivative evidence first.** Before grading, identify citations and reports that derive from the same root incident, so one event cannot masquerade as independent corroboration.
2. **Merge candidates into themes.** Each merged theme gets its own L-ID local to the synthesis report and cites every contributing analyze report and source L-ID.
3. **Re-grade.** Corroboration by distinct root incidents across reports upgrades a B to an A; derivative corroboration never does. A candidate contradicted by another report's evidence is not averaged — investigate which evidence holds and record the resolution.
4. **Report tensions and contradictions** as a distinct section, per shared discipline 4.
5. **Route the merged themes** through the same tiers, and re-check prior promotions: a standing rule that no surviving evidence supports is proposed for retirement from `AGENTS.md`. Write the synthesis report.
6. **Escalate corroborated proposals to the operator.** A routed proposal meets the escalation test when its theme is A-grade **and** its root incidents come from two or more distinct analyze reports; a single report's evidence, however strong, stays in the report. Attended — the harness offers a structured question tool or the operator is live — present every proposal that meets the test as one multi-select menu: each item names the rule or change, its target (`AGENTS.md` standing rule, another project file, a user-owned artifact, an upstream candidate), and its grade with the contributing reports. Record the operator's choice in the report's Operator selection section; for each accepted item name the application step (`valcraft:hone` against a prompt artifact, a quick task for a project file, the upstream suggestion for a plugin skill). Temper applies nothing itself. Unattended, or under a Foreman dispatch with no live operator, list the same items as `offered, awaiting selection` and end `Status: done`; never block on the menu and never accept on the operator's behalf.

## Routing

Every candidate gets exactly one primary tier. Name a secondary action when another owner has a distinct response to the same lesson.

1. **Project-owned — promotion to standing rules.** An A- or B-grade candidate that passes the promotion gate is proposed as one line in a `Standing rules` section of the project's root `AGENTS.md`, citing its `<report>, L-NNN`. The gate is a deletion test: promote only if a future run in this project would plausibly repeat the incident without the rule. Rules the contract already states, one-off incidents, and C-grade candidates fail the gate and stay in the report. Project-owned also covers proposals to specs, ADRs, and plan conventions when the lesson is a contract fix rather than a rule.
2. **User-owned.** A candidate that generalizes beyond this project routes to the user's own prompt artifacts — their global instructions, their own skills — with `valcraft:hone` named as the application step. Propose the change; do not apply it.
3. **Upstream candidates.** A candidate that would improve a plugin skill itself, reported in a dedicated section addressed to the plugin's maintainer. Admission requires an attribution argument, not just severity: the evidence must locate the cause in the skill's own instruction text. An A- or B-grade upstream candidate requires direct run evidence — a transcript or equivalent record — that identifies the invoked skill revision or instruction and shows the agent followed it as written and still failed, ruling out the user's code, project contract, configuration, and harness. Git-only evidence supports at most a C-grade attribution hypothesis — never an A/B upstream candidate and never a submission suggestion. A candidate whose incident traces to the user's own side routes to tier 1 or 2 instead, however severe; portability is the tiebreak question — would the same incident recur in a different project on a different harness? When an admitted candidate is A-grade and corroborated across multiple analyze reports, suggest that the user submit it upstream as an issue or pull request against the plugin's repository — attended, offer it; unattended, record the suggestion in the report. Temper never submits an upstream issue or change, and it writes no git or external state at all. When an upstream correction and a project safeguard are both necessary, upstream is the primary tier and the safeguard is a secondary project-owned action.

Retirement of a promoted rule happens in `AGENTS.md`, proposed by a later run.
