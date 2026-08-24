# Configuration contract

Valcraft configuration lives in two files under `.valcraft/`:

- `.valcraft/config.yaml` — the committed base. It is tracked in git, shared by every collaborator, and standalone-valid: it holds the complete configuration and passes validation on its own.
- `.valcraft/config.local.yaml` — the optional user-local overlay. It is gitignored, never committed, and may set only user-scoped keys.

The **resolved configuration** is the base with each overlay key applied. Readers validate and use the resolved configuration. Tune is the sole writer of both files.

Every mapping in either file is closed: reject unknown keys at every level. Reject duplicate YAML keys, non-string mapping keys, and values of the wrong YAML type. Strings required below must be nonempty after trimming. Neither file contains a schema version, and no value has a read-time default.

## Scope split

Repo-scoped settings live only in the base: the whole `tracker` section, `foreman.default_branch`, `foreman.release_branch`, `foreman.clarification_assignees`, and `pull_requests.merge_strategy`. A repo-scoped key in the overlay is a validation error.

User-scoped settings may appear in the overlay: `foreman.approval_mode`, `foreman.backend`, `foreman.herdr`, and `foreman.ao`.

## Resolution

Each overlay key replaces the corresponding base value atomically; nothing merges deeper.

- An overlay `foreman.approval_mode` replaces the base value.
- `foreman.backend` and the backend-specific mappings `foreman.herdr` and `foreman.ao` override as a unit. An overlay backend of `herdr` requires a complete overlay `herdr` mapping, and an overlay backend of `ao` requires a complete overlay `ao` mapping; an overlay `backend` masks every base backend-specific mapping. An overlay `herdr` or `ao` mapping without an overlay `backend` is valid only when the resolved backend matches it, and it replaces the whole base mapping.

Validate in three steps: the base standalone against the shape below; the overlay as a closed mapping permitting only `foreman` with the user-scoped keys; the resolved configuration against the shape below, including reviewer independence.

## Shape

The base takes this shape and the root requires exactly `tracker`, `foreman`, and `pull_requests`:

```yaml
tracker:
  mode: local

foreman:
  backend: subagents
  approval_mode: unattended
  default_branch: main
  release_branch: null

pull_requests:
  merge_strategy: squash
```

### Tracker

`tracker.mode` is `local` or `github`.

- `local` permits only `mode`.
- `github` requires `github_repository`: either one repository identifier accepted as free-form input and stored as a string, or the literal placeholder `TBD` recording that the operator has not selected the target yet. `TBD` is never an identifier: a skill that needs a concrete target treats it as pending activation and routes target selection back to Tune. Do not probe or mutate the host merely to validate configuration.

Changing `tracker.mode` when committed feature artifacts exist is blocked: every committed mapping would need migration, and Tune performs no migration.

### Foreman

`foreman` always requires:

- `backend`: `subagents`, `ao`, or `herdr`;
- `approval_mode`: `attended` or `unattended`;
- `default_branch`: a branch identifier stored as a string; and
- `release_branch`: a branch identifier stored as a string or YAML `null` when no separate release branch exists.

When `tracker.mode` is `github`, `foreman` also requires `clarification_assignees` with exactly `product` and `default`. Each value is an assignee identifier string or YAML `null`. Omit this mapping in local mode.

When the resolved `foreman.backend` is `herdr`, the resolved configuration also requires `foreman.herdr`. Omit it for `subagents` and `ao`.

When the resolved `foreman.backend` is `ao`, the resolved configuration also requires `foreman.ao` with exactly `project_id`: the exact Agent Orchestrator project identifier stored as a nonempty string, passed only as an argument value. Omit `foreman.ao` for `subagents` and `herdr`.

`foreman.herdr` requires:

- `session`: a Herdr session identifier string or YAML `null` to use the active controller session; and
- `workers`: exactly `draft`, `plan_review`, `forge`, `code_review`, `land`, `temper`, `retro_review`, and `evidence_review`.

Each worker requires exactly `harness`, `model`, and `effort`.

- Claude workers use `harness: claude`; known model aliases are `sonnet`, `fable`, and `opus`; allowed effort is `low`, `medium`, `high`, `xhigh`, or `max`.
- Codex workers use `harness: codex`; known model aliases are `gpt-5.6-terra`, `gpt-5.6-sol`, and `gpt-5.6-luna`. Terra and Sol allow `low`, `medium`, `high`, `xhigh`, `max`, or `ultra`. Luna allows `low`, `medium`, `high`, `xhigh`, or `max`.
- A nonempty, single-line model alias without control characters and whose first character is not `-` is valid as a free-form model value. Keep it as data and do not infer its provider or availability. For a free-form Codex model, allow `low`, `medium`, `high`, `xhigh`, `max`, or `ultra`; runtime readiness still verifies model availability. A free-form Claude model uses the Claude effort set.

Reviewer independence is structural. On the resolved configuration, require different harnesses for each pair: `plan_review` and `draft`, `code_review` and `forge`, `retro_review` and `temper`, and `evidence_review` and `land`. Reject the complete candidate if any pair uses the same harness.

### Pull requests

`pull_requests` requires only `merge_strategy`, one of `squash`, `merge`, or `rebase`. This choice selects a host merge method but grants no authority to use it.

## Question flow

Ask only questions whose answers are genuinely open. Apply a value without asking when one authoritative source resolves it: an answer the operator already supplied in the current exchange, a valid existing value the operator did not ask to change, or unambiguous repository evidence. Ask when authoritative sources conflict or none exists.

