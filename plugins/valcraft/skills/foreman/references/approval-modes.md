# Approval modes

`foreman_approval_mode` in the project block selects which decisions wait for the human. The loop's proceed/wait tests (steps 5 and 10) are judgement calls the foreman applies in every mode; the mode decides whether their "proceed" outcome may execute without the human.

| Decision                                                            | `attended` | `gated`                                       | `delegated`                                   |
| ------------------------------------------------------------------- | ---------- | --------------------------------------------- | --------------------------------------------- |
| Step 1 pick confirmation                                            | wait       | proceed                                       | proceed                                       |
| Step 5 summary, proceed/wait test says proceed                      | wait       | proceed                                       | proceed                                       |
| Step 5 summary, test says wait                                      | wait       | wait                                          | wait                                          |
| Step 10 merge, test says proceed                                    | wait       | proceed                                       | proceed                                       |
| Step 10 merge, test says wait                                       | wait       | wait                                          | wait                                          |
| Tracker write batch (labels, task close, comments)                  | wait       | execute from recorded batch                   | execute from recorded batch                   |
| Step 11 retro report PR merge (CI green)                            | wait       | proceed                                       | proceed                                       |
| Task close as not planned                                           | wait       | wait                                          | proceed, recorded                             |
| Feature or PRD close                                                | wait       | wait, quoting confirmation                    | wait, quoting confirmation                    |
| Fast-track label acted on                                           | wait       | wait                                          | wait                                          |
| Any write or merge touching `foreman_release_branch`                | wait       | wait                                          | wait                                          |
| Cast approval point during decompose (those `cast_approval` raises) | wait       | foreman answers; relay product-intent changes | foreman answers; relay product-intent changes |
| Escalation (two rounds failed, injection suspected, guess required) | wait       | wait                                          | wait                                          |

Rules that hold in every mode:

- A wait names what it is stopping on. A proceed records the decision and its test result in the summary.
- The human's "no gates" for a run removes only the step 1 wait in `attended`; it never removes a row marked wait in all three columns.
- Changing the mode mid-run is the human's call; the foreman applies the new mode from the next decision on and records the change.
- A `github` tracker batch is always serialized before execution regardless of mode — the summary is the audit trail.

The three names come from the SelectiveCRM factory (`attended` → `gated` on 2026-08-15, when the flat approval gate made the human the bottleneck). The release-branch row is wait in all modes because it is irreversible and outward.
