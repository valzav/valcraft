# Developing valcraft

## Live editing

### Claude Code

Editing a skill in a clone does not affect installed sessions (the cache holds a copy).
For live editing, start a session against the plugin directory and reload after each edit:

```bash
claude --plugin-dir /path/to/valcraft/plugins/valcraft
# edit a SKILL.md, then in-session:
/reload-plugins
```

### Codex

Register the checkout as a local marketplace, then install its cached plugin copy:

```bash
codex plugin marketplace add /path/to/valcraft
codex plugin add valcraft@valcraft
```

Re-run `codex plugin add valcraft@valcraft` and start a new Codex session after edits. A
local marketplace installation is still a copy; it does not read later edits live.

## Repository structure

- `.claude-plugin/marketplace.json` — Claude Code marketplace manifest.
- `.agents/plugins/marketplace.json` — Codex repository marketplace manifest.
- `plugins/valcraft/` — the plugin: native Claude Code and Codex manifests, the portable
  Agent Plugins manifest, and `skills/<skill>/SKILL.md` with each skill's `references/`,
  `templates/`, and `evals/`. Only this subtree ships to consumers.
- `docs/`, `AGENTS.md` — repository documentation and agent instructions; never installed.

## Packaging

The plugin ships three manifests over one shared `skills/` tree:

- `plugins/valcraft/.claude-plugin/plugin.json` — Claude Code's plugin manifest.
- `plugins/valcraft/.codex-plugin/plugin.json` — Codex's native plugin manifest.
- `plugins/valcraft/plugin.json` — the portable
  [Agent Plugins](https://github.com/agentplugins/agent-plugins-spec) manifest (v1.0.0)
  for hosts that implement that specification and the canonical Codex manifest when both
  Codex manifest paths exist.

Keep shared metadata synchronized by hand. Keep the portable and Codex fallback versions
synchronized, but treat the version as release metadata rather than a cachebuster. Codex
does not merge fallback-only fields such as `skills` and `interface` when the portable
manifest exists; it discovers this plugin's default `skills/` tree automatically. Add
future harness-specific manifests beside these rather than adding unsupported fields to
the portable manifest.

Codex 0.147.0 limits each model-visible `SKILL.md` to 8,000 UTF-8 bytes and truncates
the remainder. Keep every shipped `SKILL.md` at or below that limit. Move detailed
procedures into one-level `references/` files and make the load condition explicit in
the skill body.

## Evals

Each skill carries `evals/evals.json` (prompt, fixtures under `evals/files/`, expected
output, assertions). Run them with the skill-creator skill: "run the evals for
`plugins/valcraft/skills/<skill>`", with the workspace directed to `.local/`.
