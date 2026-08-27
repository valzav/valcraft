# Run directory

Create one gitignored directory per Foreman run:

```text
.valcraft/foreman/<run-id>/
├── state.md
├── workers.md
├── specifier-F004-d000.md
├── spec-reviewer-F004-d000.md
├── drafter-F004-T012-d000.md
├── plan-reviewer-F004-T012-d000.md
├── forge-F004-T012-d000.md
├── code-reviewer-F004-T012-d000.md
├── land-F004-T012-d000.md
├── review-evidence-F004-T012-d000.md
├── specifier-Q007-d000.md
├── spec-reviewer-Q007-d000.md
├── forge-Q007-QT001-d000.md
├── temper-F004-d000.md
└── retro-reviewer-F004-d000.md
```

`<run-id>` is either the next repository-valid dated run id or an operator-provided name matching `^[A-Za-z0-9][A-Za-z0-9._-]*$` other than `.` or `..`. Resolve the final path inside `.valcraft/foreman/`. A run id never supplies an artifact date.

## `workers.md`

Append one row for every physical dispatch:

`assignment id | named state | target | logical worker | backend | host/harness | physical identity | physical branch or none | assigned report path | predecessor SHA or none | backend return | worker state`

Preserve prior rows and report paths after respawn. Use the dispatch discriminator in the report filename so a predecessor cannot append to its replacement's active path. A Codex identity records task name and agent id. A Cursor identity records the Task agent id. An external-orchestrator identity records the dispatch ordinal plus the exact physical fields its backend reference declares. A backend whose workers share the orchestrator's checkout records `none` for the physical branch. Record terminal evidence before marking a row done. For backend returns, `workers.md` is a derived index of `state.md`: on disagreement, rebuild the row from the latest `state.md` checkpoint. Workers write only their assigned report path.

## `state.md`

Append checkpoints with:

- a wall-clock timestamp on every checkpoint heading (`## CP-NNN 2026-08-21T17:19:05-04:00 <title>`), backend return, and dispatch, so run timing does not depend on report-file mtimes;
- active named state, target kind, canonical task identity, tracker reference, and authoritative contract paths;
- takeover disposition: exact checkpoint resume or confirmed takeover; for takeover record the candidate set, evidence and conflicts, operator response, inferred state, next action, and exact attributed dirty paths;
- active assignment id, logical and physical worker identities, physical branch, attributed report path, and predecessor target;
- the plugin revision of each dispatched skill at every dispatch, as that skill's `version` content hash from the plugin's `skills/index.json` together with the plugin manifest's release version string. The content hash is the canonical revision because it distinguishes snapshots that share a release version; the release version string is corroborating metadata and never substitutes for it. Record the revision as unavailable when `skills/index.json` cannot be read, rather than falling back to the base directory or the release version;
- every backend return, its source, time, and terminal or nonterminal disposition;
- accepted producer report path, terminal status, routing code or structured verdict, exact artifact or PR identity, and registry transition;
- adopted pre-run report path, content hash, producer contract, exact target, predecessor plan or artifact, covered head or hash, validation result, and operator attribution, without an assignment, backend return, or worker row;
- canonical and physical branch refs, exact local and remote SHAs, workspace seed SHA and kind, and synchronization classification;
- workflow target git identity, preserving `none` independently from an external-orchestrator transport-only workspace seed;
- Review-covered SHA, current head, and producer-reported delta or check route;
- approval decision and exact target-bound authority source;
- intermediate tracker state, held questions, deferred-finding owner and durable locator, and feature confirmation;
- recovery probes, observations, accessibility, dispositions, replacement identity, and every rejected stale return or report; and
- each dated artifact's resolved date and authority.

This checkpoint is not an authority. Re-read every referenced git, tracker, report, and backend fact before transition. Preserve prior checkpoints so resume can explain the state that produced each decision.

The run directory is the audit and resume surface. Nothing in it is committed or pasted into a producer artifact.

Ignore runtime state outside `.valcraft/foreman/`. Never migrate it into the current runtime contract.
