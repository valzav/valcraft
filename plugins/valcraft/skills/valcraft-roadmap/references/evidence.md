# Roadmap evidence

The roadmap joins accepted product direction to verified progress. Neither an old roadmap nor a task count proves current capability state.

## Source authority

Resolve the project's existing authority order. Use accepted requirements and decisions for goals, capability scope, dependencies, and priority. Use the configured tracker for task state: in local mode, feature `tasks.md` checkboxes; in GitHub mode, current mapped issue state. Quick tasks retain their local file authority in either mode. Read only the existing tracker configuration needed to resolve this; Roadmap never invokes Tune or changes configuration as a side effect of reporting. When the source cannot be resolved or read, mark the affected capability unverified and name the gap.

Treat git, tracker, deployment, and outcome evidence as separate observations. A commit proves a change exists at that revision. A merged feature or `status: complete` proves only the closure its contract defines. Release evidence proves availability only for its named environment and version. A successful pilot or measured outcome proves only the named population and observation period. Keep these scopes visible when they matter to the reader.

Reports and owner attestations are attributed evidence. A report tied to an earlier head remains historical evidence, not a fresh verification of changed behavior. A Foreman assignment may supply the current task-start or blocker observation with its source and scope; it supplies no independent acceptance verdict.

## Capability state

Use plain-language states suited to the project. Separate implementation, availability, and achieved business outcomes whenever conflating them would mislead. Do not impose a lifecycle enum on existing feature contracts.

- Mark a capability planned when accepted scope exists but delivery is not established.
- Mark work underway only from current work or authoritative in-progress evidence, not from a spec's existence or its position in a list.
- Name a blocker only when a source establishes that it prevents this capability. A failed quality experiment is not a blocker for another workstream without a governing dependency.
- Mark implementation complete only when the capability's full applicable scope is covered by completion evidence. Follow transferred requirements and named successor work before deciding.
- Claim available or outcome achieved only with evidence for that claim. Otherwise say implementation complete with availability unverified, or the project-specific equivalent.

When new evidence contradicts a previous state, update the state and record the basis. When a source merely becomes inaccessible, retain the prior result as a dated observation and mark current verification unavailable. Never silently promote uncertainty to success or turn lack of access into a proven regression.

Task completion percentages do not measure business progress. Do not invent dates, targets, budgets, or timeouts. Carry an existing numerical goal only with its authoritative source and conditions. An owner-approved decision to stop pursuing a target does not mean the target was met.

## Coverage and freshness

Keep a source mapping for each capability in the roadmap's evidence section. A mapping may name several specs, criteria, decisions, release records, or outcome observations. Use stable source identifiers and repository-relative links for local artifacts. Do not expose implementation details in the business table merely to make the mapping convenient.

For each refresh, inspect accepted scope changes and the mapped evidence needed to settle current states. Record the checked date, described repository revision or revisions, tracker observation when applicable, external evidence checked, and sources not checked. A changed HEAD alone does not prove the roadmap stale or fresh; external task or deployment state can change without any commit.

Use the project's canonical branch for accepted scope and delivered implementation. Attribute work on another branch as work in progress at its exact revision. If a Foreman worker checkout differs from the project checkout, read the assigned source revisions rather than treating the worker's older checkout as current. Do not label all capabilities freshly verified when only an event's affected sources were checked.

Retain later accepted scope even when it has no spec yet. Record an ambiguous or missing mapping as a gap. Exclude unaccepted ideas from the accepted course; describe them separately in the report only when relevant to the request.
