# distill — save destinations and output formats

Read this file when offering or acting on save options.

## Saving the result

Nothing defaults to "next to the source": skills usually live in plugin caches and host-specific `.agents/` or `.claude/` directories the user never opens. In clean mode the cleaned copy is the deliverable: default to option 1 for skills, or `./<name>.cleaned.md` in the current working directory for other artifacts. In study mode offer all options, plus "don't save" — the chat summary is already delivered:

1. **Cleaned skill** — select the active harness's personal-skill destination: `~/.agents/skills/<name>/` under Codex, `~/.claude/skills/<name>/` under Claude Code, or `~/.cursor/skills/<name>/` under Cursor. That Cursor path is a personal destination, not the Valcraft product install path. Copy the complete source skill directory there, then replace only its `SKILL.md` with the cleaned version (in clean mode, preserving the original frontmatter and structure; in study mode, a fresh `name` and `description` over the distilled body). Preserve every bundled resource referenced by a surviving instruction. The result is usable in place of the original; the original stays untouched. If the destination already exists, ask the user for a new skill name and use it for both the directory and the frontmatter. In study mode, create a new skill only when the generated `SKILL.md` is self-contained.
2. **YAML distillate** — the stable-key form defined in SKILL.md, saved to `./<name>.distilled.yaml` in the current working directory.
3. **Summary markdown** — the full distillate format below, saved to `./<name>.distilled.md` in the current working directory.

## Distillate format

The full saved form. Fixed section order; omit a section only when it is empty.

```markdown
## <name> — distilled

**Goal:** <one line: the outcome and what proves it>
**Use when:** <positive applicability boundary>
**Do not use when:** <the nearest tasks this artifact is not for>
**Inputs:** <what the artifact needs to start>

**Steps:**

1. <concrete action, in the source's own verbs and names>

**Load-bearing constraints:**

- <rule that survives the deletion test but is not a step>

**Testable behaviors:**

- <a step or constraint restated as an assertion observable in the artifact's
  output or effects — ready to become an eval check>

**Dropped:**

- <one bullet per noise group: category — count — representative example>
```
