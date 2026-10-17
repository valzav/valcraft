## Spec report

### Source

Assignment ra-spec-d000: resolve R-002 from .valcraft/foreman/run-amend-projection/plan-reviewer-F001-T002-d000.md.

### Artifact

- specs/001-invite-links/design.md — revised: TS-003 positive control now rejects a link used exactly at `expires_at`.
- specs/001-invite-links/tasks.md — revised: the T-002 task line names the boundary rejection.
- specs/001-invite-links/spec.md — unchanged.

### Readiness

Implementation-ready. The scope test selects the task branch: the amendment changes only T-002's own obligations, and T-002 is open.

### Workspace

Commit target: task branch. Canonical branch feat/f001-t002-expired-link-rejection. Physical branch none. Clean worktree after commit.

### Projection

- Prepared continuation only; tracker mutation authority was not granted.
- Target: github.com/example/loop-github. Projection-state revision: `sha256:4c1d9e0b7a3f5e2d8c6b1a0f9e8d7c6b5a4f3e2d1c0b9a8f7e6d5c4b3a2f1e0d`.
- Verified mappings: FEAT-001 → #40; T-001 → #41; T-002 → #42; T-003 → #43. No mapping, hierarchy, order, dependency, or label delta exists.
- Exact prepared operation set: update only issue #42's body to the revised T-002 text at artifact head 7777777777777777777777777777777777777777. Current body hash `sha256:1a2b3c4d5e6f708192a3b4c5d6e7f8091a2b3c4d5e6f708192a3b4c5d6e7f809`; prepared body hash `sha256:9f8e7d6c5b4a39281706f5e4d3c2b1a09f8e7d6c5b4a39281706f5e4d3c2b1a0`.

### Outward mutations

- Committed the two revised artifact paths on feat/f001-t002-expired-link-rejection at 7777777777777777777777777777777777777777.
- Revalidated the repository, remote, canonical ref at its bound observation 6666666666666666666666666666666666666666, ancestry, and clean worktree immediately before the push.
- Non-force pushed 7777777777777777777777777777777777777777 to refs/heads/feat/f001-t002-expired-link-rejection; the remote read-back matched.
- No spec PR was opened, because the commit target is the task branch. No tracker write was performed.

### Finding resolutions

| R-ID | Resolution |
| --- | --- |
| R-002 | TS-003 positive control and the T-002 task line now reject a link used exactly at `expires_at`. |

### Review target

specs/001-invite-links/design.md and specs/001-invite-links/tasks.md at 7777777777777777777777777777777777777777

### Land target

none

### Open questions

none

Status: done
