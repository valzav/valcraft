---
name: distill
description: Distill a prompt artifact — inline prompt text, a markdown prompt file (system prompt, agent instructions, slash command), a skill directory, or a workflow — into its minimal goal-directed essence, a short structured summary of goal, applicability, steps, and load-bearing constraints. Use whenever the user runs /valcraft:distill, or asks to distill, condense, deconstruct, or boil down a prompt or skill, asks what a skill actually does under the noise, wants a cleaned minimal copy of a skill saved as a new skill, or wants to compare two similar skills or prompts. Read-only over the source — for improving the artifact in place, use hone.
---

# distill

Reduce a prompt artifact to the smallest instruction set that still achieves its goal,
and present the result either as a short structured summary — the distillate — or as a
leaner working copy, depending on the user's goal. distill never edits the source. When
the user wants the source improved in place, offer `hone` instead.

## Mode

Establish the user's goal before distilling. Ask with the harness's structured question
tool when one exists, otherwise in plain text — but skip the question when the request
already names the goal:

- **Study** — understand the artifact, compare it with another, or seed evals. Maximum
  reduction: every claim faces the deletion test against the goal essence, and the
  output is the distillate.
- **Clean** — produce a leaner copy the user will run instead of the original. Drop a
  line only when the artifact does its job identically without it. Keep the original
  frontmatter (`name` and `description` control triggering), the file structure, the
  references to bundled resources, and every output contract. The output is a drop-in
  replacement, not a summary.

## The deletion test

State the artifact's goal first: the outcome it exists to produce and the criteria that
prove it. The artifact's own output contract and safety rules are part of that goal —
contract terms, never deletion candidates.

Then judge every instruction by one test: **if deleting it leaves the goal unmet or
unproven, it survives; otherwise it is noise.** Useful, thorough, and plausible are not
aliases for necessary.

Typical noise, grouped for the report:

- **repetition** — the same rule stated in several places;
- **default behavior** — instructions current models follow unprompted ("think step by
  step", "be helpful", "use tools when appropriate");
- **old-model babysitting** — ALWAYS/NEVER walls and exhaustive case enumerations where a
  capable model generalizes from one steering line;
- **ceremony** — formatting, tone, and process demands not tied to the outcome;
- **dead references** — files, tools, or sections that do not exist.

A rationale attached to an instruction is not noise. Brief steering plus its reason
generalizes better than the bare command, so decompose "instruction + its why" as one
claim and let them survive together. Only a reason attached to nothing — motivational
prose, vendor statistics, pep talk — is droppable.

## Workflow

1. Read the whole artifact. For a skill directory: SKILL.md plus every referenced
   resource. Never distill text you have not fully read — a line that looks redundant may
   be load-bearing for a case you have not seen.
2. State the goal and success criteria in one or two lines, before decomposing.
3. Decompose the artifact into atomic claims: each instruction, step, rule, constraint,
   example.
4. Apply the deletion test to each claim. When unsure whether a claim is load-bearing,
   keep it marked "(unclear necessity)" — never drop on suspicion.
5. Show a chat summary. Study mode: the goal, the applicability boundaries, the
   numbered steps, and one line totaling what was dropped ("dropped 12 of 19
   instructions: repetition ×4, ceremony ×5, …") — a few short paragraphs plus one
   list, not the full distillate. Clean mode: the word delta and the dropped groups —
   the copy itself is the deliverable.
6. Offer the save options below and act on the user's choice.

Quality bar: every line of the distillate is specific enough to act on without opening
the source. Keep the source's concrete verbs, file names, and tool names. Where the
source leaves something undefined, write the gap explicitly ("undefined in source: …")
instead of filling it with plausible prose. Never invent facts the source does not state
— auth, endpoints, tool schemas, environment.

## Saving the result

Nothing defaults to "next to the source": skills usually live in plugin caches and
`.claude/` directories the user never opens. In clean mode the cleaned copy is the
deliverable: default to option 1 for skills, or `./<name>.cleaned.md` in the current
working directory for other artifacts. In study mode offer all options, plus "don't
save" — the chat summary is already delivered:

1. **Cleaned skill** — generate a new minimal SKILL.md from the surviving instructions
   (in clean mode, preserving the original frontmatter and structure; in study mode, a
   fresh `name` and `description` over the distilled body) and save it to
   `~/.claude/skills/<name>/SKILL.md`, where Claude Code auto-registers personal skills.
   The result is usable in place of the original; the original stays untouched. If the
   name collides with an installed skill, switch to the custom-name variant.
   - **Custom name** — the same, but ask the user for a new skill name and use it for
     both the directory and the frontmatter.
2. **YAML distillate** — the stable-key form described below, saved to
   `./<name>.distilled.yaml` in the current working directory.
3. **Summary markdown** — the full distillate format below, saved to
   `./<name>.distilled.md` in the current working directory.

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

**Dropped:** <one line per noise group: category — count — representative example>
```

The YAML distillate carries the same content with exactly these keys: `name`, `goal`,
`use_when`, `do_not_use_when`, `inputs`, `steps`, `constraints`, `testable_behaviors`,
`dropped`. The keys are stable — downstream tooling relies on them.

## Compare mode

A request to compare two artifacts implies study mode — skip the mode question.

1. Launch one subagent per artifact with the harness's agent tool, both in a single
   message so they run in parallel. Each subagent runs the full study-mode workflow on
   its artifact and returns only the YAML distillate — the stable keys make the handoff
   reliable.
2. Compare the distillates, not the sources. Do not re-read the artifacts, and never
   execute either one: every behavioral claim is inferred from the distillates.
3. Align vocabulary first: steps that accomplish the same thing get identical phrasing
   in both distillates.
4. Report the behavioral diff, not the two distillates:
   - the shared core, in one or two lines;
   - differences grouped: only in A; only in B; same step under different constraints;
   - the divergence in results — given the same input, what each artifact would do or
     produce differently, inferred from the distillates.

Present differences without a verdict. Recommend one only when the user asks which to
prefer, and tie the recommendation to their stated use. Offer to save the two
distillates with the standard save options.

## What not to do

- Never edit the source artifact.
- Don't paraphrase steps into vagueness — a distillate in generic verbs fails the quality
  bar even when structurally correct.
- Don't drop safety rules or output contracts as noise; they are part of the goal.
- Don't grade, score, or rewrite the source — distill describes, and at most emits a
  cleaned copy elsewhere. Improving the artifact in place is `hone`.
