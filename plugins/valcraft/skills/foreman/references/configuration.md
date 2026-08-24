# Foreman runtime configuration

Read `.valcraft/config.yaml` and [`../../tune/references/config.md`](../../tune/references/config.md) completely. Tune is the sole configuration writer.

Resolution rules:

- Require a complete valid snapshot. Never apply read-time defaults or inspect legacy declarations in `AGENTS.md`.
- Use `tracker.mode` to select intake. Use `foreman.backend`, `foreman.approval_mode`, `foreman.default_branch`, and `foreman.release_branch` exactly as stored.
- In GitHub mode, use `foreman.clarification_assignees` exactly as stored.
- For Herdr, use the configured session and complete worker map. See its backend reference for translation to native command arguments.
- Delegate any missing or invalid value to `valcraft:tune` for the affected section. Resume only after `Status: done` and a complete re-read.
- `.valcraft/` must be gitignored; `valcraft:cast` establishes the rule at scaffold time.
