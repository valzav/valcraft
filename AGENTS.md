# Agent instructions

## Orientation

- `plugins/valcraft/` — the shipped plugin. Everything under it is copied into a consumer's plugin cache on install; everything outside it is development scaffold.
- `plugins/valcraft/skills/<skill>/SKILL.md` — one directory per skill, with its own `references/`, `templates/`, or `evals/` beside it.
- `docs/` — repository documentation.

Read the docs relevant to your change before modifying a skill or a manifest. Do not invent missing requirements — ask, or record the assumption in the change.

## Writing standard

Use these rules for documentation, plans, skill instructions, code comments, reviews, issues, commit messages, and PR text.

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
- Do not hard-wrap prose paragraphs, list items, or blockquotes. Keep each on one physical line and rely on soft wrapping. Preserve line breaks only when Markdown syntax or embedded content requires them, such as headings, tables, code blocks, frontmatter, HTML blocks, and explicit hard breaks.

For instructions, prompts, safety rules, and error messages:

- Put one action in each instruction.
- Name the actor when it is not clear.
- Prefer direct commands and simple sentence structures.

## Commands

There is no application build or dependency install. The shipped plugin is Markdown, JSON, and YAML; standard-library Python scripts validate repository contracts and generated metadata.

- Develop a skill live: `claude --plugin-dir /path/to/valcraft/plugins/valcraft`, then `/reload-plugins` after each edit.
- Exercise the Codex packaging path: add the repository as a local marketplace with `codex plugin marketplace add /path/to/valcraft`, then install the cached copy with `codex plugin add valcraft@valcraft`. Use an isolated Codex profile for verification; never mutate the operator's live configuration without explicit approval.
- Verify the portable manifest: validate `plugins/valcraft/plugin.json` against `https://agent-plugins.org/schemas/1.0.0/plugin.schema.json` with any JSON Schema validator.
- Run a skill's evals (`plugins/valcraft/skills/<skill>/evals/evals.json`): invoke the skill-creator skill with "run the evals for plugins/valcraft/skills/<skill>". Direct its workspace to `.local/` (gitignored) — never to the default sibling location inside `plugins/valcraft/`.
- Regenerate the OpenCode skills index after any change under `plugins/valcraft/skills/` outside `evals/`: `python3 scripts/build-skills-index.py` (CI runs it with `--check`). OpenCode consumes the skills through that index over raw GitHub; there is no OpenCode manifest.
- Check the federated worker-report registry, routing codes, backend returns, and active transport-deviation eval references: `python3 scripts/check-coordination-contracts.py`. Run its discriminating static tests with `python3 scripts/tests/test_check_coordination_contracts.py`. These checks detect declaration drift; behavioral evals prove behavior.

## Architecture constraints

- The plugin subtree ships; the repository root does not. Never place development-only material under `plugins/valcraft/`. `plugins/valcraft/skills/index.json` is a consumer artifact (OpenCode's remote skills index), generated — never hand-edited.
- Both marketplace manifests, both native plugin manifests, the portable plugin manifest, and the marketplace key in a Claude Code consumer's `plugins.toml` use the single name `valcraft`. A mismatch causes sync churn or failed installs.
- The Claude Code manifest carries no `version` field. Claude Code version resolution falls through to the repository's commit SHA, so every push is a new version. The portable manifest is canonical for Codex when it and the native Codex manifest both exist. The native Codex manifest is its official compatibility fallback. Keep their release versions synchronized; a version does not control cache refresh.
- The native Claude Code, native Codex fallback, and portable manifests never merge. Update their shared metadata together. Current Codex does not merge fallback-only fields such as `skills` and `interface` when the portable manifest exists. Add a separate native manifest when a future harness requires one.
- The portable manifest allows no unknown top-level fields. Adding a Claude Code field or Codex field there breaks schema validation.
- No `~/.claude/skills` symlink may ever point into this repository. A bare skills directory auto-registers as an unmanaged `@skills-dir` plugin and breaks Claude Code config sync. Consumption is plugin-only.
- No secrets and no machine-local state. Machine-specific wiring lives in the operator's config repository.

## Change discipline

- Non-trivial work starts with a plan; working plans live in `.local/plans/` (gitignored), not in the repository.
- Keep tracked Valcraft content consumer-neutral. Do not name consumer projects, products, organizations, or brands. Keep consumer-specific evidence in the consumer repository or under gitignored `.local/`. Use a generic role, a neutral fictional identity, or an incident label instead. Valcraft and required third-party technology or platform names are exempt.
- Apply the MSW deletion test to commit messages and PR bodies: state only what the change does and why it matters, then delete every sentence whose removal loses none of that. No process narration, no restated diff, no filler.
- Update affected docs in the same change as the skill edit.
- Renaming a skill directory changes its invocation string. Update the skill's `name:` field, every self-reference in its description and body, and the README table together.

## Completion criteria

Before marking work complete:

1. Load each changed skill in every supported harness affected by the change. For Claude Code, use a `--plugin-dir` session and confirm the `valcraft:` namespace triggers. For Codex, install from the repository marketplace in an isolated profile and confirm the `$valcraft:<skill>` namespace triggers. If an isolated profile is unavailable, do not mutate the operator's live profile; report the skipped runtime check explicitly.
2. Validate each changed manifest with its native validator or schema. Run the Codex plugin validator for `plugins/valcraft`. Validate `plugins/valcraft/plugin.json` against the published portable schema if it changed.
3. Parse every changed JSON or YAML file and confirm all skill-relative paths resolve. Run `python3 scripts/build-skills-index.py --check` when a shipped skill file changed.
4. Run `python3 scripts/check-coordination-contracts.py` and `python3 scripts/tests/test_check_coordination_contracts.py` when a report producer, Foreman coordination contract, backend, or Foreman eval changed.
5. Update affected docs.
6. Confirm no secret material was added.
