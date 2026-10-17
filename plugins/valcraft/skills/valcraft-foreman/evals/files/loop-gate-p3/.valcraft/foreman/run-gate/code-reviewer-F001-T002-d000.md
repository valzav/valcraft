## Review report

### Mode and change class

code; class: code; target PR #12 head 2222222222222222222222222222222222222222

### Verdict

verdict: pass; open: none; covered: PR #12 head 2222222222222222222222222222222222222222

### Findings

| R-ID | severity | claim | evidence | resolution |
| --- | --- | --- | --- | --- |
| R-003 | P3 | `use_link` repeats the expiry comparison in a helper and in the caller | `src/invites.py` `use_link` | valcraft-forge: informational; no change required |

### Reproductions

none

### Checks performed

target pinned; revert-the-fix in a disposable worktree (`test_expired_rejects` red on base); scope

### Not examined

UI; none in this task

Status: done
