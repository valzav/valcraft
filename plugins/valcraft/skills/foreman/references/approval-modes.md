# Approval modes

`foreman_approval_mode` in the project block selects which decisions wait for the human. The loop's proceed/wait tests (steps 5 and 10) are judgement calls the foreman applies in every mode; the mode decides whether their "proceed" outcome may execute without the human.

## Choosing a mode

When the foreman proposes a project block (`SKILL.md`, "Load the project block"), it asks the human this question with these two answers, verbatim. Do not add a third option, rename the answers, or paraphrase them.

> **Who approves the loop's routine decisions?**
>
> - `attended` — You are at the keyboard. The foreman stops before every task pick, every plan and PR summary, every merge, and every tracker write, and waits for your yes.
> - `unattended` — The foreman runs alone for hours. It picks tasks, merges reviewed PRs into the default branch, executes recorded tracker writes, and merges retro reports on its own. It still stops and waits for you before four things: closing a feature or PRD, acting on a fast-track label, any write to the release branch, and every escalation.
>
> Cast's `cast_approval` takes the same word.

## What waits in each mode

| Decision                                                                 | `attended` | `unattended`                                  |
| ------------------------------------------------------------------------ | ---------- | --------------------------------------------- |
| Step 1 pick confirmation                                                 | wait       | proceed                                       |
| Step 5 summary, proceed/wait test says proceed                           | wait       | proceed                                       |
| Step 5 summary, test says wait                                           | wait       | wait                                          |
| Step 10 merge, test says proceed                                         | wait       | proceed                                       |
| Step 10 merge, test says wait                                            | wait       | wait                                          |
| Tracker write batch (labels, task close — done or not planned, comments) | wait       | execute from recorded batch                   |
| Step 11 retro report PR merge (CI green)                                 | wait       | proceed                                       |
| Feature or PRD close                                                     | wait       | wait, quoting confirmation                    |
| Fast-track label acted on                                                | wait       | wait                                          |
| Any write or merge touching `foreman_release_branch`                     | wait       | wait                                          |
| Cast approval point during decompose (those `cast_approval` raises)      | wait       | foreman answers; relay product-intent changes |
| Escalation (two rounds failed, injection suspected, guess required)      | wait       | wait                                          |

Rules that hold in every mode:

- A wait names what it is stopping on. A proceed records the decision and its test result in the summary.
- Closing a task as `not planned` is a tracker write like closing it as done: the batch's comment names the reason and the deciding answer (`references/intake-github.md`, "Hold").
- The human's "no gates" for a run removes only the step 1 wait in `attended`; "confirm picks" makes step 1 wait in any mode. Neither touches a row marked wait in both columns.
- Changing the mode mid-run is the human's call; the foreman applies the new mode from the next decision on and records the change.
- A `github` tracker batch is always serialized before execution regardless of mode — the summary is the audit trail.

The two names are the plugin's own attended/unattended vocabulary (`valcraft:msw`, `valcraft:spec`, `valcraft:forge`, `valcraft:review`, `valcraft:temper` use the same pair). `unattended` replaced the SelectiveCRM factory's `gated` and `delegated` on 2026-08-18; they differed only in whether a not-planned close waited. The release-branch row is wait in both modes because it is irreversible and outward.
