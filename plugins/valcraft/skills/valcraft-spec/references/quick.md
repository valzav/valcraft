# Quick tasks

A quick task is a change too small for a feature triplet but still delivered through the working loop. It is one file, `specs/quick/<NNN>-<slug>.md`, from `../templates/quick.md`: frontmatter `id: Q-NNN`, then `Sources`, `Requirements` (`FR-` and `AC-`), `Approach`, and `Tasks` (checkbox `QT-` items). Spec owns this complete contract.

## Reservation and routing

`specs/quick/` is reserved for quick tasks. It is never a feature candidate and never contains `spec.md`, `design.md`, or `tasks.md`.

A change requiring several phases, a separate design artifact, a tracker issue hierarchy, or several independently reviewable areas is a feature. A quick task is a change whose requirements a few-line approach fully specifies, not merely summarizes. Honor an operator-selected shape after stating a clear mismatch. Otherwise propose the shape and wait when attended; bind and record the proposal when unattended. When one source contains independently valuable changes, ask the operator to select one.

## Identity and allocation

- The filename is `<NNN>-<slug>.md`: at least three decimal digits, then a slug matching `[a-z0-9]+(?:-[a-z0-9]+)*`.
- Frontmatter holds exactly one `id: Q-NNN` whose digits equal the filename.
- Allocate the greatest valid number in `specs/quick/` plus one, padded to three digits; use `001` when the directory is absent or empty. Re-run identity and collision checks immediately before writing. Never reuse a gap or append a suffix.
- `FR-`, `AC-`, and `QT-` IDs restart per quick file. A task ID is `QT-XXX`, with at least three digits. `Q-NNN` qualifies it; the canonical identity in assignments, branches, reviews, and reports is `Q-007 QT-001`.
- `T-XXX` is feature-only. A quick file containing a `T-` task, mixed prefixes, a malformed task ID, or a wrong-prefix dependency is invalid. A feature `tasks.md` containing `QT-XXX` is invalid. Stop before selection or work. Never map legacy syntax.
- A local dependency is exactly `blocked by QT-XXX` and resolves in the current file. A cross-file dependency is exactly `blocked by Q-NNN QT-XXX`. The file and task must exist. Dependency status is the referenced checkbox.
- A bare `Q-NNN` selects that file's first unchecked `QT-` in file order whose dependencies are checked. A bare `QT-XXX` resolves only when enumeration finds one matching valid quick file. A bare `T-XXX` searches feature tasks only. Zero or several matches stop.
- A file with no eligible task resolves to nothing. Do not pick a blocked or checked task.

Derive a task-delivery branch as `feat/q007-qt001-<slug>` and a logical worker or report identity as `Q007-QT001`, preserving every digit. That later task-delivery identity is separate from Spec's feature-contract delivery branch.

## Source and contents

Apply `feature-contract.md` source trust and provenance rules. A quick task also accepts `operator request, <YYYY-MM-DD>` when the request arrived as a message with no document. Keep exactly one source item.

State the required behavior in `Requirements`, with at least one observable `AC-`. State a correction of statements the change makes false as `feature-contract.md` requires: an open obligation with the search that finds them, and the criterion written against the search result. In `Approach`, state how the change will produce that behavior and what stays untouched. In `Verification`, design one `Test strategy` entry per `AC-`, as `feature-contract.md` defines the entry, with `TS-` IDs that restart per quick file. The entry's failing input must be constructible at the head of the `QT-` task that verifies the criterion; the criterion's entry is that task's check, so task lines carry no check ID. Do not copy mutable environment, deployment, or managed-service status. Link to `docs/status.md` when an observation matters; the snapshot never defines target behavior, acceptance criteria, task state, or authority.

Use one or a few concrete checkbox `QT-` tasks. Preserve supported source requirements. Record assumptions and open questions instead of inventing behavior. Quick-task plan names remain semantic; never add `quick` solely because the source is a quick task.

## Tracking and readiness

Quick tasks track locally in every project tracker mode. Their checkboxes are task status and git is the only tracker. A quick file has no `spec_issue`, issue, label, hierarchy, dependency projection, or closure batch. Do not inspect or mutate GitHub for a quick task. `quick_tracker` is reserved for a future contract; until then, `local` is its only valid value.

A quick task is implementation-ready when:

- `Requirements` has project-specific content and at least one observable `AC-`;
- `Approach` states the intended behavior and mechanism in the file's own words;
- `Verification` has one complete `Test strategy` entry per `AC-`, each with a failing input constructible at the head of the verifying `QT-` task;
- `Tasks` contains at least one valid `QT-` item; and
- no assumption or open question can change behavior or an acceptance criterion unless the operator explicitly accepted it.

An unready quick task reports the blocking section or question. A task closes only when its checkbox becomes `- [x] QT-XXX` in a reviewed change that cites the canonical identity. A quick file is done when every task is checked. Quick work has no per-file retrospective; retrospective analysis may use `specs/quick/` as a corpus.
