# Code-mode review checks

## Pin the code target

Record repository identity plus exact base and head before diffing:

- PR: recorded repository, PR identity, base ref and SHA, head ref and SHA.
- `A..B`: resolved full commits A and B.
- Branch: merge-base with the authoritative default branch and the branch's full tip commit.
- Bare base: merge-base with `HEAD` and full `HEAD` commit.
- Offline captured diff: its recorded repository and full base/head identities.

Resolve both commits, pin `git diff <base>...<head>`, and capture `git log <base>..<head> --oneline`. Re-read the selected PR or branch head before reporting. Any change is `review_target_mismatch`; do not transfer the verdict to the new head.

An unresolvable target or empty diff is `review_blocked`. An uncommitted working tree may be inspected to return findings, but it cannot receive `pass` because it has no durable exact code head. Disclose untracked paths and return blocked when no material finding already determines the result.

Classify the pinned file list as **docs** when it touches only documentation, **config** when it touches only configuration, CI, or dependency manifests, and **code** otherwise. Classification changes no review policy.

## Map the contract

Feature commits cite the canonical `FEAT-NNN/T-XXX`, an `FR-`, or a plan `R-` ID. Validate the governing feature `tasks.md` before mapping and require `T-XXX` there. Quick commits cite `Q-NNN/QT-XXX`; resolve the exact pair and dependencies through `quick.md`. Apply identity validation only to commits that contribute to the pinned review target. Earlier history may establish context, but it is not current work. Within the target, reject missing, mixed, malformed, or wrong-prefix identity instead of mapping it to a valid one. A change governed by no task or requirement is a finding. A task PR may change `spec.md`, `design.md`, `tasks.md`, or a quick file only in a Spec-owned commit whose triplet blobs the passed plan Review pinned and whose identity and R-IDs the PR body names, or in the task's own completion transition below; any other triplet change in a task PR is a finding.

Read the tracker mode from the committed `.valcraft/config.yaml`. In `local` mode for a feature task, and in every mode for a quick task, the head must carry exactly the selected task's unchecked-to-checked transition in `tasks.md` or the quick file, committed by Forge. A missing transition, a transition of another task, or any other change to the task file in that commit is a material finding owned by Forge. In `github` mode, a feature task PR that changes its task's checkbox is a material finding owned by Forge.

Require the passed task plan path and exact Review-passed plan commit for a non-trivial implementation. A code finding within that plan resolves in Forge. A finding that changes product scope, acceptance behavior, or the plan's declared approach resolves in Draft. A `Test strategy` entry that no worker can observe through the recorded route resolves in Spec. Review invokes no owner.

## Review the change

- Attack user-controlled prompt, path, filename, and identifier inputs with the smallest delimiter, traversal, absolute-path, newline, empty, and whitespace cases that apply.
- Revert a claimed fix in a disposable worktree and prove its regression test fails before the change. A test green on both sides is vacuous.
- Compare whole values for "nothing else changed" claims.
- Hunt success paths that return empty, partial, or default output and then replace real data.
- Combine orthogonal input dimensions; independent cases do not prove their intersections.
- Re-run the load-bearing verification and read raw output rather than trusting a wrapper or CI mark.
- Observe UI criteria yourself through the recorded verification route, headless when the route allows it. Never return `review_blocked` to obtain an operator's perception; a criterion whose design entry cannot be observed through the route is a material finding owned by Spec.
- Inspect every immutable pinned action's source and defaults at that revision.
- Exercise every failure mode named by a finding before closure.
- Report behavior no requirement requests as scope creep.
- Check repository change discipline: affected contracts and docs move with the code, commit subjects cite owned IDs, and generated files are not hand-edited.
- Report delivery state that the change writes into a git-owned document, as `feature-contract.md`'s delivery-state rule defines it, as a material finding owned by the producer of the commit that writes it.

Every pass or material-findings report names the exact repository, base ref and SHA, head ref and SHA, and PR identity or `none`. A later head requires a fresh Review.
