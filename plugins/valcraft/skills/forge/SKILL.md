---
name: forge
description: >
  Bootstrap a new project with Val's lean spec-driven development (SDD) scaffold —
  README, AGENTS.md (+ CLAUDE.md symlink), product brief, ADRs, and numbered
  specs/<NNN>-<feature>/ spec+design+tasks triplets — then run the
  plan → implement → review working loop. Use whenever Val starts a new project or
  repository, says "new project", "start building X", "scaffold this", "set up
  specs", or wants to retrofit spec-driven structure onto an existing codebase,
  even if he doesn't mention SDD or docs explicitly.
---

# forge

Lean SDD project scaffold. Distilled 2026-08-03 from a 1550-line Codex-oriented starter
template plus two weeks of practice on the reference project that implements this
workflow. Everything here earned its place there; everything else
from the source template was deliberately dropped. Resist reintroducing heavyweight
machinery (full traceability matrices, 20-section templates, contracts/ trees) unless the
project demonstrably needs it — the goal is durable context, not documentation theater.

## Principles

- **Docs before code.** The first commit is a documentation baseline. Code arrives after
  the stack and boundaries are settled in ADRs.
- **Stable IDs are the working currency.** `FR-001`, `AC-003`, `T012`, `ADR-0009` get
  referenced from commit subjects, reviews, tests, and follow-up plans. IDs + links give
  you traceability for free; matrices are theater.
- **Never invent missing requirements.** Record assumptions and open questions in the
  spec instead. Populate documents from evidence in priority order: facts the user gave →
  existing repo/code → established conventions → clearly-marked assumptions.
- **Scale docs to the project.** Every file below is opt-in past the skeleton. A weekend
  tool needs five files; a system with real machine boundaries grows contracts/ later.

## Step 1: Gather project facts

Ask only what changes the scaffold; `TBD` is an acceptable answer for the rest.

1. Name + one-sentence description
2. Primary user and the problem being solved
3. MVP outcome (one coherent end-to-end journey, not an infra chore list)
4. Stack: language, framework, data store, deploy target
5. Machine interfaces? (public API / events / multi-service → plan a `contracts/` dir later)
6. Domain-heavy vocabulary? (→ add `docs/glossary.md`)

## Step 2: Create the skeleton

```text
README.md                     # from templates/README.md
AGENTS.md                     # from templates/AGENTS.md — keep it ~100 lines
CLAUDE.md                     # symlink → AGENTS.md (one instruction file, every agent host)
.gitignore                    # from templates/gitignore-base + stack ignores
docs/
├── product-brief.md          # from templates/product-brief.md (system requirements folded in)
├── plans/                    # working plans — tracked in git, NOT ignored
└── architecture/
    ├── overview.md           # short: context, components, boundaries, data ownership
    └── adr/README.md         # ADR index (one line per ADR)
specs/
└── 001-mvp/
    ├── spec.md               # from templates/spec.md — what and why
    ├── design.md             # from templates/design.md — how
    └── tasks.md              # from templates/tasks.md — ordered, verifiable
```

Copy templates from this skill's `templates/` directory and fill them in. Create the
CLAUDE.md symlink with `ln -s AGENTS.md CLAUDE.md` (relative, so the repo moves cleanly).

Opt-in additions — create only when the trigger is real:

| Add                                        | When                                                           |
| ------------------------------------------ | -------------------------------------------------------------- |
| `docs/glossary.md`                         | Domain terms that must not be reworded exist                   |
| `docs/system-requirements.md`              | Cross-cutting requirements outgrow the brief section           |
| `docs/use-cases/uc-NNN-*.md`               | Product steering needs narrative scenarios (interview output)  |
| `contracts/` + README                      | Real machine boundaries: public API, events, multiple services |
| `specs/NNN-*/research.md`, `data-model.md` | A feature is complex enough to need them                       |

## Step 3: Populate and define the MVP

- Fill the skeleton from evidence (priority order above). Mark every assumption.
- `specs/001-mvp/` describes one coherent end-to-end outcome: scenarios, functional
  requirements (`FR-`), acceptance criteria (`AC-`), non-goals, edge cases.
- Identify consequential technical decisions. Write each as an ADR
  (`docs/architecture/adr/NNNN-kebab-title.md`, from `templates/adr.md`) — accepted or
  explicitly open. The reference project accepted 16 ADRs in the first week; cheap to write, expensive
  to reconstruct. Small implementation choices don't need ADRs.
- Ready to code when: user + problem stated, MVP journey specified with IDs, non-goals
  explicit, stack decided or an open ADR says why not, build/test/lint commands in
  AGENTS.md, assumptions visible.

## Step 4: The working loop (per feature/task)

1. **Plan** — non-trivial work gets a plan in `docs/plans/YYYY-MM-DD-NNN-<type>-<slug>-plan.md`
   (e.g. `2026-08-02-001-feat-t030-predicate-compiler-plan.md`). Plans referenced from
   tasks.md are tracked in git — never gitignored (the reference project tried, reverted same day).
2. **Implement** — small verifiable tasks; commit subjects reference IDs
   (`T029: predicate registry…`, `fix(t030): resolve the material findings…`).
3. **Review** — run an independent review (second model or fresh agent). Findings get IDs
   (`R-001…`), material ones get a remediation plan in `docs/plans/`, resolution commits
   cite the IDs. **Do not commit raw review records** — the reference project committed one and removed
   it the next commit; findings live in the remediation plan and commit messages.
4. **Update docs in the same change** — specs, ADRs, and contracts affected by the code
   change move with it, not in a later sweep.

## Deliberately omitted (don't add back without cause)

From the source template, dropped after practice on the reference project:

- ISO/IEEE standards references and document-lifecycle machinery — a `status:` line in
  frontmatter is enough.
- The 20-section spec/design templates — actors tables, analytics, rollout constraints,
  state models are opt-in sections listed inside the lean templates.
- Traceability matrix tables — stable IDs referenced from commits/tests do the job.
- `contracts/` scaffolding by default — the reference project needed it (multi-engine, event
  envelopes); most projects don't start there.
- Committing the starter template into the project repo — the skill is its durable home.
- Verbose AGENTS.md — the reference project condensed it on day 1; ~100 lines, imperative, no product
  content.
