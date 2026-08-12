---
name: distill
description: Distill a prompt artifact — inline prompt text, a markdown prompt file (system prompt, agent instructions, slash command), a skill directory, or a workflow — into its minimal goal-directed essence, a short structured summary of goal, applicability, steps, and load-bearing constraints. Use whenever the user runs /valcraft:distill, or asks to distill, condense, deconstruct, or boil down a prompt or skill, asks what a skill actually does under the noise, or wants to compare two similar skills or prompts. Read-only over the source — for improving the artifact itself, use hone.
---

# distill

Reduce a prompt artifact to the smallest instruction set that still achieves its goal, and
present that essence as a short structured summary — the distillate. distill never edits
the source. When the user wants the source improved, offer `hone` instead.

The distillate serves three uses: seeing what an over-instructed artifact actually does,
comparing two similar artifacts, and seeding evals from testable behaviors.

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

## Workflow

1. Read the whole artifact. For a skill directory: SKILL.md plus every referenced
   resource. Never distill text you have not fully read — a line that looks redundant may
   be load-bearing for a case you have not seen.
2. State the goal and success criteria in one or two lines, before decomposing.
3. Decompose the artifact into atomic claims: each instruction, step, rule, constraint,
   example.
4. Apply the deletion test to each claim. When unsure whether a claim is load-bearing,
   keep it marked "(unclear necessity)" — never drop on suspicion.
5. Emit the distillate in the format below. Chat by default; write a file only when the
   user asks to save (default `<name>.distilled.md` next to the source).

Quality bar: every line of the distillate is specific enough to act on without opening
the source. Keep the source's concrete verbs, file names, and tool names. Where the
source leaves something undefined, write the gap explicitly ("undefined in source: …")
instead of filling it with plausible prose. Never invent facts the source does not state
— auth, endpoints, tool schemas, environment.

## Distillate format

Fixed section order; omit a section only when it is empty.

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

When the user asks for machine-readable output or an import payload, emit the same
content as YAML with exactly these keys: `name`, `goal`, `use_when`, `do_not_use_when`,
`inputs`, `steps`, `constraints`, `testable_behaviors`, `dropped`. The keys are stable —
downstream tooling relies on them.

## Compare mode

Given two artifacts:

1. Distill both.
2. Align vocabulary: steps that accomplish the same thing get identical phrasing in both
   distillates.
3. After the two distillates, summarize differences in four groups: shared steps; only in
   A; only in B; same step under different constraints.

Present differences without a verdict. Recommend one only when the user asks which to
prefer, and tie the recommendation to their stated use.

## What not to do

- Never edit the source artifact.
- Don't paraphrase steps into vagueness — a distillate in generic verbs fails the quality
  bar even when structurally correct.
- Don't drop safety rules or output contracts as noise; they are part of the goal.
- Don't grade, score, or improve — distill describes. Improving is `hone`.
