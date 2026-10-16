# Hygiene

## Context

- Hold only the active named state, exact target pointers, logical and physical worker identities, assigned report paths, backend returns, gate decisions, and recovery observations.
- Rebuild other facts from git, tracker state, producer reports, and the run directory.
- Read an active producer report only after `report_available`, and read only the parts [`contracts.md`](contracts.md#coordinator-reads) names: the heading index, the terminal status line, and the listed sections. Never load a report body. Pass report paths to workers; never paste report, tracker, plan, diff, or fetched content into an assignment.
- On resume or after a context reset, read the latest `state.md` checkpoint and the active assignment's `workers.md` rows. Read an earlier checkpoint only to explain one recorded decision, never the whole log.
- Use explicit fields for hosted-tracker reads and the smallest backend status window.

## Naming

- A new contract's specifier is `specifier-new-<source-slug>` until Spec reports the identity. Feature workers include `specifier-F004`, `spec-reviewer-F004`, `drafter-F004-T012`, `plan-reviewer-F004-T012`, `forge-F004-T012`, `code-reviewer-F004-T012`, `land-F004-T012`, and `review-evidence-F004-T012`.
- Quick workers preserve the qualified identity, for example `specifier-Q007`, `spec-reviewer-Q007`, and `forge-Q007-QT001`. Retrospective workers are `temper-F004` and `retro-reviewer-F004`. Roadmap workers are `roadmap-F004` and `roadmap-reviewer-F004`.
- Branches follow [`contracts.md`](contracts.md#canonical-branches); a retrospective has no branch, its report lives in the gitignored `docs/.retro/`. External-orchestrator physical branches are unique dispatch refs and never replace the canonical remote ref.
- Preserve every identity digit. Backend physical aliases remain separate and every dispatch gets a new row in `workers.md`.

## Workers

- One active worker per named state and target. Every initial dispatch and respawn is fresh. Preserve logical identity across recovery; never reuse the physical worker.
- A Review worker may handle its scoped closure check and second full round only when the backend keeps it active. A one-shot backend respawns it with the same logical identity and a new physical identity.
- A producer is always fresh: remediation, a re-dispatch under its grant, and a prepared continuation each get a new physical worker.
- Release terminal workers after their accepted report. Keep Land active while checks are pending. Never leave a worker active after its target completes.
- Workspace cleanup belongs to the backend reference.

## Review rounds

One full round is the default. Every material-finding remediation receives a closure check, or a second full round that performs that check's inspection when a trigger is already known. Run a second full round only on a trigger in [`review-round.md`](review-round.md). Two full rounds is the owner-established cap; a third escalates with the open finding. RetroReview runs one full round, and Temper records a finding its closure check leaves open in the report instead of escalating it. RoadmapReview runs one full round, and a finding its closure check leaves open keeps the candidate unpublished instead of escalating it.

The owner-established two-attempt rule also covers assignments that fail to start, reports that remain incomplete, backend dispatch recovery, and unresolved batch delivery. External failures follow their own owner-established schedule in [`contracts.md`](contracts.md#external-failures) instead. Do not invent another retry or round count.

## Human overrides

Apply [`approval-modes.md`](approval-modes.md) for `no gates`, `confirm picks`, and mid-run mode changes. A human override changes only its named coordination gate. It does not grant another role's mutation authority or waive evidence.
