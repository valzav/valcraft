# Spec PR 43 at the reviewed head

- Repository: `example/reports`
- Remote: `origin` = `https://example.test/reports.git`
- Base: `main` at `1111111111111111111111111111111111111111`
- Head branch: `spec/f001-amend-1111111`
- Current head: `4444444444444444444444444444444444444444`
- Title: `spec(F001): state the header rule for repeated spaces`
- State: open
- Merge method: squash
- Merging account: `maintainer`
- Changed files: `specs/001-report-export/spec.md`
- Checks: `unit` passed on the current head

## Commits, in host order

### `3a3a3a3a3a3a3a3a3a3a3a3a3a3a3a3a3a3a3a3a`

Author: `Delivery Worker <worker@example.test>`

```text
spec(F001): state the header rule for repeated spaces

FR-002 now says that repeated spaces in a header become one underscore.
```

### `4444444444444444444444444444444444444444`

Author: `Delivery Worker <worker@example.test>`

```text
spec(F001): resolve R-004 in AC-002

AC-002 names a header with two spaces in a row as its example.
```