### First run or full repair

Walk this order. Every quoted choice is a list item with its explanation, not an inferred default. Skip a step whose value is already resolved by an authoritative source.

1. **Tasks/Issue Tracker:** `Local (Recommended)` — keep task state in the repository with no hosted tracker; `GitHub` — project features and tasks through GitHub Issues. For GitHub, ask for the repository identifier as free-form input; accept the literal `TBD` to defer target selection.
2. **Foreman Loop — backend.** Foreman is the coordinator that runs the delivery loop through fresh Draft, Review, Forge, Land, and Temper workers. Offer `Subagents (Recommended)` — use workers provided by the active coding session; `Herdr` — dispatch roles through a Herdr session with configured models. `ao` remains a valid `foreman.backend` value but is not offered interactively; when the operator explicitly configures `ao`, ask for `foreman.ao.project_id` as free-form input.
3. **Foreman Loop — approval:** `Unattended (Recommended)` — advance routine prepared stages while preserving mandatory authority gates; `Attended` — pause at Foreman's optional coordination gates.
4. **Default branch:** detect the branch from authoritative local or host metadata available without mutation, preferring an explicit hosting-service default or the remote symbolic HEAD. Do not call the current checkout authoritative merely because it is checked out. Store an unambiguous detected branch silently. Ask only when authoritative sources disagree — explain the conflict — or when none exists, offering `main (Recommended)` and `Enter another branch`. Store an explicit value in every case.
5. **Release branch:** `No separate release branch (Recommended)` — use YAML `null`; `Configure a release branch` — ask for the branch identifier.
6. **Clarification assignees, GitHub only:** `No default assignees (Recommended)` — store both values as YAML `null`; `Configure assignees` — ask separately for optional product and default assignee identifiers, with `None (Recommended)` first for each.
7. **Herdr, only when selected:** ask the session and worker questions below.
8. **Pull request strategy:** `Squash (Recommended)` — combine the pull request into one commit; `Merge commit` — retain the branch commits and add a merge commit; `Rebase` — replay the branch commits without a merge commit.

### Herdr

Ask for session binding first: `Use the active session (Recommended)` — store YAML `null`; `Pin a session` — ask for the session identifier.

Then show this preset list:

1. `Balanced (Recommended)` — use Claude Sonnet and Codex Terra at medium effort with independent reviewers.
2. `Quality` — use Claude Opus and Codex Sol at high effort with the same independent role split.
3. `Economy` — use Claude Fable and Codex Luna at low effort with the same independent role split.
4. `Custom` — choose harness, model, and effort for every role; invalid reviewer pairings are rejected.

All three presets use this harness split:

| Role              | Harness |
| ----------------- | ------- |
| `draft`           | Codex   |
| `plan_review`     | Claude  |
| `forge`           | Claude  |
| `code_review`     | Codex   |
| `land`            | Claude  |
| `temper`          | Claude  |
| `retro_review`    | Codex   |
| `evidence_review` | Codex   |

For Custom, ask each role in the table order. Put the preset harness for that role first and mark it recommended. After the harness choice, offer that harness's known models with the balanced alias first and marked recommended, followed by the other known aliases and `Enter another model alias`. Offer `Medium (Recommended)` first for effort, then every other effort supported by the selected known model. For a free-form model, use its harness's free-form effort set. Explain every effort in plain language. Revalidate all four independence pairs after the last role; do not silently change a conflicting answer.

## Reconfiguration

For an existing valid resolved configuration, reconfigure only when the caller or operator asks for it. The first question is a list of sections. When the caller or operator named a section, put that section first and mark it recommended; this focuses delegation without accepting answers from the caller. Otherwise use this order:

1. `Tasks/Issue Tracker (Recommended)` — change local or GitHub tracking and its dependent assignees.
2. `Foreman Loop` — change backend, approval mode, branches, and backend-dependent settings. Foreman is the coordinator that runs the delivery loop through fresh Draft, Review, Forge, Land, and Temper workers.
3. `Herdr workers` — change session, preset, or role settings; show only when the resolved backend is Herdr.
4. `Pull request strategy` — change the merge strategy.

Show each section with its current resolved value summary.

**Layer question.** When a reconfiguration changes only user-scoped keys, ask once where the change applies: `For everyone (Recommended)` — write it into the committed `.valcraft/config.yaml`; `Just for you` — write it into the gitignored `.valcraft/config.local.yaml` overlay. A change that touches any repo-scoped key writes to the base and never offers the overlay. An overlay write replaces its whitelisted keys atomically, with `backend` and `herdr` written as a unit.

Removal semantics apply within each file: never retain an inapplicable block as dormant configuration. In the base, changing tracker mode to local removes `tracker.github_repository` and `foreman.clarification_assignees`; changing to GitHub asks for both. In whichever file carries the change, moving Foreman away from Herdr removes that file's `foreman.herdr`; moving to Herdr asks the complete Herdr flow.

## Report and noninteractive use

Write immediately after the last answer; an interactive answer authorizes the write it configures, so ask no confirmation question. In the report, show the complete canonical YAML of every written file, and the resolved configuration whenever an overlay exists. After a base write outside an active Cast invocation, stage and commit only `.valcraft/config.yaml` and report the commit.

In a headless or noninteractive run, return `configuration_required` with the unresolved fields and make no write. Do not select recommended answers, convert an invalid partial document, or treat `foreman.approval_mode: unattended` as authority to answer questions.
