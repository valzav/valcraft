# temper report format

The single file a temper run creates. This reference is the format authority; SKILL.md
owns the process that fills it.

## File

- Location: `docs/retro/` in the analyzed project, tracked in git.
- Name: `YYYY-MM-DD-NNN-<mode>-<scope>.md`, where `<mode>` is `analyze` or
  `synthesize` and `<scope>` is a short kebab-case name of the corpus or source set
  (`003-search`, `prs-38-55`, `q3-features`).
- Allocate `NNN` as one more than the highest number already present for that
  date in `docs/retro/` (`2026-08-20-001-…`, `2026-08-20-002-…`); an empty date
  starts at `001`. `NNN` exists to keep same-date filenames unique and ordered;
  if the computed number is taken by the time of writing (a concurrent run),
  take the next free one instead of probing repeatedly. Never overwrite or
  extend an existing report.
- Reports are append-only history: a report is never edited after its run. A later run
  that overturns a lesson writes its own report and proposes the retirement there.

## Lesson IDs

- `L-NNN`, numbered from `L-001`, stable within one report, never renumbered.
- The citation form is `<report file>, L-NNN`
  (`2026-08-20-001-analyze-003-search.md, L-004`). `AGENTS.md` standing rules, later
  reports, and upstream submissions cite lessons in this form.
- A synthesis report's merged themes carry their own L-IDs, local to that report; each
  theme also cites every contributing analyze report and source L-ID.

## Incident record

Every incident behind a candidate carries six fields:

1. **Root-incident key** — one identifier per real-world event, shared by every
   citation that traces back to it. Two sources describing the same event share one
   key.
2. **Source locator** — commit SHA, PR, file:line, or transcript path and quote. A
   locator says where the claim lives, not that it is true.
3. **Observed outcome** — what actually happened, stated from the evidence.
4. **Claimed cause** — the causal explanation the source or the analysis asserts.
5. **Verification method** — how this run checked the claim: diff read, command
   re-run, test re-run, cross-source match. `none` is a valid value.
6. **Verification result** — what the check showed. A partial verification names
   what was and was not checked ("verified on the commit record, not on the
   ledger text") and supports the claim only as far as it reached. An incident
   whose chain lacks a successful verification is marked **unverified**.

## Evidence grades

- **A** — corroborated by at least two root incidents with non-derivative causal
  chains. Two root incidents corroborate independently when they arose in
  different units of work and neither's record cites the other or a shared
  source. Multiple reports or sources derived from one root incident strengthen
  its trace but never make an A.
- **B** — one verified root incident.
- **C** — weak or unverified: an uncorroborated self-report, an inference without a
  verified incident record, or evidence its own source flags as weak. C-grade
  candidates are guidance; they are never promoted and never admitted as A/B upstream
  candidates.

## Gate execution states

Stage attribution records the responsible gate's execution as one of:

- **ran** — positive evidence the gate executed (a review record, finding IDs, a
  resolution commit citing them);
- **skipped** — positive evidence it did not run;
- **unknown** — no durable record either way. Absence of a record is never recorded
  as skipped.

## Analyze report sections, in order

1. **Header** — the pinned corpus (exact commit range, PR list, feature directory
   and task IDs, or quick pool and `Q-`/`T-` IDs), date window, evidence sources available, evidence sources absent or
   unavailable.
2. **Inventory** — one row per unit of work: ID or PR, what it was, review history
   (rounds, finding IDs, or clean pass), examination depth. The four depths:
   `verified deep` — the unit's record read in full plus two or more independent
   verifications performed this run (diff read, targeted grep, cross-source
   match); `verified` — record read in full plus one verification; `skimmed` —
   record read partially or through search, no verification; `commit-record
only` — headline and metadata only.
3. **Case studies** — the strongest incidents, written against the evidence: what the
   record claims, what the evidence shows, verbatim quotes with their locators, and
   the full incident record for each.
4. **Lesson candidates** — one row per candidate:
   `L-NNN | rule statement | root incidents | grade | stage + gate state | primary tier | secondary action`.
   The stage cell names the gate that should have caught the incident with its
   execution state, and — when a later gate did catch it — which gate caught it;
   the catch location is evidence about the loop, not only the miss.
   `secondary action` is empty unless another owner has a distinct response.
   Structural findings — observations about the process's design that no single
   rule fixes — follow the table as prose with their own `S-NNN` IDs, citable
   like lessons.
5. **Proposed standing rules** — for each tier-1 candidate that passed the promotion
   gate, the exact one-line `AGENTS.md` text, ending with its citation. State the
   deletion-test argument in one sentence per rule.
6. **User-owned proposals** — tier-2 candidates: the target artifact and the proposed
   change, with `valcraft:hone` named as the application step.
7. **Upstream candidates** — tier-3 candidates, each with its attribution argument:
   the skill step or rule at fault, the direct run evidence identifying the invoked
   skill revision or instruction, the causes ruled out (user code, project contract,
   configuration, harness), and the portability argument. A git-only attribution is a
   C-grade hypothesis and says so. Include the submit-upstream suggestion only for
   A-grade candidates corroborated across multiple analyze reports.
8. **Not examined** — what the run did not open or verify: units at `skimmed` or
   `commit-record only` depth, absent evidence sources, unread transcripts. Name them
   specifically.

## Synthesis report sections, in order

1. **Header** — the source analyze reports, and any prior synthesis superseded.
2. **Root-incident collapse** — citations and reports identified as deriving from the
   same root incident, listed by shared key, so the grading below is auditable.
3. **Themes** — merged candidates, strongest evidence first. Each theme carries its
   own `L-NNN`, the merged rule statement, the re-graded evidence level, and every
   contributing `<report>, L-NNN`.
4. **Tensions and contradictions** — tensions: both candidates stand, with the
   boundary between their domains; contradictions: the resolution and which evidence
   decided it, or an explicit `unresolved` with what would settle it.
5. **Routing** — the merged themes routed through the three tiers, in the same shapes
   as analyze sections 5–7, plus proposed retirements: promoted standing rules no
   surviving evidence supports.
6. **Not examined** — source reports not fully processed, and corpora deliberately
   not re-opened.

## Standing rules in AGENTS.md

The promotion target is a `## Standing rules` section in the project's root
`AGENTS.md`, created by the first accepted promotion. One line per rule, each ending
with its citation:

```markdown
## Standing rules

- Normalize input first, then validate the result, never the reverse.
  (docs/retro/2026-08-20-001-analyze-003-search.md, L-002)
```

Keep the section small enough to read: propose a merge or retirement when rules
overlap, and retire through a later report's routing section, never by silent
deletion.
