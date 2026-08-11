# Agent instructions

## Orientation

- `docs/` — product brief, working plans, architecture docs, ADRs.
- `specs/` — feature behavior (`spec.md`), technical design (`design.md`), ordered
  implementation tasks (`tasks.md`).
- `<source dir>` — application code. `<test dir>` — automated tests.

Read the docs relevant to your change before modifying code or specifications. On
conflict, accepted ADRs prevail, then `specs/`, then derived `docs/`. Do not invent
missing requirements — record assumptions and open questions in the relevant spec, and
consequential technical decisions as ADRs.

## Writing standard

Use these rules for documentation, specifications, ADRs, plans, code comments, reviews,
issues, commit messages, and PR text.

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

- Install: `<command>`
- Develop: `<command>`
- Test: `<command>`
- Lint: `<command>`
- Type check: `<command>`

## Architecture constraints

<Only real, binding constraints — 3 to 6 lines. Examples:>

- Business logic must not depend on UI components.
- Database access goes through <the established boundary>.
- Secrets are never committed; reference an external store.

## Change discipline

- Product intent lives in `spec.md`; implementation detail in `design.md`.
- Reference requirement and task IDs (`FR-`, `AC-`, `T-`) from commits and tests.
- Non-trivial work starts with a plan in `docs/plans/YYYY-MM-DD-NNN-<type>-<slug>-plan.md`.
- Update affected specs, ADRs, and docs in the same change as the code.
- Do not edit generated files by hand.

## Completion criteria

Before marking work complete:

1. Run tests, lint, and type check; report anything skipped or missing.
2. Add or update tests for changed behavior; verify the acceptance criteria touched.
3. Update affected specifications, designs, and ADRs.
4. Confirm no secret material was added.
