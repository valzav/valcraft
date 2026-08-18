# Foreman project block

Add this block to the project's root `AGENTS.md`, under "Project metadata" next to Cast's `project_tracker` declaration. It replaces any per-project orchestrator rules file: the loop lives in `valcraft:foreman`; the project states only what the skill cannot know.

```yaml
foreman_backend: subagents # subagents | ao — references/backends/<name>.md
foreman_approval_mode: unattended # attended | unattended — references/approval-modes.md, "Choosing a mode"
foreman_default_branch: main # task PRs target this branch
foreman_release_branch: main # writes here wait for the human in every mode; equal to default when there is no separate release branch
project_tracker: local # Cast's declaration, reused — local | github (with github_repository)
cast_approval: unattended # Cast's declaration — the same word as the foreman mode (below)
```

Optional, only when the project needs it:

```yaml
foreman_clarification_assignees: # github intake only — who receives a needs-clarification question
  product: <login>
  default: <login>
```

Rules:

- One block per project. A missing block stops a foreman run.
- `cast_approval` takes the same word as `foreman_approval_mode`. In `unattended`, Cast's projection is a recorded mutation preview executed from its record — the same standing as the foreman's tracker batches — while `TBD` target activation waits in every mode. Cast reads its own declaration when the planner runs it during decompose; under `unattended` only Cast's residual stops reach the foreman as approval points. Missing means `attended`.
- The backend reference may require its own environment (`ao`: an AO project id and `set-config`; see the reference). That wiring lives in the operator's configuration, never in the block.
- `.foreman/` must be gitignored; `valcraft:cast` adds it at scaffold time.
