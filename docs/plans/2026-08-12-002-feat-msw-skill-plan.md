# Plan: msw skill

Date: 2026-08-12. Status: approved, in progress.

## Goal

Add a fourth skill, `msw`, that applies the MSW Kernel to a markdown document passed as
the argument to `/valcraft:msw` — a plan, a spec, a skill, a prompt, or any other .md
file. The skill judges every claim in the document by the kernel's deletion test against
the document's own contract, deletes the claims that fail, and reports in the kernel's
report format.

Origin: the MSW Kernel by @aienginerd
(https://x.com/aienginerd/status/2085342869850603672). The operator's global CLAUDE.md
carries the same kernel for task execution; this skill applies it to documents instead,
and ships the kernel text so plugin consumers do not need that private file.

## Decisions

- Output mode: edit in place (owner decision, 2026-08-12). The skill deletes failing
  claims from the document and reports the delta. The file is a working copy; git
  protects it. When the target is outside a git repository, say so in the report before
  editing.
- The kernel text ships verbatim in `references/kernel.md` — program, definitions,
  fuses, and the "No unauthoritative limits" rule. SKILL.md instructs, the reference
  defines; the skill never paraphrases the kernel.
- The document's contract is derived from the document itself (its stated goal, or the
  outcome it evidently exists to produce). If no contract is derivable and the user is
  attended, ask; unattended, bind the smallest reading consistent with the document's
  evident intent and record the assumption in the report — mirroring the kernel's own
  ambiguity rule.
- A dedicated limits pass applies "No unauthoritative limits" to the document: every
  numeric cap, threshold, count, or budget must name its authority or be deleted.
- Boundary with `distill`: distill targets prompt artifacts and reduces them to a
  goal-directed essence without editing the source; msw targets any markdown document,
  judges it against its own contract including the limits audit, and edits in place.
- Boundary with `hone`: hone refines prompt artifacts against vendor prompting guides;
  msw applies one fixed necessity test and adds nothing — it only deletes and reports.

## Tasks

- T-1 Write this plan.
- T-2 Create `plugins/valcraft/skills/msw/SKILL.md` and `references/kernel.md`.
- T-3 Update the README skills table and both manifest descriptions.
- T-4 Validate `plugins/valcraft/plugin.json` against the published schema.
- T-5 Load the skill in a `--plugin-dir` session and confirm it registers.

## Out of scope

- Applying msw to non-markdown files or to code.
- Evals for msw itself (add after first real usage).
