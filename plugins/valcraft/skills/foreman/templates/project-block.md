# Foreman project block

Add this block to the project's root `AGENTS.md`, under "Project metadata" next to Cast's `project_tracker` declaration. It replaces any per-project orchestrator rules file: the loop lives in `valcraft:foreman`; the project states only what the skill cannot know.

```yaml
foreman_backend: subagents # subagents | ao — references/backends/<name>.md
foreman_approval_mode: gated # attended | gated | delegated — references/approval-modes.md
foreman_default_branch: main # task PRs target this branch
foreman_release_branch: main # writes here wait for the human in every mode; equal to default when there is no separate release branch
project_tracker: local # Cast's declaration, reused — local | github (with github_repository)
cast_approval: delegated # Cast's declaration — pair with the foreman mode (below)
```

Optional, only when the project needs it:

```yaml
foreman_clarification_assignees: # github intake only — who receives a needs-clarification question
  product: <login>
  default: <login>
```

Rules:

- One block per project. A missing block stops a foreman run.
- Pair `cast_approval` with `foreman_approval_mode`: `attended` ↔ `attended`; `gated` or `delegated` ↔ `delegated`. In `gated`, Cast's projection is a recorded mutation preview executed from its record — the same standing as the foreman's tracker batches — while `TBD` target activation and task removal wait in every mode. Cast reads its own declaration when the planner runs it during decompose; under `delegated` only Cast's residual stops reach the foreman as approval points. Missing means `attended`.
- The backend reference may require its own environment (`ao`: an AO project id and `set-config`; see the reference). That wiring lives in the operator's configuration, never in the block.
- `.foreman/` must be gitignored; `valcraft:cast` adds it at scaffold time.
