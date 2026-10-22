## Review report

### Mode and change class

code; class: code; target PR #16 head 4444444444444444444444444444444444444444

### Verdict

verdict: material findings; open: R-005:P2 valcraft-spec; covered: PR #16 head 4444444444444444444444444444444444444444

### Findings

| R-ID | severity | claim | evidence | resolution |
| --- | --- | --- | --- | --- |
| R-005 | P2 | The feature contract states no behavior for an unknown token, so the PR's `UnknownInvite` rejection has no clause to verify against | spec FR-002 covers a valid link and AC-002 an expired one; design `use_link` names only `ExpiredInvite`; `src/invites.py` `use_link` raises `UnknownInvite` | open — valcraft-spec |

### Reproductions

Read spec FR-002, FR-003, AC-002 and design `use_link`; call `use_link("missing", now)` on the PR head: it raises `UnknownInvite` and writes no membership.

### Checks performed

target pinned; requirement coverage; revert-the-fix in a disposable worktree (`test_expired_rejects` red on base); scope

### Not examined

UI; none in this task

Status: done
