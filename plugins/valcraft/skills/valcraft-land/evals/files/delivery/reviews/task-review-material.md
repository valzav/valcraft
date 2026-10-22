# Captured task review

## Review report

### Mode and change class

Code mode: `example/reports` PR 42, base `main` at `1111111111111111111111111111111111111111`, head `feat/f001-t002-normalize-headers` at `3333333333333333333333333333333333333333`; change class code.

### Verdict

verdict: material findings; open: R-009:P2 valcraft-spec; covered: `example/reports` PR 42, base `main` at `1111111111111111111111111111111111111111`, head `feat/f001-t002-normalize-headers` at `3333333333333333333333333333333333333333`

### Findings

| R-ID | severity | claim | evidence | resolution |
| --- | --- | --- | --- | --- |
| R-009 | P2 | FR-002 says only "normalize", so AC-002 is the sole header rule, yet it names no rule for headers that differ only by case; the PR merges `Total` and `total` into one `total` column, which no clause permits or forbids | `specs/001-report-export/spec.md` FR-002 and AC-002; the PR's header normalization | open — valcraft-spec; second full round upheld it after Spec declined |

### Reproductions

Export a report with columns `Total` and `total` at `3333333333333333333333333333333333333333`: the CSV has one `total` column.

### Checks performed

Contract mapping and tests at `3333333333333333333333333333333333333333`.

### Not examined

Hosted merge permission.

Status: done
