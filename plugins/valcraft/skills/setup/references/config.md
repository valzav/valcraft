# Configuration contract

`.valcraft/config.yaml` is a complete user-local snapshot. Every mapping is closed: reject unknown keys at every level. Reject duplicate YAML keys, non-string mapping keys, and values of the wrong YAML type. Strings required below must be nonempty after trimming. The file contains no schema version and has no defaults at read time.

## Shape

```yaml
tracker:
  mode: local

cast:
  approval_mode: attended

foreman:
  backend: subagents
  approval_mode: unattended
  default_branch: main
  release_branch: null

pull_requests:
  merge_strategy: squash
```

The root requires exactly `tracker`, `cast`, `foreman`, and `pull_requests`.

### Tracker

`tracker.mode` is `local` or `github`.

- `local` permits only `mode`.
- `github` requires `github_repository`, a repository identifier accepted as free-form input and stored as a string. Do not probe or mutate the host merely to validate configuration.

### Cast

`cast` requires only `approval_mode`, either `attended` or `unattended`.

### Foreman

`foreman` always requires:

- `backend`: `subagents`, `ao`, or `herdr`;
- `approval_mode`: `attended` or `unattended`;
- `default_branch`: a branch identifier stored as a string; and
- `release_branch`: a branch identifier stored as a string or YAML `null` when no separate release branch exists.

When `tracker.mode` is `github`, `foreman` also requires `clarification_assignees` with exactly `product` and `default`. Each value is an assignee identifier string or YAML `null`. Omit this mapping in local mode.

When `foreman.backend` is `herdr`, `foreman` also requires `herdr`. Omit it for `subagents` and `ao`.

`foreman.herdr` requires:

- `session`: a Herdr session identifier string or YAML `null` to use the active controller session; and
- `workers`: exactly `draft`, `plan_review`, `forge`, `code_review`, `land`, `temper`, `retro_review`, and `evidence_review`.

Each worker requires exactly `harness`, `model`, and `effort`.

- Claude workers use `harness: claude`; known model aliases are `sonnet`, `fable`, and `opus`; allowed effort is `low`, `medium`, `high`, `xhigh`, or `max`.
- Codex workers use `harness: codex`; known model aliases are `gpt-5.6-terra`, `gpt-5.6-sol`, and `gpt-5.6-luna`. Terra and Sol allow `low`, `medium`, `high`, `xhigh`, `max`, or `ultra`. Luna allows `low`, `medium`, `high`, `xhigh`, or `max`.
- A nonempty, single-line model alias without control characters and whose first character is not `-` is valid as a free-form model value. Keep it as data and do not infer its provider or availability. For a free-form Codex model, allow `low`, `medium`, `high`, `xhigh`, `max`, or `ultra`; runtime readiness still verifies model availability. A free-form Claude model uses the Claude effort set.

Reviewer independence is structural. Require different harnesses for each pair: `plan_review` and `draft`, `code_review` and `forge`, `retro_review` and `temper`, and `evidence_review` and `land`. Reject the complete candidate if any pair uses the same harness.

### Pull requests

`pull_requests` requires only `merge_strategy`, one of `squash`, `merge`, or `rebase`. This choice selects a host merge method but grants no authority to use it.

## Question flow

Ask only questions whose answers are not already supplied by the operator in the current interactive exchange. Still show and confirm the complete resulting YAML before writing.

### First run or full repair

Ask in this order. Every quoted choice is a list item with its explanation, not an inferred default.

