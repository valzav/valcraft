# <Project name>

<One-paragraph description: what it is and its primary value.>

## Status

Pre-development | Prototype | Alpha | Beta | Production

## Repository structure

- `docs/` — product brief, plans, and architecture documentation.
- `specs/` — Spec-owned feature triplets and quick-task contracts.
- `<source dirs>` — application code.

## Documentation

- [Product brief](docs/product-brief.md)
- [Architecture overview](docs/architecture/overview.md)
- [Architecture decisions](docs/architecture/adr/)
- [Feature specifications](specs/)
<!-- When docs/status.md exists, render this bullet and remove this instruction:
- [Operational snapshot](docs/status.md) — dated, non-authoritative external observations.
Omit both the bullet and this instruction when the snapshot is absent. -->

## Development

### Spec-driven workflow

Claude Code `/valcraft:valcraft-<name>`; Codex `$valcraft:valcraft-<name>`; OpenCode `valcraft-<name>`; Cursor `/valcraft-<name>`.

Start with the project frame and product brief created by Cast. Run `valcraft-spec` to create the first MVP feature, a later feature triplet, or a quick task. For task delivery, use Draft, Review, Forge, Review, and Land directly, or let Foreman coordinate those stages.

Valcraft's shared settings live in the committed `.valcraft/config.yaml`; personal overrides live in the gitignored `.valcraft/config.local.yaml`. Run `valcraft-tune` to change tracker, approval, Foreman, branch, Herdr worker, or pull-request choices.

### Prerequisites

<Runtimes, package managers, databases, external tools.>

### Install / run / test

```bash
<install command>
<dev command>
<test command>
<lint + type-check commands>
```

## Configuration

<Environment variables and local setup. No secrets in the repo — references only.>
