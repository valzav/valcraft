# Code-mode review checks

Read this reference for a diff, PR, branch, commit range, or working-tree review.

## Pin the target

Normalize the target to a pinned base and head before diffing: a PR → its recorded base and head; a commit range `A..B` → A and B; a branch under review → its merge-base with the default branch, and the branch tip; a bare base ref → its merge-base with `HEAD`, and `HEAD`. Verify both resolve (`git rev-parse <base> <head>`), pin the diff (`git diff <base>...<head>`), and capture the commit list (`git log <base>..<head> --oneline`). When the target is the current working tree, diff the base against the tree itself (`git diff <base>`) and disclose untracked paths (`git status --porcelain`). An unresolvable target or an empty diff is a **blocked** verdict, not a mid-review failure.

Map the diff to its governing contract. Feature commits cite `T-`/`FR-`/`R-` IDs and
feature `tasks.md` maps T-IDs. Quick commits cite `Q-NNN QT-XXX`; resolve that exact pair
to `specs/quick/NNN-*.md`, validate the file and dependencies through `quick.md`, and
never interpret historical `Q-NNN T-XXX` as current work. A missing Q file or QT-ID,
legacy or mixed prefix, malformed identity, wrong prefix, `QT-XXX` in feature tasks, or
change governed by no task or requirement is a finding.

## Review the change

- **Attack every user-controlled string** that reaches a prompt, path, filename, or generated identifier: construct the smallest adversarial input — an embedded delimiter, `../`, a leading `/`, a newline, an empty or whitespace-only value — and check whether the code rejects it or is corrupted by it.
- **Revert the fix.** When a change ships with a regression test, confirm the test goes red against the pre-change code. Run this in a disposable `git worktree` pinned to the reviewed revisions — review is report-only and never mutates the target checkout. A test green on both sides is vacuous, and vacuous regression tests recur.
- **"Nothing else changed" tests must compare whole rows or values**, not field subsets or containment — an omitted field can change silently behind a passing partial comparison.
- **Hunt the silent-replacement pattern**: an operation whose no-error path can return empty, partial, or default output, then used to overwrite or stand in for real content. Happy-path tests do not catch it; read the control flow for this shape deliberately.
- **Check combination coverage**: input dimensions tested only independently, never together, are a blind spot regardless of the suite's pass count.
- **Re-run the verification the change leans on hardest yourself.** Local wrappers can swallow a real failure and report clean; a CI check mark is a conclusion, not evidence — read the log content for the load-bearing lines (what loaded, what ran, the counts).
- **Hunt scope creep**: behavior in the diff that no requirement asks for, including speculative generality — abstraction, parameters, or hooks for needs no requirement states. Cite the non-goal it violates or the requirement it lacks.
- **Check Cast's change discipline**: affected specs, ADRs, and docs move in the same change as the code; commit subjects cite the IDs they implement or resolve; generated files are not edited by hand. Cite the violated `AGENTS.md` clause.
