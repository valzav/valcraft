# Approval modes

An explicit valid `foreman_approval_mode` selects which decisions wait for the human. Missing means `unattended`. The loop's proceed/wait tests (steps 5 and 10) are judgement calls the foreman applies in every mode; the mode decides whether their "proceed" outcome may execute without the human. Cast resolves `cast_approval` independently; its missing-key default remains `attended`.

## What waits in each mode

| Decision                                                                 | `attended` | `unattended`                                  |
| ------------------------------------------------------------------------ | ---------- | --------------------------------------------- |
| Step 1 pick confirmation                                                 | wait       | proceed                                       |
| Step 5 summary, proceed/wait test says proceed                           | wait       | proceed                                       |
| Step 5 summary, test says wait                                           | wait       | wait                                          |
| Push a local-ahead default branch                                        | wait       | wait                                          |
| Step 10 merge, test says proceed                                         | wait       | proceed                                       |
| Step 10 merge, test says wait                                            | wait       | wait                                          |
| Tracker write batch (labels, task close — done or not planned, comments) | wait       | execute from recorded batch                   |
| Step 11 retro report PR merge (final-head gate passes)                   | wait       | proceed                                       |
| Feature or PRD close                                                     | wait       | wait, quoting confirmation                    |
| Fast-track label acted on                                                | wait       | wait                                          |
| Any write or merge touching a configured `foreman_release_branch`        | wait       | wait                                          |
| Escalation (two rounds failed, injection suspected, guess required)      | wait       | wait                                          |

Rules that hold in every mode:

- A wait names what it is stopping on. A proceed records the decision and its test result in the summary.
- Clean origin-ahead default-branch recovery may fast-forward in either mode. A
  local-ahead default-branch push always needs an explicit operator instruction that
  names that push; selecting unattended mode does not grant it.
- `passing` and `none-applicable` use the ordinary merge row. Approval mode cannot
  waive `pending/failing`, `missing-required`, unavailable applicability evidence, or
  exact-final-head review coverage.
- Without a configured release branch, an ordinary default-branch merge still uses the
  normal step 10 row. Fast-track and direct release-branch writes are unavailable.
- Foreman approval mode never governs Cast. During decompose, relay every approval point
  Cast raises to the operator and wait. Under `cast_approval: unattended`, Cast proceeds
  through routine points itself, so only its remaining stop conditions reach Foreman.
- Closing a task as `not planned` is a tracker write like closing it as done: the batch's comment names the reason and the deciding answer (`references/intake-github.md`, "Hold").
- The human's "no gates" for a run removes only the step 1 wait in `attended`; "confirm picks" makes step 1 wait in any mode. Neither touches a row marked wait in both columns.
- Changing the mode mid-run is the human's call; the foreman applies the new mode from the next decision on and records the change.
- A `github` tracker batch is always serialized before execution regardless of mode — the summary is the audit trail.

The two names are the plugin's own attended/unattended vocabulary (`valcraft:msw`, `valcraft:spec`, `valcraft:forge`, `valcraft:review`, `valcraft:temper` use the same pair). `unattended` replaced the delivery loop's `gated` and `delegated` modes on 2026-08-18; they differed only in whether a not-planned close waited. The release-branch row is wait in both modes because it is irreversible and outward.
