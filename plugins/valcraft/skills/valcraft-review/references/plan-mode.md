# Plan-mode review checks

## Pin the plan target

Bind the review to a repository-relative plan or feature-artifact path and one full commit SHA before reading content. When the caller supplies both, verify that the commit exists and contains that path. When the caller supplies only a current tracked path, resolve `HEAD^{commit}` and require that path to have no staged, unstaged, or untracked change. Record the resulting path and full commit under `Mode and change class`.

A gitignored retrospective report under `docs/.retro/` has no commit: pin it by absolute path and the SHA-256 of its content, hash the file on disk before reading it, and name that pair as the covered target.

Read the blob at the pinned commit, or the file at the pinned hash. A newer commit at the same path is not covered; name it under `Not examined`. If the supplied target and observed blob, commit, or content hash disagree, stop with `review_target_mismatch`. If the path or commit cannot be resolved, stop with `review_blocked`. Never infer coverage from a path, branch name, previous verdict, or mutable working tree.

## Review the plan

- Cross-check the authorities against each other. A plan can agree with a spec and design that already contradict. Apply the precedence in `../SKILL.md` and report a same-level conflict it cannot resolve.
- Enumerate every shape named by each claimed requirement and match it to verification. The simplest case does not cover the list.
- Separate plan assertions from assumptions about current state. Require a live check for fixture, data, or environment assumptions.
- For every invariant, explain how its test could still pass if the property were false. Check ordering, state, and scheduling dependencies.
- Reject textual delimiters as containment for untrusted content that can reproduce the marker. Require structural encoding at the plan boundary.
- Trace each proposed failure through the actual dispatcher or handler before accepting its claimed outcome.
- Reproduce a runtime-behavior claim by running that behavior. A reading of source or a numeric model is inference: label it as inference, and do not let it close a question that execution can settle.
- Accept a task plan's citation of a reviewed `Test strategy` entry without deriving the check again. Review what the plan adds to or changes from that entry.
- Reproduce mechanism claims against the exact tool or library version. Mutable documentation is not evidence. A mechanism-dependent accepted ADR without evidence is a finding; a conceptual ADR needs no Verification section.
- Assess a configured value's necessity separately from its authority. A governed conflict is a finding. A necessary ungoverned value is implementation discretion whose behavior and evidence still require review.
- Compare proposed work with goals and non-goals. Work no requirement asks for is scope creep.
- When the plan declares an exclusive scope, resolve every git-owned document the change makes contradictory by the contract it describes, not by searching for a changed identifier; a document can describe the same shape in prose without naming the symbol. Report an omitted document as a material finding.
- Route task-plan findings to Draft. Route feature and quick-artifact findings to Spec. Review never revises the target.

For a feature spec, verify that directory number equals frontmatter `id`, `Sources` contains exactly one canonical entry, and `spec_issue` matches tracker mode.

For feature `tasks.md`, require every task to use `T-XXX`. Map every declared `FR-`, `AC-`, `NFR-`, and `BR-` to a verifying task. Check ownership of every substantive acceptance-criterion clause, including each enumerated surface or behavior; an ID appearing in a task is insufficient. Resolve every `blocked by T-XXX`. Report wrong prefixes, missing dependencies, and uncovered requirements as material findings. Apply `feature-contract.md`'s sizing rule: report as material findings neighboring tasks that share a subsystem and raise no separate review question with no stated reason for the split, and a task that only verifies behavior other tasks build.

When the assignment names Spec-owned R-IDs resolved on the task branch, pin the triplet blobs at the same full commit as the plan and re-run each of those R-IDs against them. Verify Spec's reported scope test against the predecessor-to-head diff using `feature-contract.md`'s `Amendment scope`; an out-of-scope hunk is a material finding owned by Spec. This closure check is the review of the amendment; no separate Spec Review runs.

When `design.md` and `tasks.md` both exist, apply `feature-contract.md`'s complete implementation-readiness gate. Apply the substantive checks above to the whole triplet: independently verify the existing-code assumptions that determine its design and cross-check its behavior against the spec and task ownership. Use the recorded baseline and evidence as locators, not as a substitute for reproduction. Do not pass an unverified consequential claim by deferring it to a later task review. Proposed behavior still belongs to implementation; do not require it to exist at the baseline.

Judge the design's `Test strategy` once, here. Require an entry for each applicable acceptance criterion and invariant with all five fields. For each entry, decide whether the named check could pass with the guarded defect present and whether the observation method can record that defect class. Derive the cited criterion's domain yourself from its words and the design's formulas, then compare it with the entry's stated domain and covering method. An entry whose check omits a population, quantifier, or free variable of that domain, or whose covering method does not reach it, is a material finding owned by Spec. A sweep or case list over a continuous domain with no derivation of where the extrema lie and no bound between cases is such a finding. When the design gives a formula, reproduce the gap with a scratch computation. For each verifiable obligation a task line assigns, require a discriminating check that the owning task lists and can run at its own head. A missing one is a material finding owned by Spec, even when a later task's entry guards the same defect. Require the adversarial cases for each interaction or interface, and the recorded verification route when a criterion needs an observation tool that a worker must drive. An entry whose observation method names an operator's perception, an attended viewing session, or any judgment no worker can make through the recorded route is a material finding owned by Spec. A headed session a worker drives and observes through the verified route is a worker observation. For each entry that observes through the recorded route, confirm that the route's recorded proof covers the event class the entry relies on, counting every kind of entry the criterion's surface shows. An entry that relies on a class with no planted-instance proof is a material finding owned by Spec.

For a retrospective report under `docs/.retro/`, apply Temper's `report-format.md` and `process.md` as the governing contract.

- Require the mode's sections, in that reference's order and shapes. A missing or empty required section is a material finding.
- Require every lesson incident to carry the six-field record and an A, B, or C grade. Verify each grade against the incidents the record itself cites: an A needs two independent root incidents, an uncorroborated self-report is C, and a gate with no durable evidence is `unknown`, never `skipped`. A grade the cited evidence does not support is a material finding.
- Verify the cited evidence exists and says what the record claims. Sample against the corpus the report names, and list what you did not open under `Not examined`.
- Require every candidate to carry exactly one primary tier, and check each promotion against `process.md`'s deletion gate. A promotion the gate rejects is a material finding.
- For a synthesis report, check the root-incident collapse before the grades that depend on it: derivative corroboration never upgrades a B to an A, and a contradiction must record its resolution and the deciding evidence or an explicit `unresolved`.
- Check `Operator selection` against the run: `none` when no proposal met the escalation test, `offered, awaiting selection` for an unattended run, and accepted or declined with an application step for every accepted item in an attended one. A proposal that met the test but is absent is a material finding.
- Require `Review target` to name the absolute report path, the content hash, and the described head, and require that pair to match the target you pinned.
- Report an applied proposal as a material finding. Temper proposes; applying is later reviewed work.

For `specs/quick/NNN-*.md`, apply Spec's `quick.md` full grammar: filename number, `id: Q-NNN`, one source, `QT-XXX` tasks, qualified dependencies, readiness, and AC coverage. Reject legacy, mixed, malformed, missing, or wrong-prefix identities before eligibility. Preserve a semantic plan type and slug; `quick` is not added solely for task shape.
