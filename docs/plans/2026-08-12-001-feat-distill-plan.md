# Plan: distill skill

Date: 2026-08-12. Status: approved, in progress.

## Goal

Add a third skill, `distill`, that reduces a prompt artifact — inline prompt text, a
markdown prompt file, a skill directory, or a workflow — to the minimal instruction set
that achieves its goal, presented as a short structured summary (the distillate).

`distill` serves three uses:

1. See what an over-instructed skill actually does. Skills written for older models carry
   noise that current models do not need.
2. Compare two similar artifacts. Two distillates with aligned steps make differences
   visible.
3. Seed evals. Each surviving step restated as an observable assertion.

## Decisions

- Output goes to chat as a short summary (goal, applicability, steps, one dropped-total
  line); distill then offers save options: a cleaned skill in `~/.claude/skills/<name>/`
  (with a custom-name variant on collision or request), the YAML distillate, or the full
  summary markdown — the latter two in the current working directory. Nothing saves next
  to the source: skills usually live in caches the user never opens. (Amended
  2026-08-12; the original decision was chat-only with save on request.)
- Compare mode is built in: two inputs produce two step-aligned distillates plus a
  difference summary.
- The distillate ends with a "Testable behaviors" section: each step or constraint as an
  observable assertion.
- The core mechanism is a deletion test stated inside the skill itself: an instruction
  survives only if deleting it leaves the artifact's goal unmet or unproven. The skill is
  self-contained; it references no private material.
- The distillate has a fixed section order and, on request, a machine-readable YAML
  variant with stable keys (`name`, `goal`, `use_when`, `do_not_use_when`, `inputs`,
  `steps`, `constraints`, `testable_behaviors`, `dropped`). Downstream tooling may rely
  on the keys.
- SkillDog integration stays out of this plugin. A separate adapter in the skilldog
  repository (docs/contract-generation/manual-contract-generator/) will map distillate
  keys to its semantic enrichment fields. Rationale: the execution contract is a
  fail-closed schema whose mechanical facts must not be model-generated, and embedding a
  private versioned schema into a shipped plugin couples every consumer to it.
- Boundary with `hone`: `hone` rewrites the artifact in place; `distill` produces a
  derived summary and never edits the source.
- Two modes, asked up front unless the request names one (amended 2026-08-12): study —
  maximum reduction, distillate output; clean — an operability-preserving leaner copy
  that keeps the original frontmatter, structure, resource references, and output
  contracts, dropping a line only when the artifact does its job identically without
  it.

## Tasks

- T-1 Write this plan.
- T-2 Create `plugins/valcraft/skills/distill/SKILL.md`.
- T-3 Update the README skills table and both manifest descriptions.
- T-4 Validate `plugins/valcraft/plugin.json` against the published schema.
- T-5 Load the skill in a `--plugin-dir` session and confirm it registers.

## Out of scope

- The skilldog-side adapter (separate task in that repository).
- Evals for distill itself (add after first real usage).
