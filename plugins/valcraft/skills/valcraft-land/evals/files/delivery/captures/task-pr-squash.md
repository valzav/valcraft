# Task PR 42 at the reviewed head

- Repository: `example/reports`
- Remote: `origin` = `https://example.test/reports.git`
- Base: `main` at `1111111111111111111111111111111111111111`
- Head branch: `feat/f001-t002-normalize-headers`
- Current head: `2222222222222222222222222222222222222222`
- Title: `feat(F001 T-002): normalize export headers`
- State: open
- Merge method: squash
- Merging account: `maintainer`
- Task issue: 17, open, label `in-progress`
- Checks: `unit` passed on the current head

## Commits, in host order

### `1a1a1a1a1a1a1a1a1a1a1a1a1a1a1a1a1a1a1a1a`

Author: `Delivery Worker <worker@example.test>`

```text
feat(F001 T-002): normalize CSV header names

Lowercase each header and replace spaces with underscores (FR-002).
```

### `2222222222222222222222222222222222222222`

Author: `Delivery Worker <worker@example.test>`

```text
test(F001 T-002): cover headers with repeated spaces

A header with two spaces in a row becomes one underscore (AC-002).
```
