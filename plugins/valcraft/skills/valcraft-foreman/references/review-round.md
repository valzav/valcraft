# After material findings

Read this after a SpecReview, PlanReview, CodeReview, RetroReview, or RoadmapReview report returns material findings. One full round is the default; two is the established cap for SpecReview, PlanReview, and CodeReview. RetroReview and RoadmapReview run one full round, as [RetroReview](#retroreview) and [RoadmapReview](#roadmapreview) define.

1. Return the exact Review report path and R-IDs to the owning producer: Spec for feature-contract or quick-file findings, Draft for plan findings, Forge for task-code findings, Temper for retrospective findings, or Roadmap for roadmap-candidate findings.
2. After the producer reports resolutions, unless step 3 sends them straight to a second full round, send the same logical Review role the resolution report path and R-IDs. Require it to inspect each resolving commit and locator, re-run that R-ID's reproduction, update the resolution column, open no new finding, and emit Review's unchanged report contract. This is a closure check, not a full round.
3. Run a second full round only when round one or the resolution shows one of the owner-established triggers:
   - three or more P1 findings in round one;
   - a resolution touches a file, module, or plan step no R-ID evidence cites, or changes the plan's approach, including an adjacent statement edited only to stay consistent with the accepted fix;
   - the producer declines or defers a material R-ID;
   - a P1 concerns a trust boundary, security or permission check, data loss, or a migration;
   - the resolution adds a dependency, replaces a test, or changes CI configuration to pass.

   When round one's report or the producer's resolution report already shows a trigger, skip the closure check and send the resolution straight to the second full round. Its envelope names the round-one R-IDs and requires step 2's inspection of each before the full review. A trigger that only the closure check's inspection reveals runs the second full round after that closure check.
4. Return second-round findings once more to the producer, then run a closure check. Escalate immediately when the producer declines a finding that round two upholds, or when a material finding remains open after closure. Foreman never decides it.
5. Without a second-round trigger, treat the closure-check table as the round's final state.

Record the branch and evidence in `state.md`. Cross-task ownership, external-completion origin, adjacency, or small size grants no exemption.

## RetroReview

RetroReview runs one full round. Step 3's triggers and step 4 do not apply to it.

1. Return its findings to Temper once, then run the closure check, as steps 1 and 2 define.
2. When the closure check leaves no material R-ID open, the round is complete.
3. When a material R-ID remains open, including one Temper declined or deferred, do not escalate and do not run another round. Dispatch Temper once more with the RetroReview report path and the open R-IDs, and require it to record them in the report's `Open review findings` section. That record receives no review.
4. Enter `Complete` after Temper records them. Name each open R-ID and the report path in the run-end report, so the person who reads the report can address them after the run.

## RoadmapReview

RoadmapReview runs one full round. Step 3's triggers and step 4 do not apply to it.

1. Return its findings to Roadmap once, then run the closure check, as steps 1 and 2 define. The closure check's covered target is Roadmap's new candidate commit.
2. When the closure check leaves no material R-ID open, the candidate is reviewed and publication pending.
3. When a material R-ID remains open, including one Roadmap declined, do not escalate, run another round, or dispatch Roadmap again. The candidate stays unpublished. Record each open R-ID with the Review report path, name them in the run-end report, and apply `ResumeDelivery`.
