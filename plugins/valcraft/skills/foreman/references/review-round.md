# After material findings

Read this after a PlanReview, CodeReview, or RetroReview report returns material findings. One full round is the default; two is the established cap.

1. Return the exact Review report path and R-IDs to the owning producer: Draft for plan findings, Forge for task-code findings, or Temper for retrospective findings.
2. After the producer reports resolutions, send the same logical Review role the resolution report path and R-IDs. Require it to inspect each resolving commit and locator, re-run that R-ID's reproduction, update the resolution column, open no new finding, and emit Review's unchanged report contract. This is a closure check, not a full round.
3. Run a second full round only when round one or the resolution shows one of the owner-established triggers:
   - three or more P1 findings in round one;
   - a resolution touches a file, module, or plan step no R-ID evidence cites, or changes the plan's approach — a resolution that edits an adjacent statement solely because the accepted fix would otherwise contradict it still fires this trigger;
   - the producer declines or defers a material R-ID;
   - a P1 concerns a trust boundary, security or permission check, data loss, or a migration;
   - the resolution adds a dependency, replaces a test, or changes CI configuration to pass.
4. Return second-round findings once more to the producer, then run a closure check. Escalate immediately when the producer declines a finding that round two upholds, or when a material finding remains open after closure. Foreman never decides it.
5. Without a second-round trigger, treat the closure-check table as the round's final state.

Record the branch and evidence in `state.md`. Cross-task ownership, external-completion origin, adjacency, or small size grants no exemption.
