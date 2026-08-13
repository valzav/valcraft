# valcraft

Val's Claude Code skills, distributed as a plugin marketplace. One marketplace, one plugin
(`valcraft`), one directory per skill.

## Status

Alpha — the packaging is settled; the skill set grows one skill at a time.

## Skills

| Skill     | Invoke              | What it does                                                                                   |
| --------- | ------------------- | ---------------------------------------------------------------------------------------------- |
| `forge`   | `/valcraft:forge`   | Bootstrap a project with lean SDD and selectable local or GitHub issue tracking.               |
| `hone`    | `/valcraft:hone`    | Refine an existing prompt, skill, or agent instruction file against model guides.              |
| `distill` | `/valcraft:distill` | Reduce a prompt or skill to its goal-directed essence: goal, steps, constraints.               |
| `msw`     | `/valcraft:msw`     | Apply the MSW Kernel to a markdown document: delete every claim its contract does not require. |

All skills also trigger automatically from their descriptions — the slash commands are
the explicit path, not the only one.

MSW Kernel origin: designed by "Fable at mega high monkey effort", published by
[@aienginerd](https://x.com/aienginerd/status/2085342869850603672).

## Install

```bash
claude plugin marketplace add valzav/valcraft
claude plugin install valcraft@valcraft
```

Installing copies the plugin subtree into Claude Code's versioned cache
(`~/.claude/plugins/cache/`); no clone of this repository is required to consume it.

This repository is currently **private**, so the commands above need a GitHub account
with read access — Claude Code clones it over SSH. Nothing else about the install path
changes.

## Update

Auto-update stays off for third-party marketplaces, so pull changes with the update pair:

```bash
claude plugin marketplace update valcraft   # refresh the catalog
claude plugin update valcraft@valcraft      # refresh the installed cache copy
```

The plugin carries no `version` field, so the cache is keyed by this repository's commit
SHA — every push is a new version and the pair above picks it up.

## Develop

Editing a skill in a clone does not affect installed sessions (the cache holds a copy).
For live editing, start a session against the plugin directory and reload after each edit:

```bash
claude --plugin-dir ~/dev/valcraft/plugins/valcraft
# edit a SKILL.md, then in-session:
/reload-plugins
```

## Repository structure

- `.claude-plugin/marketplace.json` — marketplace manifest.
- `plugins/valcraft/` — the plugin: Claude Code manifest, portable Agent Plugins manifest,
  and `skills/<skill>/SKILL.md`. Only this subtree ships to consumers.
- `docs/`, `AGENTS.md` — repository documentation and agent instructions; never installed.

## Packaging

The plugin ships two manifests over one shared `skills/` tree:

- `plugins/valcraft/.claude-plugin/plugin.json` — Claude Code's plugin manifest.
- `plugins/valcraft/plugin.json` — the portable
  [Agent Plugins](https://github.com/agentplugins/agent-plugins-spec) manifest (v1.0.0),
  which VS Code, Copilot, Codex, Cursor, and Kiro read. Claude Code ignores it.

The two manifests are independent files kept in sync by hand.
