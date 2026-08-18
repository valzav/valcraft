# After a review round

Read this when a review round returns **material findings** — deliver steps 5 and 9, decompose step 4. One review round is the default; a second full round is the exception; two is the cap (`references/hygiene.md`, "Rounds and escalation").

A round-one verdict of **pass** needs nothing more: proceed. **blocked** is not a round — apply the report check in `references/contracts.md`. On **material findings**, after the worker's resolution report:

1. **Closure check.** Send the same reviewer the worker's resolution report path and the R-IDs it claims resolved: "For each listed R-ID, inspect the named resolving commit and its diff at the repository-relative locator first. If the report's claim contradicts the actual diff, keep the finding open. Then re-run the reproduction from that R-ID's evidence cell against the remediated artifact and record the new output in its resolution column (`valcraft:review` rule 6). Review nothing else. Re-emit the review report block with the updated resolution column, then the `Status:` line." This is a closure check, not a review round: it opens no new findings, and a finding whose claim contradicts the diff or whose re-run still fires stays open.
2. **Second full round — only when a trigger fires.** Send the reviewer the updated artifact for a complete `valcraft:review` pass when round one or the resolution shows any of:
   - three or more P1 findings in round one (authority: the owner's rule for this loop, 2026-08-16);
   - the resolution reached beyond the findings — a resolution commit or plan edit touches a file, module, or plan step that no round-one R-ID's evidence cell cites, or the plan's approach changed;
   - the worker declined or deferred a material R-ID (resolution other than fixed) — the reviewer holds the evidence and adjudicates, not the foreman;
   - a round-one P1 on a trust boundary, a security or permission check, data loss, or a migration;
   - the resolution added a dependency, replaced (not added) a test, or changed CI configuration to go green.

   Findings from round two go to the worker once more, followed by a closure check — except a finding the worker declined and round two upheld, which is a disagreement the human settles: escalate at once. A material finding still open after the closure check is also an escalation; the foreman never decides a material finding itself.

3. **Otherwise** the closure check's table is the round's final state: proceed to the step's summary and proceed/wait test.

These branches apply unchanged to remediation selected by cross-task causal routing or
record and close. Small size, adjacency, another task's ownership, or the exceptional
completion path is never a blanket exemption from a closure check or a listed
second-full-round trigger.

Record which branch applied and why in the summary and in `state.md`.
