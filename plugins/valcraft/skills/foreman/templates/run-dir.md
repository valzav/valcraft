# Run directory

One directory per foreman run, inside the foreman's checkout, gitignored:

```text
.foreman/<run-id>/
├── state.md                     # picked task, current step, held tasks, mode changes
├── workers.md                   # <role>-<F>-<T> → backend handle (session id, agent name)
├── planner-F004-T012.md         # one report file per role per task; appended across rounds
├── reviewer-1-F004-T012.md
├── worker-F004-T012.md
├── reviewer-2-F004-T012.md
└── planner-prd225.md            # decompose reports use the source as the task part
```

- `<run-id>`: `YYYY-MM-DD-NNN`, `NNN` the next free number for that date in `.foreman/`. The human may name a run instead.
- The foreman writes `state.md` and `workers.md`; workers write only their own report file, by the absolute path the envelope names.
- The directory is the run's audit trail and the resume source: step 0 reads it before the tracker.
- Nothing here is committed. A report is never pasted into a commit, PR body, or issue; the durable record is Cast's — remediation plans in `docs/plans/` and resolution commits citing R-IDs.
