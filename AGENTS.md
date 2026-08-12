# Agent instructions

## Orientation

- `plugins/valcraft/` — the shipped plugin. Everything under it is copied into a
  consumer's plugin cache on install; everything outside it is development scaffold.
- `plugins/valcraft/skills/<skill>/SKILL.md` — one directory per skill, with its own
  `references/`, `templates/`, or `evals/` beside it.
- `specs/` — feature behavior (`spec.md`), technical design (`design.md`), ordered
  implementation tasks (`tasks.md`).
- `docs/plans/` — working plans, tracked in git.

Read the docs relevant to your change before modifying a skill or a manifest. On conflict,
accepted ADRs prevail, then `specs/`, then derived `docs/`. Do not invent missing
requirements — record assumptions and open questions in the relevant spec, and
consequential technical decisions as ADRs under `docs/architecture/adr/`.

## Writing standard

Use these rules for documentation, specifications, ADRs, plans, skill instructions, code
comments, reviews, issues, commit messages, and PR text.

- Write for quick and unambiguous reading.
- Preserve precise terms, necessary qualifiers, and natural English.
- Prefer active voice when the actor matters.
- Keep each sentence focused. Split sentences that contain unrelated ideas or multiple instructions.
- Use one consistent term for each project concept. Do not change terms only for variety.
- Keep each paragraph focused on one topic.
- Use lists when prose would hide steps, options, or conditions.
- Define unfamiliar domain terms once. Keep established technical terms and necessary jargon.
- Avoid long noun chains, vague pronouns, and missing subjects.
- Preserve facts, conditions, exceptions, and scope. Never remove meaning only to make text shorter.
- Treat sentence length as a clarity signal, not a hard limit.

For instructions, prompts, safety rules, and error messages:

- Put one action in each instruction.
- Name the actor when it is not clear.
- Prefer direct commands and simple sentence structures.

## Commands

There is no build, no dependency install, and no test runner — the repository is markdown
and JSON.

- Develop a skill live: `claude --plugin-dir ~/dev/valcraft/plugins/valcraft`, then
  `/reload-plugins` after each edit.
- Verify the portable manifest: validate `plugins/valcraft/plugin.json` against
  `https://agent-plugins.org/schemas/1.0.0/plugin.schema.json` with any JSON Schema
  validator.
- Run a skill's evals (`plugins/valcraft/skills/<skill>/evals/evals.json`): invoke the
  skill-creator skill with "run the evals for plugins/valcraft/skills/<skill>". Direct
  its workspace to `.local/` (gitignored) — never to the default sibling location inside
  `plugins/valcraft/`.

## Architecture constraints

- The plugin subtree ships; the repository root does not. Never place development-only
  material under `plugins/valcraft/`.
- `.claude-plugin/marketplace.json`'s `name`, the plugin's name, and the marketplace key in
  the consumer's `plugins.toml` are all the single string `valcraft`. A mismatch causes
  perpetual sync churn and failed installs.
- Neither manifest carries a `version` field. Version resolution falls through to the
  repository's commit SHA, so every push is a new version.
- The two manifests (`plugins/valcraft/.claude-plugin/plugin.json` and
  `plugins/valcraft/plugin.json`) never merge. Update both when plugin metadata changes.
- The portable manifest allows no unknown top-level fields. Adding a Claude Code field
  there breaks schema validation.
- No `~/.claude/skills` symlink may ever point into this repository. A bare skills
  directory auto-registers as an unmanaged `@skills-dir` plugin and breaks Claude Code
  config sync. Consumption is plugin-only.
- No secrets and no machine-local state. Machine-specific wiring lives in the operator's
  config repository.

## Change discipline

- Product intent lives in `spec.md`; implementation detail in `design.md`.
- Reference requirement and task IDs (`FR-`, `AC-`, `T-`) from commits and tests.
- Non-trivial work starts with a plan in `docs/plans/YYYY-MM-DD-NNN-<type>-<slug>-plan.md`.
- Update affected specs, ADRs, and docs in the same change as the skill edit.
- Renaming a skill directory changes its invocation string. Update the skill's `name:`
  field, every self-reference in its description and body, and the README table together.

## Completion criteria

Before marking work complete:

1. Load the changed skill in a `--plugin-dir` session and confirm it appears under the
   `valcraft:` namespace and triggers.
2. Validate `plugins/valcraft/plugin.json` against the published schema if it changed.
3. Update affected specifications, designs, and ADRs.
4. Confirm no secret material was added.
