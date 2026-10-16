# Task PR heads and completion transitions

Each case names the head the passing code Review covers and the current PR head.

## Feature task F001 T-002

### Case A

The current PR head equals the reviewed head. The PR's delta against `main` includes this change to `specs/001-neutral/tasks.md` and no other change to that file:

```diff
-- [ ] T-002 Normalize headers. Covers FR-002 and AC-002.
+- [x] T-002 Normalize headers. Covers FR-002 and AC-002.
```

### Case B

The current PR head equals the reviewed head. The PR's delta against `main` changes no line of `specs/001-neutral/tasks.md`.

### Case C

The reviewed head's delta changes no line of `specs/001-neutral/tasks.md`. The current PR head is one commit on the reviewed head, pushed after Review, and that commit's whole delta is:

```diff
-- [ ] T-002 Normalize headers. Covers FR-002 and AC-002.
+- [x] T-002 Normalize headers. Covers FR-002 and AC-002.
```

## Quick task Q-007 QT-001

### Case A

The current PR head equals the reviewed head. The PR's delta against `main` includes this change to the quick file and no other change to that file:

```diff
-- [ ] QT-001 Normalize headers. Covers FR-001 and AC-001.
+- [x] QT-001 Normalize headers. Covers FR-001 and AC-001.
```

### Case B

The current PR head equals the reviewed head. The PR's delta against `main` changes no line of the quick file.

### Case C

The reviewed head's delta changes no line of the quick file. The current PR head is one commit on the reviewed head, pushed after Review, and that commit's whole delta is:

```diff
-- [ ] QT-001 Normalize headers. Covers FR-001 and AC-001.
+- [x] QT-001 Normalize headers. Covers FR-001 and AC-001.
```
