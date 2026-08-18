# Run directory

One directory per foreman run, inside the foreman's checkout, gitignored:

```text
.foreman/<run-id>/
├── state.md                     # picked task, current step, held tasks, mode changes
├── workers.md                   # canonical logical identity → physical backend handle
├── planner-F004-T012.md         # one report file per role per task; appended across rounds
├── reviewer-1-F004-T012.md
├── worker-F004-T012.md
├── reviewer-2-F004-T012.md
├── worker-Q007-QT001.md         # quick-task logical report name
├── temper-F004.md               # step 11, once per feature
└── planner-prd225.md            # decompose reports use the source as the task part
```

- `<run-id>`: `YYYY-MM-DD-NNN`, `NNN` the next free number for that date in `.foreman/`. The human may name a run instead; a name is valid only when it matches `^[A-Za-z0-9][A-Za-z0-9._-]*$` and is not `.` or `..` — no path separators, no traversal — so the run directory always resolves inside `.foreman/`. Reject any other name and ask for another. The run ID never supplies or freezes the date of a later artifact; `references/contracts.md`, "Artifact dates", resolves each artifact when it is created.
- The foreman writes `state.md` and `workers.md`. Each dispatch gets one workers row:
  role, canonical task identity, logical name, host, physical handle, and state. A Codex
  handle records both `task_name` and returned agent id. Keep prior rows when a one-shot
  worker respawns so every physical dispatch remains mapped to its logical identity.
  Record terminal evidence before marking a row done; absence from a live-only status
  result is not evidence. Workers write only their own logical report file, by the
  absolute path the envelope names.
- `state.md` is a run checkpoint, not a durable authority. Record the selected task and current step; pointers to the governing task, plan, reports, tracker or change request, and deferred decisions; the local and remote default-branch SHAs, their four-way synchronization classification, any explicit local-ahead push authority, and the reconciled SHA; the reviewer-covered SHA, each later PR head and exact delta disposition, every check-applicability source and probe, the final check classification, and the exact final SHA; attributed-context source and probe locators; recovery-inventory dispositions; and the resolved date plus authority for each dated artifact. Tie every synchronization, review, check, approval, and merge decision to its exact SHA. Preserve earlier checkpoints so a resume can identify the exact state that produced a decision.
- On resume, re-read every referenced git or tracker fact from its authoritative source. A `state.md` pointer or SHA identifies what to verify; it never overrides current git, the tracker, or a git-owned task contract. Record and reconcile any mismatch before advancing.
- The directory is the run's audit trail and the resume source: step 0 reads it before the tracker.
- Nothing here is committed. A report is never pasted into a commit, PR body, or issue; the durable record is Cast's — remediation plans in `docs/plans/` and resolution commits citing R-IDs.
