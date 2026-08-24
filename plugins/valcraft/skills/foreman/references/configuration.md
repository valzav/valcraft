# Foreman runtime configuration

Read the committed `.valcraft/config.yaml`, the optional gitignored `.valcraft/config.local.yaml` overlay, and [`../../tune/references/config.md`](../../tune/references/config.md) completely. Tune is the sole configuration writer.

Resolution rules:

- Resolve the configuration per the Tune contract: the base overridden by the overlay on the user-scoped keys `foreman.approval_mode`, `foreman.backend`, and `foreman.herdr`, with `backend` and `herdr` overriding as a unit. Require the resolved configuration to be complete and valid. Never apply read-time defaults or inspect legacy declarations in `AGENTS.md`.
- A repo-scoped key in the overlay is invalid configuration; delegate it to `valcraft:tune`.
- Use `tracker.mode` to select intake. Use the resolved `foreman.backend` and `foreman.approval_mode`, and the base `foreman.default_branch` and `foreman.release_branch`, exactly as stored.
- In GitHub mode, use `foreman.clarification_assignees` exactly as stored.
- For Herdr, use the resolved session and complete worker map. See its backend reference for translation to native command arguments.
- Delegate any missing or invalid value to `valcraft:tune` for the affected section. Resume only after `Status: done` and a complete re-read.
- Everything under `.valcraft/` except `config.yaml` must be gitignored; `valcraft:cast` establishes the `/.valcraft/*` and `!/.valcraft/config.yaml` pair at scaffold time.
