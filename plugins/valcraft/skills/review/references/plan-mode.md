# Plan-mode review checks

Read this reference for a plan, spec, design, or tasks review. Apply every check that the target type makes relevant.

- **Cross-check the authorities against each other**, not only against the plan: a plan can sit consistently on a spec and a design that already contradict each other, or misattribute an ADR. Resolve contradictions by the precedence order in `../SKILL.md`; report an unresolved contradiction between authorities as its own finding.
- **For every requirement the plan claims to close, check its verification covers every shape the requirement names** — enumerate the requirement's own listed cases and match each to a test; the plan will otherwise verify the simplest one.
- **Separate what the plan asserts from what it assumes about current system state** (fixture contents, "starts empty", "no prior rows"). Route assumptions to a live-data check demand, not to stronger prose — a hardened assertion on a false premise still fails.
- **For every asserted invariant, trace "why would this test still pass if the property were false"** — reason through the scheduling/ordering/state contract the invariant depends on.
- **Wherever the plan frames untrusted content with a boundary marker** — a delimiter string, a fixed prefix or suffix, a path root — ask whether content from that source can reproduce the boundary itself. "We'll validate later" does not close the question; the answer is a structural encoding decision made now.
- **Trace each new failure mode through the actual dispatcher or handler code** before accepting the plan's prose about the outcome. "This becomes a skip" may in fact mark the item durably handled and lose it permanently.
- **Reproduce every concrete mechanism claim the plan relies on** against the exact tool or library version and record the command and observed result; mutable documentation is not evidence. A mechanism-dependent ADR without that evidence remains proposed or provisional, and an accepted one is a finding. A conceptual ADR needs no Verification section.
- **For every configured value, assess necessity separately from authority.** Check the selected value against every applicable ADR, spec, repository instruction, and operator instruction. A governed conflict is a finding even when some value is necessary. A necessary value that no authority governs is implementation discretion, not a missing-authority defect; still assess whether its behavior and evidence meet the contract.
- **Compare the plan's proposed work against the spec's goals and non-goals.** Work no requirement asks for is scope creep, and it hides best in a plan that is otherwise faithful.
- **When the target is a feature spec, check its structural contract from `spec-intake.md`**: the directory number matches the frontmatter `id`, the `Sources` section holds exactly one canonical entry, and the `spec_issue` mapping matches the tracker mode.
- **When the target is feature `tasks.md`, require every task to use `T-XXX`**;
  `QT-XXX` is a material finding before readiness. Map every `FR-` and `AC-` — and
  every `NFR-` and `BR-` the spec declares — to at least one task that verifies it,
  and check each `blocked by T-XXX` names an existing task. An unverified requirement
  is a gap regardless of how complete the task list looks.
- **When the target completes the spec triplet** (`design.md` and `tasks.md` both exist), check the implementation-readiness gate defined in `spec-intake.md` and report a failed gate as a material finding citing the readiness contract.
- **When the target is a quick task file** (`specs/quick/NNN-*.md`), check
  `quick.md`'s full grammar: filename number equals `id: Q-NNN`, one `Sources` entry,
  every task is `QT-XXX`, and dependencies are local `blocked by QT-XXX` or qualified
  `blocked by Q-NNN QT-XXX`. Resolve every dependency and report a missing file or task,
  legacy `T-XXX`, mixed or malformed prefix, wrong-prefix dependency, or feature
  `tasks.md` containing `QT-XXX` as a material finding before eligibility. Apply the
  readiness rule separately. Map every `AC-` to at least one task; an unverified
  criterion is a coverage gap, not a readiness failure. Quick-task plans keep semantic
  types and slugs; `quick` added solely for task shape is a finding.
