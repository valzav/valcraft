## Spec report

### Source

Assignment re-spec-d000: new feature contract from docs/requirements/transcript-export.md.

### Artifact

None written. The design cannot fix the export's filtering until the question below is answered.

### Readiness

Not ready: one owner decision is open.

### Workspace

No commit. Clean worktree on dev.

### Projection

none

### Outward mutations

none

### Finding resolutions

none

### Review target

none

### Land target

none

### Open questions

The records team has approved exporting transcripts, so the only open choice is how an export treats `restricted` transcripts: include them only for records-team members, or exclude them from every export. The requirement "only transcripts the requesting researcher may open" fits both readings. A shared access check is planned separately as Q-006/QT-001 in specs/quick/006-access-check.md.

Status: question: owner_decision_required — whether an export includes restricted transcripts for records-team members or excludes them for everyone
