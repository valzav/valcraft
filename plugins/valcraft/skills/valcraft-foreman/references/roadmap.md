# Optional roadmap refresh

Read this reference only when `docs/roadmap.md` exists in the canonical project checkout. The file is an optional business view. Its absence changes no delivery behavior, and Foreman never creates it. Task selection, dependencies, approval gates, and completion still come only from delivery contracts and authoritative state.

## When to refresh

Record a refresh event when accepted scope changes, a task starts, an established blocker appears or clears, or Land confirms task or feature completion. Include a release or business-outcome observation only when the operator or an accepted producer report supplies its exact source. On takeover or resume, refresh when authoritative observations differ from the last recorded refresh event or no refresh observation exists. Do not derive a progress event from an unaccepted plan, review finding, or roadmap prose.

Wait until the active worker has returned and any retained worker is idle. Dispatch before the next delivery worker or before presenting the already-required human gate or completion. Combine pending events in that assignment; their distinct source locators remain recorded. Roadmap decides whether they change the business view. A no-change result creates no delivery work.

## Dispatch

1. Record the triggering event, exact evidence locators, current task and delivery state, and the state that delivery should resume. Enter `RoadmapRefresh` without changing the selected work or its pending gate.
2. Dispatch a fresh `roadmap-<identity>` worker through the configured backend with `valcraft-roadmap`, the canonical project checkout and `docs/roadmap.md` target, the integration ref and base SHA, accepted source revisions, relevant report paths, the previous pending Roadmap report when present, and attributed task-start or blocker observations. Pass the roadmap as an output target, never as delivery authority. The worker prepares its tracked update on an isolated documentation branch under Roadmap's publication contract; it may not alter the task branch, a reviewed head, or other producers' files.
3. Use the ordinary assignment envelope, worker identity, report path, backend await, and report-validation rules. The Herdr backend maps this documentation role to its configured `spec` entry. Other backends use their normal role dispatch. An isolated backend must pass the canonical project output path explicitly; an absent copy inside a worker worktree is not proof that the project's roadmap is absent.
4. Accept the Roadmap report by the registry. Record its artifact disposition, exact candidate branch and commit, changed capabilities, evidence gaps, and blockers. Keep publication pending visible; a prepared candidate does not update the published roadmap. Mark the event handled only after a terminal refresh result or a recorded failed attempt; a stale predecessor report handles nothing.
5. Apply `ResumeDelivery`: revalidate and resume the saved delivery state, target, and pending gate. Report an unsuccessful refresh as a stale roadmap with its cause. A Roadmap `done` never closes a task or feature. An evidence gap in the roadmap never becomes a new delivery gate.

## Failure and recovery

An interrupted `RoadmapRefresh` resumes from its active assignment and recorded backend state, not from a second untracked dispatch. Apply the backend's identity and release rules before replacing a worker. Never leave a possibly live roadmap writer behind while advancing another worker.

After a terminal backend failure, release the exact worker and verify the task branch, reviewed head, and unrelated working-tree state are unchanged. When they are preserved, record the refresh as failed and resume delivery. Re-attempt only for a new source event or an explicit refresh request. Unreconciled writes or an unreleased worker use the existing recovery gate; optional reporting does not waive shared-checkout safety.

Permission prompts retain the backend's normal permission handling. Foreman grants no publication authority merely because a roadmap refresh was scheduled. A local candidate awaiting the repository's documentation publication workflow is a successful preparation, not a refresh failure or a new delivery gate.