1. **Tracker:** `Local (Recommended)` — keep task state in the repository with no hosted tracker; `GitHub` — project features and tasks through GitHub Issues. For GitHub, ask for the repository identifier as free-form input.
2. **Cast approval:** `Attended (Recommended)` — confirm Cast's exact scaffold before it writes; `Unattended` — let Cast apply an already-defined scaffold without that gate.
3. **Foreman backend:** `Subagents (Recommended)` — use workers provided by the active coding session; `AO` — dispatch through the external AO orchestrator; `Herdr` — dispatch roles through a Herdr session with configured models.
4. **Foreman approval:** `Unattended (Recommended)` — advance routine prepared stages while preserving mandatory authority gates; `Attended` — pause at Foreman's optional coordination gates.
5. **Default branch:** inspect authoritative repository metadata first. Offer the detected branch as `(Recommended)` and explain its source. If no authoritative branch is available, offer `main (Recommended)` and `Enter another branch`. Store an explicit value in either case.
6. **Release branch:** `No separate release branch (Recommended)` — use YAML `null`; `Configure a release branch` — ask for the branch identifier.
7. **Clarification assignees, GitHub only:** `No default assignees (Recommended)` — store both values as YAML `null`; `Configure assignees` — ask separately for optional product and default assignee identifiers, with `None (Recommended)` first for each.
8. **Herdr, only when selected:** ask the session and worker questions below.
9. **Pull-request merge strategy:** `Squash (Recommended)` — combine the pull request into one commit; `Merge commit` — retain the branch commits and add a merge commit; `Rebase` — replay the branch commits without a merge commit.

Detect the default branch from authoritative local or host metadata available without mutation, preferring an explicit hosting-service default or the remote symbolic HEAD. Do not call the current checkout authoritative merely because it is checked out. If authoritative sources disagree, explain the conflict and ask the operator to select or enter the branch.

### Herdr

Ask for session binding first: `Use the active session (Recommended)` — store YAML `null`; `Pin a session` — ask for the session identifier.

Then show this preset list:

1. `Balanced (Recommended)` — use Claude Sonnet and Codex Terra at medium effort with independent reviewers.
2. `Quality` — use Claude Opus and Codex Sol at high effort with the same independent role split.
3. `Economy` — use Claude Fable and Codex Luna at low effort with the same independent role split.
4. `Custom` — choose harness, model, and effort for every role; invalid reviewer pairings are rejected.

All three presets use this harness split:

| Role | Harness |
| --- | --- |
| `draft` | Codex |
| `plan_review` | Claude |
| `forge` | Claude |
| `code_review` | Codex |
| `land` | Claude |
| `temper` | Claude |
| `retro_review` | Codex |
| `evidence_review` | Codex |

For Custom, ask each role in the table order. Put the preset harness for that role first and mark it recommended. After the harness choice, offer that harness's known models with the balanced alias first and marked recommended, followed by the other known aliases and `Enter another model alias`. Offer `Medium (Recommended)` first for effort, then every other effort supported by the selected known model. For a free-form model, use its harness's free-form effort set. Explain every effort in plain language. Revalidate all four independence pairs after the last role; do not silently change a conflicting answer.

## Reconfiguration

For an existing valid file, the first question is a list of sections. When the caller or operator named a section, put that section first and mark it recommended; this focuses delegation without accepting answers from the caller. Otherwise use this order:

1. `Tracker (Recommended)` — change local or GitHub tracking and its dependent assignees.
2. `Cast` — change Cast's approval mode.
3. `Foreman` — change backend, approval mode, branches, and backend-dependent settings.
4. `Herdr workers` — change session, preset, or role settings; show only when Herdr is the current backend.
5. `Pull requests` — change merge strategy.

After one section, offer `Review and save (Recommended)` and `Change another section`. Always confirm the complete candidate, not only the changed fragment.

Changing tracker mode to local removes `tracker.github_repository` and `foreman.clarification_assignees`. Changing to GitHub asks for both. Changing Foreman away from Herdr removes `foreman.herdr`; changing to Herdr asks the complete Herdr flow. Never retain an inapplicable block as dormant configuration.

## Confirmation and noninteractive use

Display the complete canonical YAML. Ask with this list:

1. `Save configuration (Recommended)` — atomically replace the file.
2. `Change another section` — return to the section menu or the relevant first-run question.
3. `Cancel` — preserve the existing file or leave it absent.

In a headless or noninteractive run, return `configuration_required` with the unresolved fields and make no write. Do not select recommended answers, convert an invalid partial document, or treat `foreman.approval_mode: unattended` as setup authority.
