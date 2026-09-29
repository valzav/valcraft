## Review report

### Mode and change class

plan; class: feature contract; target specs/001-invite-links/spec.md, specs/001-invite-links/design.md, and specs/001-invite-links/tasks.md at 5e3900d6437cfa4ed97be7b32b5670c9671799da on `dev`

### Verdict

verdict: pass; open: none; covered: specs/001-invite-links/{spec,design,tasks}.md at 5e3900d6437cfa4ed97be7b32b5670c9671799da

The triplet meets `feature-contract.md`'s readiness rule. Every requirement and acceptance-criterion clause maps to a task and a `Test strategy` entry, and VB-001 reproduces at its cited baseline.

### Findings

none

### Reproductions

- VB-001: `git show c2585740b55c613149294af38eaf089d03637409:src/invites.py | grep -c "class Link\|LINK_LIFETIME = timedelta(days=7)\|def create_link\|_links\[link.token\]"` printed `4`.
- TS-001 positive control: `PYTHONPATH=src python3 -m unittest discover -s tests` at 5e3900d6437cfa4ed97be7b32b5670c9671799da printed `OK`.
- TS-001 failing input: with `LINK_LIFETIME = timedelta(days=6)` in a scratch copy, the same command printed `FAILED (failures=1)`.

### Checks performed

- Authority cross-check: product brief, spec, design, and tasks agree; no accepted ADR exists.
- Requirement coverage: FR-001 → T-001, T-003; FR-002 → T-002; FR-003 → T-001, T-002; AC-001 → T-001; AC-002 → T-002; AC-003 → T-002; AC-004 → T-003.
- Task obligations and check IDs: T-001 `Link` record and `create_link` → TS-001; T-002 unknown-token rejection → TS-003, expiry rejection → TS-002, single membership write → TS-003; T-003 admin CLI → TS-004.
- Invariants: rejection before any write (design `Failure handling`) → TS-002, TS-003.
- Failing inputs constructible at each task's head: TS-001 at T-001; TS-002 and TS-003 at T-002; TS-004 at T-003.
- Task identities and dependencies: T-001 through T-003 use `T-XXX`; `blocked by T-001` resolves.
- Open questions and assumptions: none.

### Not examined

none

Status: done
