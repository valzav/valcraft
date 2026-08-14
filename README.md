# valcraft

Reusable agent skills, distributed as one plugin (`valcraft`) over a shared skills tree,
with native packaging for Claude Code and OpenAI Codex.

## Status

Alpha — Claude Code and Codex packaging are supported; the skill set grows one skill at
a time.

## Skills

| Skill     | Claude Code         | Codex               | What it does                                                                                      |
| --------- | ------------------- | ------------------- | ------------------------------------------------------------------------------------------------- |
| `cast`    | `/valcraft:cast`    | `$valcraft:cast`    | Bootstrap a project with lean SDD and selectable local or GitHub issue tracking.                  |
| `spec`    | `/valcraft:spec`    | `$valcraft:spec`    | Turn one local PRD/plan or explicit GitHub issue into the next canonical Cast feature spec.       |
| `forge`   | `/valcraft:forge`   | `$valcraft:forge`   | Implement one unit of work from its git-owned definition and hand the change to review.           |
| `review`  | `/valcraft:review`  | `$valcraft:review`  | Review a plan or code change against its Cast contract; report an auditable finding table.        |
| `temper`  | `/valcraft:temper`  | `$valcraft:temper`  | Retrospect over completed work; report graded, incident-cited lessons and propose standing rules. |
| `hone`    | `/valcraft:hone`    | `$valcraft:hone`    | Refine an existing prompt, skill, or agent instruction file against model guides.                 |
| `distill` | `/valcraft:distill` | `$valcraft:distill` | Reduce a prompt or skill to its goal-directed essence: goal, steps, constraints.                  |
| `msw`     | `/valcraft:msw`     | `$valcraft:msw`     | Apply the MSW Kernel to a markdown document: delete every claim its contract does not require.    |

All skills also trigger automatically from their descriptions. The host-specific command
is the explicit path, not the only one.

MSW Kernel origin: designed by "Fable at mega high monkey effort", published by
[@aienginerd](https://x.com/aienginerd/status/2085342869850603672).

## Install

### Claude Code

```bash
claude plugin marketplace add valzav/valcraft
claude plugin install valcraft@valcraft
```

Installing copies the plugin subtree into Claude Code's versioned cache
(`~/.claude/plugins/cache/`); no clone of this repository is required to consume it.

### Codex

```bash
codex plugin marketplace add valzav/valcraft
codex plugin add valcraft@valcraft
```

Start a new Codex session after installation. Codex reads the repository marketplace at
`.agents/plugins/marketplace.json`, then prefers `plugins/valcraft/plugin.json`. The
native `plugins/valcraft/.codex-plugin/plugin.json` remains the compatibility fallback.

## Update

### Claude Code

Auto-update stays off for third-party marketplaces, so pull changes with the update pair:

```bash
claude plugin marketplace update valcraft   # refresh the catalog
claude plugin update valcraft@valcraft      # refresh the installed cache copy
```

The plugin carries no `version` field, so the cache is keyed by this repository's commit
SHA — every push is a new version and the pair above picks it up.

### Codex

```bash
codex plugin marketplace upgrade valcraft
codex plugin add valcraft@valcraft
```

Codex has no `plugin update` command. Re-running `add` installs the plugin from the
refreshed marketplace snapshot. The manifest version describes a release; it does not
control cache refresh. Start a new Codex session afterward.

## Develop

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
  Agent Plugins manifest, and `skills/<skill>/SKILL.md`. Only this subtree ships to
  consumers.
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
