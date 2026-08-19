# Hygiene

## Context

- Hold only the active named state, exact target pointers, logical and physical worker
  identities, assigned report paths, backend returns, gate decisions, and recovery
  observations.
- Rebuild other facts from git, tracker state, producer reports, and the run directory.
- Read a producer report only after `report_available`. Pass its path to the next worker;
  never paste report, tracker, plan, diff, or fetched content into an assignment.
- Use explicit fields for hosted-tracker reads and the smallest backend status window.

## Naming

- Feature workers: `drafter-F004-T012`, `plan-reviewer-F004-T012`,
  `forge-F004-T012`, `code-reviewer-F004-T012`, `land-F004-T012`, and
  `review-evidence-F004-T012`.
- Quick workers preserve the qualified identity, for example
  `forge-Q007-QT001`. Retrospective workers are `temper-F004`,
  `retro-reviewer-F004`, and `land-F004-retro`.
- Branches: canonical task `feat/f004-t012-<slug>` or
  `feat/q007-qt001-<slug>`; retrospective `retro/f004-<slug>`. Agent
  Orchestrator physical branches are unique dispatch refs and never replace the
  canonical remote ref.
- Preserve every identity digit. Backend physical aliases remain separate and every
  dispatch gets a new row in `workers.md`.

## Workers

- One active worker per named state and target. Every initial dispatch and respawn is
  fresh. Preserve logical identity across recovery; never reuse the physical worker.
- A Review worker may handle its scoped closure check and second full round only when
  the backend keeps it active. A one-shot backend respawns it with the same logical
  identity and a new physical identity.
- Release terminal workers after their accepted report. Keep Land active while checks
  are pending. Never leave a worker active after its target completes.
- Workspace cleanup belongs to the backend reference.

## Review rounds

One full round is the default. Every material-finding remediation receives a closure
check. Run a second full round only on a trigger in [`review-round.md`](review-round.md).
Two full rounds is the owner-established cap; a third escalates with the open finding.

The owner-established two-attempt rule also covers assignments that fail to start,
reports that remain incomplete, backend dispatch recovery, and unresolved batch
delivery. Do not invent another retry or round count.

## Human overrides

Apply [`approval-modes.md`](approval-modes.md) for `no gates`, `confirm picks`, and
mid-run mode changes. A human override changes only its named coordination gate. It
does not grant another role's mutation authority or waive evidence.
