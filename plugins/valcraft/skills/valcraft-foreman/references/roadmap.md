# Optional roadmap refresh

Read this reference only when `docs/roadmap.md` exists in the canonical project checkout. The file is an optional business view. Its absence changes no delivery behavior, and Foreman never creates it. Task selection, dependencies, approval gates, and completion still come only from delivery contracts and authoritative state.

## When to refresh

Record an automatic refresh event only when an accepted Land report confirms feature closure. Bind the event to the exact feature and Land report. Task start or completion, scope changes, blocker changes, and takeover do not trigger automatic refresh. The operator can invoke `valcraft-roadmap` manually for more frequent updates.

Wait until the Land worker has returned and any retained worker is idle. Refresh before dispatching Temper, with `Retrospective` as the saved delivery state. Roadmap decides whether the evidence changes the business view. A no-change result creates no delivery work. On resume, reconcile a recorded pending or active feature-close refresh or roadmap review; do not replay a handled closure or create a refresh merely because an existing feature is closed.

## Dispatch

1. Record the triggering event, exact evidence locators, current task and delivery state, and the state that delivery should resume. Enter `RoadmapRefresh` without changing the selected work or its pending gate.
2. Dispatch a fresh `roadmap-<identity>` worker through the configured backend with `valcraft-roadmap`, the canonical project checkout and `docs/roadmap.md` target, the integration ref and base SHA, accepted source revisions, the exact feature-close Land report, relevant evidence locators, and the previous pending Roadmap report when present. Pass the roadmap as an output target, never as delivery authority. The worker prepares its tracked update on an isolated documentation branch under Roadmap's publication contract; it may not alter the task branch, a reviewed head, or other producers' files.
3. Use the ordinary assignment envelope, worker identity, report path, backend await, and report-validation rules. The Herdr backend maps this documentation role to its configured `spec` entry and its reviewer to `spec_review`. Other backends use their normal role dispatch. An isolated backend must pass the canonical project output path explicitly; an absent copy inside a worker worktree is not proof that the project's roadmap is absent.
4. Accept the Roadmap report by the registry. Record its artifact disposition, exact candidate branch and commit, changed capabilities, evidence gaps, finding resolutions, Review target, and blockers. A prepared candidate does not update the published roadmap. When the report names a Review target, enter `RoadmapReview`. Otherwise apply `ResumeDelivery`. Mark the event handled only after a terminal refresh result or a recorded failed attempt; a stale predecessor report handles nothing.
5. Apply `ResumeDelivery`: revalidate and resume the saved delivery state, target, and pending gate. Report an unsuccessful refresh as a stale roadmap with its cause. A Roadmap `done` never closes a task or feature. An evidence gap in the roadmap never becomes a new delivery gate.

## `RoadmapReview`

Dispatch a fresh `roadmap-reviewer-<identity>` with `valcraft-review` in plan mode on the exact candidate path and full commit. RoadmapReview runs one full round, as [`review-round.md`](review-round.md#roadmapreview) defines. Material findings return the Review report path and R-IDs to a fresh `roadmap-<identity>` worker in `RoadmapRefresh`. That worker commits its resolutions on the same documentation branch, and the closure check covers the new commit.

A pass covering the latest candidate commit records the candidate as `reviewed — publication pending`. An R-ID the closure check leaves open records it as `review findings open`; a blocked or mismatched Review report records it as `review blocked`. Either candidate stays unpublished; name it with the Review report path and open R-IDs in the run-end report. Then mark the event handled and apply `ResumeDelivery`. No RoadmapReview result changes the delivery state or adds a delivery gate.

## Failure and recovery

An interrupted `RoadmapRefresh` or `RoadmapReview` resumes from its active assignment and recorded backend state, not from a second untracked dispatch. Apply the backend's identity and release rules before replacing a worker. Never leave a possibly live roadmap writer behind while advancing another worker.

After a terminal backend failure, release the exact worker and verify the task branch, reviewed head, and unrelated working-tree state are unchanged. When they are preserved, record the refresh as failed and resume delivery. Another automatic refresh requires a new confirmed feature closure; the operator can retry manually. Unreconciled writes or an unreleased worker use the existing recovery gate; optional reporting does not waive shared-checkout safety.

Permission prompts retain the backend's normal permission handling. Foreman grants no publication authority merely because a roadmap refresh was scheduled. A reviewed candidate awaiting the repository's documentation publication workflow is a successful refresh, not a refresh failure or a new delivery gate.
