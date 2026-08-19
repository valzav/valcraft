# Plan-mode review checks

## Pin the plan target

Bind the review to a repository-relative plan or feature-artifact path and one
full commit SHA before reading content. When the caller supplies both, verify
that the commit exists and contains that path. When the caller supplies only a
current tracked path, resolve `HEAD^{commit}` and require that path to have no
staged, unstaged, or untracked change. Record the resulting path and full commit
under `Mode and change class`.

Read the blob at the pinned commit. A newer commit at the same path is not
covered; name it under `Not examined`. If the supplied target and observed blob
or commit disagree, stop with `review_target_mismatch`. If the path or commit
cannot be resolved, stop with `review_blocked`. Never infer coverage from a path,
branch name, previous verdict, or mutable working tree.

## Review the plan

- Cross-check the authorities against each other. A plan can agree with a spec
  and design that already contradict. Apply the precedence in `../SKILL.md` and
  report a same-level conflict it cannot resolve.
- Enumerate every shape named by each claimed requirement and match it to
  verification. The simplest case does not cover the list.
- Separate plan assertions from assumptions about current state. Require a live
  check for fixture, data, or environment assumptions.
- For every invariant, explain how its test could still pass if the property
  were false. Check ordering, state, and scheduling dependencies.
- Reject textual delimiters as containment for untrusted content that can
  reproduce the marker. Require structural encoding at the plan boundary.
- Trace each proposed failure through the actual dispatcher or handler before
  accepting its claimed outcome.
- Reproduce mechanism claims against the exact tool or library version. Mutable
  documentation is not evidence. A mechanism-dependent accepted ADR without
  evidence is a finding; a conceptual ADR needs no Verification section.
- Assess a configured value's necessity separately from its authority. A
  governed conflict is a finding. A necessary ungoverned value is implementation
  discretion whose behavior and evidence still require review.
- Compare proposed work with goals and non-goals. Work no requirement asks for
  is scope creep.
- Route task-plan findings to Draft. Route feature and quick-artifact findings
  to Spec. Review never revises the target.

For a feature spec, verify that directory number equals frontmatter `id`,
`Sources` contains exactly one canonical entry, and `spec_issue` matches tracker
mode.

For feature `tasks.md`, require every task to use `T-XXX`. Map every declared
`FR-`, `AC-`, `NFR-`, and `BR-` to a verifying task. Resolve every
`blocked by T-XXX`. Report wrong prefixes, missing dependencies, and uncovered
requirements as material findings.

When `design.md` and `tasks.md` both exist, apply `feature-contract.md`'s complete
implementation-readiness gate.

For `specs/quick/NNN-*.md`, apply Spec's `quick.md` full grammar: filename number,
`id: Q-NNN`, one source, `QT-XXX` tasks, qualified dependencies, readiness, and
AC coverage. Reject legacy, mixed, malformed, missing, or wrong-prefix
identities before eligibility. Preserve a semantic plan type and slug; `quick`
is not added solely for task shape.
