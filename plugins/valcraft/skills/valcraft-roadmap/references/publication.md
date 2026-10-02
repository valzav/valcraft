# Roadmap in git

`docs/roadmap.md` is a tracked project document. Prepare its changes on a dedicated documentation branch. The published view is the version on the project's integration branch; a prepared update does not replace it until the repository's normal publication process merges the change.

## Prepare locally

Resolve the canonical repository, integration ref, and exact base revision from the assignment or existing project conventions. A repository with a single local branch needs no remote lookup. An isolated worker's current branch is not automatically the integration ref. Report an ambiguous base as `target_unresolved`.

Record the canonical checkout's branch, HEAD, and working-tree state before writing. Preserve existing edits. If the checkout contains unexplained changes, or the roadmap has uncommitted edits, return `publication_blocked` with their paths. Never switch, reset, stash, or commit the delivery checkout to make room for a refresh.

Use an isolated worktree on a dedicated documentation branch, following the project's naming and worktree conventions. Put a new worktree outside the canonical checkout or in an already-ignored worktree directory. Do not add ignore rules. The skill may create and commit this local branch; it never adds the roadmap to a task branch or changes a reviewed head.

When the caller supplies a previous pending Roadmap report, resolve its exact branch, commit, and worktree before reusing them. Reuse only attributable roadmap work with no unrelated changes. Reconcile a newer integration base by a normal merge that preserves history. Preserve both published and pending manual edits; an unresolved conflict returns `publication_blocked`. Never amend a reviewed or published commit, force-update a ref, or discard a pending candidate. Without an attributable candidate, create a fresh branch rather than taking over an arbitrary documentation branch.

Read accepted scope from the resolved integration revision and attribute any additional progress evidence to its source revision or observation. Keep source links valid from `docs/roadmap.md` in the candidate. Name an unavailable source or a source present only on another branch with its exact locator instead of writing a broken relative link or copying its content into the publication branch.

Write and verify the roadmap in the isolated worktree. Commit only `docs/roadmap.md`; confirm the complete candidate diff against the integration base contains no other path. Leave other project artifacts and configuration unchanged. A source conflict or failed write preserves the candidate for inspection. Verify the canonical checkout's branch, HEAD, and working-tree state are unchanged before returning.

If the supported view and its freshness evidence are unchanged, return the existing artifact without a content commit. Retain a prepared branch and worktree while its update is pending publication.

## Publication handoff

Report the canonical target, candidate path, integration ref and base SHA, documentation branch, candidate commit SHA, content hash, and disposition. Use `prepared — publication pending` for a committed candidate and `unchanged` when no update is needed. If an unchanged artifact is already a pending candidate, preserve its pending disposition. Never describe a local candidate as an updated published roadmap.

Roadmap prepares the local change. Push, PR creation, and merge belong to the repository's normal documentation publication workflow and require their own existing authority. A Foreman task's publication grant does not cover this documentation branch. Do not route a roadmap change through Land's task or spec-PR target kinds. Recheck the candidate against the latest accepted scope before a later publication; an older prepared view is only a dated snapshot.

Foreman can resume delivery after a prepared update. Publication pending is a visible artifact disposition, not a delivery blocker or evidence that the published roadmap is current.
