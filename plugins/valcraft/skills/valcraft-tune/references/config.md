# Configuration contract

Valcraft configuration lives in two files under `.valcraft/`:

- `.valcraft/config.yaml` — the committed base. It is tracked in git, shared by every collaborator, and standalone-valid: it holds the complete configuration and passes validation on its own.
- `.valcraft/config.local.yaml` — the optional user-local overlay. It is gitignored, never committed, and may set only user-scoped keys.

The **resolved configuration** is the base with each overlay key applied. Readers validate and use the resolved configuration. Tune is the sole writer of both files.

Every mapping in either file is closed: reject unknown keys at every level. Reject duplicate YAML keys, non-string mapping keys, and values of the wrong YAML type. Strings required below must be nonempty after trimming. The base records the plugin version the repository was last migrated to in `valcraft_version`; no value has a read-time default.

## Scope split

Repo-scoped settings live only in the base: `valcraft_version`, the whole `tracker` section, `foreman.default_branch`, `foreman.release_branch`, `foreman.clarification_assignees`, and `pull_requests.merge_strategy`. A repo-scoped key in the overlay is a validation error.

User-scoped settings may appear in the overlay: `foreman.approval_mode`, `foreman.answer_page`, `foreman.backend`, `foreman.herdr`, and `foreman.ao`.

The [browser record](#browser-record) `browser` and the [editor record](#editor-record) `editor` are overlay-only. Each records the state of one machine, so either key in the base is a validation error.

## Resolution

Each overlay key replaces the corresponding base value atomically; nothing merges deeper.

- An overlay `foreman.approval_mode` replaces the base value.
- An overlay `foreman.answer_page` replaces the base value, including an overlay `false` over a base `true`. An overlay without the key inherits the base value.
- `foreman.backend` and the backend-specific mappings `foreman.herdr` and `foreman.ao` override as a unit. An overlay backend of `herdr` requires a complete overlay `herdr` mapping, and an overlay backend of `ao` requires a complete overlay `ao` mapping; an overlay `backend` masks every base backend-specific mapping. An overlay `herdr` or `ao` mapping without an overlay `backend` is valid only when the resolved backend matches it, and it replaces the whole base mapping.

Validate in three steps: the base standalone against the shape below; the overlay as a closed mapping permitting only `foreman` with the user-scoped keys, `browser`, and `editor`; the resolved configuration against the shape below, including reviewer independence.

## Shape

The base takes this shape and the root requires exactly `valcraft_version`, `tracker`, `foreman`, and `pull_requests`:

```yaml
valcraft_version: "0.8.1"

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

The `valcraft_version` value above is illustrative. First run and full repair write the current plugin version, as [Plugin version](#plugin-version) defines.

### Tracker

`tracker.mode` is `local` or `github`.

- `local` permits only `mode`.
- `github` requires `github_repository`: either one repository identifier accepted as free-form input and stored as a string, or the literal placeholder `TBD` recording that the operator has not selected the target yet. `TBD` is never an identifier: a skill that needs a concrete target treats it as pending activation and routes target selection back to Tune. Do not probe or mutate the host merely to validate configuration.

Changing `tracker.mode` when committed feature artifacts exist is blocked: every committed mapping would need migration, and Tune does not migrate tracker mappings. Replacing one concrete `github_repository` identifier with another is blocked for the same reason while any committed positive `spec_issue` or task issue mapping exists: issue numbers are repository-relative, so the retarget would silently point every mapping at a different tracker. Replacing the `TBD` placeholder with the first concrete identifier is activation, not retargeting, and stays allowed.

### Foreman

`foreman` always requires:

- `backend`: `subagents`, `ao`, or `herdr`;
- `approval_mode`: `attended` or `unattended`;
- `default_branch`: a branch identifier stored as a string; and
- `release_branch`: a branch identifier stored as a string or YAML `null` when no separate release branch exists.

`foreman` may also hold `answer_page`, a YAML boolean. `true` turns on Foreman's answer page: large operator question sets and the feature-close confirmation are delivered as a local HTML page that the operator answers and pastes back, as Foreman's [`approval-modes.md`](../../valcraft-foreman/references/approval-modes.md#answer-page) defines. A resolved configuration without the key means the page is off; that is the key's absence meaning, not a read-time default. Tune never writes `false` to the base, because an absent base key already means off; the overlay records `false` to turn the page off over a base `true`.

When `tracker.mode` is `github`, `foreman` also requires `clarification_assignees` with exactly `product` and `default`. Each value is an assignee identifier string or YAML `null`. Omit this mapping in local mode.

When the resolved `foreman.backend` is `herdr`, the resolved configuration also requires `foreman.herdr`. Omit it for `subagents` and `ao`.

When the resolved `foreman.backend` is `ao`, the resolved configuration also requires `foreman.ao` with exactly `project_id`: the exact Agent Orchestrator project identifier stored as a nonempty string, passed only as an argument value. Omit `foreman.ao` for `subagents` and `herdr`.

`foreman.herdr` requires:

- `session`: a Herdr session identifier string or YAML `null` to use the active controller session; and
- `workers`: exactly `spec`, `spec_review`, `draft`, `plan_review`, `forge`, `code_review`, `land`, `temper`, `retro_review`, and `evidence_review`.

Each worker requires exactly `harness`, `model`, and `effort`.

- `harness` is `claude`, `codex`, or `cursor`.
- `model` is a known alias for that harness in [`models.md`](models.md), or a free-form alias. A free-form alias is a nonempty, single-line value without control characters whose first character is not `-`. Keep it as data and do not infer its provider or availability; runtime readiness verifies it. `models.md` may add harness-specific restrictions on free-form aliases.
- `effort` is in the set `models.md` gives for the model: the known alias's set, or the harness's free-form set.

Reviewer independence is structural. On the resolved configuration, require different harnesses for each pair: `spec_review` and `spec`, `plan_review` and `draft`, `code_review` and `forge`, `retro_review` and `temper`, and `evidence_review` and `land`. Reject the complete candidate if any pair uses the same harness.

### Pull requests

`pull_requests` requires only `merge_strategy`, one of `squash`, `merge`, or `rebase`. This choice selects a host merge method but grants no authority to use it.

### Browser record

The overlay may hold `browser`, written only by [browser discovery](#browser-discovery). It is valid only when the resolved `foreman.backend` is `herdr`. Each key is a harness that appears in the resolved `foreman.herdr.workers`, and each value records one browser tool that harness proved it can drive on this machine:

```yaml
browser:
  codex:
    tool: agent-browser
    kind: command
    version: "0.27.0"
    executable: /usr/local/bin/agent-browser
    proof: opened a local page titled valcraft-probe-4f2a and read the title back
```

Each entry requires exactly these keys:

- `tool`: the tool's name as the harness reports it.
- `kind`: `command` for a program any harness could run, or `harness_tool` for a tool only that harness provides.
- `version`: the version the tool reports, stored as a string, or YAML `null` when it reports none.
- `executable`: an absolute path when `kind` is `command`; YAML `null` when it is `harness_tool`.
- `proof`: the harness's one-line account of the check in the discovery task.

An absent `browser` key means no record.

### Editor record

The overlay may hold `editor`, written only by [editor navigation](#editor-navigation). It turns on editor navigation from Herdr panes for this user in this repository, and it is independent of `foreman.backend`:

```yaml
editor:
  adapter: zed
  executable: /opt/homebrew/bin/zed
```

It requires exactly these keys:

- `adapter`: `zed` or `vscode`, the editor launchers the Valcraft Herdr plugin supports.
- `executable`: an absolute path that resolves, through any symbolic links, to an executable file.

An absent `editor` key means editor navigation is off. The plugin reads the record from the primary checkout, because a linked worktree has no overlay, and it refuses an overlay that git tracks or does not ignore.

### Plugin version

`valcraft_version` is a string of three dot-separated non-negative integers: the plugin version this repository was last migrated to. The current plugin version is the newest `## vX.Y.Z` heading in [`migrations.md`](migrations.md). Compare the two component by component as integers.

- Equal: valid.
- Older, when every entry under every heading newer than the recorded version says `Tune performs: none`: valid, classified `behind`. No release since the recorded version requires a configuration change, so every reader proceeds without delegating to Tune. Judge by that label alone; a reader never evaluates `Applies when`.
- Absent, or older with any other entry: invalid, reason `outdated`, even when the shape also fails, because ledger entries may repair the shape. Tune resolves it with the migration flow in `migrations.md`; the first-run flow does not run for an outdated base. Any invalidity that remains after the migration flow takes the ordinary repair path.
- Newer: invalid, reason `plugin outdated`. The installed plugin is older than the repository; Tune writes nothing and reports `plugin_outdated`.

Every reader delegates either invalid reason to Tune through its existing invalid-configuration rule and never edits the key. First run and full repair write the current plugin version without asking. Only the migration flow advances a recorded value. Any Tune run on a `behind` base runs that flow first, then the requested work; reconfiguration otherwise preserves the recorded value.

## Question flow

Ask only questions whose answers are genuinely open. Apply a value without asking when one authoritative source resolves it: an answer the operator already supplied in the current exchange, a valid existing value the operator did not ask to change, or unambiguous repository evidence. Ask when authoritative sources conflict or none exists.

This rule governs the value questions below. The reconfiguration section menu is not one of them: it always appears, and the rule under [Reconfiguration](#reconfiguration) states why.

A requested value that fails validation, such as an approval mode outside the allowed set, is an invalid answer, not a blocked change. Reject it and state why. Then ask that setting's question from its section, with every valid choice explained. A noninteractive run returns `configuration_required` for it instead. `configuration_change_rejected` covers only a change the contract structurally blocks: a tracker-mode change while committed feature artifacts exist, or a concrete-to-concrete `github_repository` change while a committed positive mapping exists.

### First run or full repair

Walk this order. Every quoted choice is a list item with its explanation, not an inferred default. Skip a step whose value is already resolved by an authoritative source.

1. **Tasks/Issue Tracker:** `Local (Recommended)` — keep task state in the repository with no hosted tracker; `GitHub` — project features and tasks through GitHub Issues. For GitHub, ask for the repository identifier as free-form input; accept the literal `TBD` to defer target selection.
2. **Foreman Loop — backend.** Foreman is the coordinator that runs the delivery loop through fresh Spec, Draft, Review, Forge, Land, and Temper workers. Offer `Subagents (Recommended)` — use workers provided by the active coding session; `Herdr` — dispatch roles through a Herdr session with configured models. `ao` remains a valid `foreman.backend` value but is not offered interactively; when the operator explicitly configures `ao`, ask for `foreman.ao.project_id` as free-form input. `ao` is temporarily unsupported because Foreman's retry of external failures is not verified on it; state that in the report whenever the resolved backend is `ao`.
3. **Foreman Loop — approval:** `Unattended (Recommended)` — advance routine prepared stages while preserving mandatory authority gates; `Attended` — pause at Foreman's optional coordination gates.
4. **Answer page:** `Chat (Recommended)` — answer every operator question in the chat; `HTML` — large question sets and the feature-close confirmation open as a local HTML page that you answer with checkboxes, option picks, and notes, then paste back into the chat. `Chat` writes no key; `HTML` writes `foreman.answer_page: true`.
5. **Default branch:** detect the branch from authoritative local or host metadata available without mutation, preferring an explicit hosting-service default or the remote symbolic HEAD. Do not call the current checkout authoritative merely because it is checked out. Store an unambiguous detected branch silently. Ask only when authoritative sources disagree — explain the conflict — or when none exists, offering `main (Recommended)` and `Enter another branch`. Store an explicit value in every case.
6. **Release branch:** `No separate release branch (Recommended)` — use YAML `null`; `Configure a release branch` — ask for the branch identifier.
7. **Clarification assignees, GitHub only:** `No default assignees (Recommended)` — store both values as YAML `null`; `Configure assignees` — ask separately for optional product and default assignee identifiers, with `None (Recommended)` first for each.
8. **Herdr, only when selected:** ask the session and worker questions below.
9. **Browser tools, Herdr only:** `Discover browser tools (Recommended)` — each configured harness reports a browser tool it can drive on this machine, and Spec starts its browser checks from that record; `Skip — no web UI` — record nothing. Apply `Discover` without asking when a committed `design.md` records a browser verification route under `Verified baseline assumptions`. Run [browser discovery](#browser-discovery) after the last other answer.
10. **Pull request strategy:** `Squash (Recommended)` — combine the pull request into one commit; `Merge commit` — retain the branch commits and add a merge commit; `Rebase` — replay the branch commits without a merge commit.
11. **Editor navigation, only when [readiness](#editor-navigation) holds:** `Enable (Recommended)` — open Valcraft identities and file references from Herdr panes in your editor, which installs the Valcraft Herdr plugin; `Skip` — record nothing. When readiness fails, skip the step and name the missing requirement in the report.

### Herdr

Ask for session binding first: `Use the active session (Recommended)` — store YAML `null`; `Pin a session` — ask for the session identifier.

Then show the presets from [`models.md`](models.md) as a list, `Balanced (Recommended)` first, each with its operator summary, followed by `Custom` — choose harness, model, and effort for every role; invalid reviewer pairings are rejected.

Every preset uses this harness split:

| Role | Harness |
| --- | --- |
| `spec` | Codex |
| `spec_review` | Claude |
| `draft` | Codex |
| `plan_review` | Claude |
| `forge` | Claude |
| `code_review` | Codex |
| `land` | Claude |
| `temper` | Claude |
| `retro_review` | Codex |
| `evidence_review` | Codex |

For Custom, ask each role in the table order. Offer Claude, Codex, and Cursor; put the preset harness for that role first and mark it recommended. After the harness choice, offer that harness's known models from `models.md` with its recommended model first and marked recommended, followed by the other known aliases and `Enter another model alias`. For effort, offer the role's recommended effort from `models.md` first and marked recommended: `High (Recommended)` for a review role, `Medium (Recommended)` for every other role. Then offer every other effort `models.md` allows for the selected known model. For a free-form model, use its harness's free-form effort set. Explain every effort in plain language. Revalidate all five independence pairs after the last role; do not silently change a conflicting answer.

## Reconfiguration

For an existing valid resolved configuration, reconfigure only when the caller or operator asks for it; a bare direct invocation is that request. The first question is always a list of sections, including when the request already named one. Naming a section is not an answer to this question, whether a caller or the operator named it: it selects the order, so put that section first and mark it recommended. The menu shows every section the operator may also want to change in the same run, which a named section cannot establish. Otherwise use this order:

1. `Tasks/Issue Tracker (Recommended)` — change local or GitHub tracking and its dependent assignees.
2. `Foreman Loop` — change backend, approval mode, answer page, branches, and backend-dependent settings. Foreman is the coordinator that runs the delivery loop through fresh Spec, Draft, Review, Forge, Land, and Temper workers.
3. `Herdr workers` — change session, preset, or role settings; show only when the resolved backend is Herdr.
4. `Pull request strategy` — change the merge strategy.
5. `Browser tools` — discover this machine's browser tools again, which replaces the record, or remove the record; show only when the resolved backend is Herdr.
6. `Editor navigation` — enable it, change the editor, or disable it.

Show each section with its current resolved value summary.

**Layer question.** When a reconfiguration changes only user-scoped keys, ask once where the change applies: `For everyone (Recommended)` — write it into the committed `.valcraft/config.yaml`; `Just for you` — write it into the gitignored `.valcraft/config.local.yaml` overlay. A change that touches any repo-scoped key writes to the base and never offers the overlay. The browser record and the editor record always go to the overlay and never take the layer question. An overlay write replaces its whitelisted keys atomically, with `backend` and `herdr` written as a unit.

The answer page follows the layer answer. `For everyone` writes `foreman.answer_page: true` to the base for `HTML`, and removes the key from the base for `Chat`. `Just for you` writes the chosen value, `true` for `HTML` or `false` for `Chat`, to the overlay.

Removal semantics apply within each file: never retain an inapplicable block as dormant configuration. In the base, changing tracker mode to local removes `tracker.github_repository` and `foreman.clarification_assignees`; changing to GitHub asks for both. In whichever file carries the change, moving Foreman away from Herdr removes that file's `foreman.herdr`, and the resolved move removes the overlay's `browser`; moving to Herdr asks the complete Herdr flow. A worker-map change that removes every role on a harness removes that harness's `browser` entry. A change that adds a harness leaves it without an entry, and the report names the `Browser tools` section that fills it.

## Writing

Create `.valcraft/` if needed, serialize each written file to its own temporary file there, and parse and validate every temporary file before replacing any destination. Then atomically replace each destination from the same directory, rechecking first that it is still a regular non-symlink path. If any replacement, re-read, or the final resolved validation fails, restore every replaced destination to its pre-run bytes, remove the temporary files, and report `configuration_write_failed`.

## Noninteractive use

In a headless or noninteractive run, return `configuration_required` with the unresolved fields and make no write. A migration flow whose applicable entries name no choice has no unresolved field: it completes, including its write and commit, in a direct or delegated run, attended or not. Do not select recommended answers, convert an invalid partial document, or treat `foreman.approval_mode: unattended` as authority to answer questions.

## Browser discovery

Browser discovery records, for each harness in the resolved Herdr worker map, one browser tool that harness proved it can drive on this machine. Run it only when the resolved `foreman.backend` is `herdr` and the question flow selected it. Tune chooses no tool and holds no list of tool names: each harness names its own.

### Discovery task

Each harness performs this task:

1. Find the browser tool you used most recently, in your own harness's session history on this machine, that runs as a command, because every harness can share it. Take the most recent harness tool only when the history holds no qualifying command tool. Only a tool installed outside temporary directories qualifies; a copy an earlier session left in a temporary directory does not.
2. Create a new temporary directory outside the repository. Write a local HTML page there with a unique title.
3. Serve that directory over HTTP on the loopback address `127.0.0.1` only.
4. Open the page's loopback URL with the tool, and read its title back. Use no other network access.
5. When the tool fails the check, or you found none in step 1, try another browser tool available to you now, a command tool before a harness tool. Stop when one passes or none remains.
6. Stop the server. Install nothing and change no configuration. Write nothing outside that temporary directory and the result file.
7. Write the result file: one entry in the [browser record](#browser-record) shape for the tool that passed, or `none: <reason>` when no tool passed the check.

### Tune's own harness

When the worker map lists the harness Tune runs in, Tune performs the discovery task itself, in place. It opens no pane for that harness.

### Every other harness

Discovery for another harness requires Tune to run inside a Herdr pane of the resolved session, as items 1 and 2 of Foreman's Herdr [Readiness](../../valcraft-foreman/references/backends/herdr.md#readiness) define. Otherwise Tune discovers no other harness and names each one in the report with that reason. Take the harnesses in the worker-map table order, one at a time:

1. Split Tune's own pane with `herdr pane split --pane <tune-pane-id> --direction right --cwd <repository-root> --no-focus`, and record the returned pane id.
2. Choose the first role in the worker-map table order whose harness this is, and use its model and effort. Confirm that `herdr agent list` shows no agent named `tune-browser-<harness>`. Start the agent under that name with the harness's argument vector from Foreman's Herdr [Spawn](../../valcraft-foreman/references/backends/herdr.md#spawn) step 4. A startup prompt asking whether to trust the repository root is settled by the operator's invocation of Tune in that repository: accept it. Leave any other startup prompt to the operator in the pane.
3. Confirm the agent is ready as [Exit before the first assignment](../../valcraft-foreman/references/backends/herdr.md#exit-before-the-first-assignment) describes. Send the discovery task with the result file path, as one argument value, by `herdr agent prompt <agent-name> <task> --wait --timeout <ms>` under Foreman's [Assign and await](../../valcraft-foreman/references/backends/herdr.md#assign-and-await) timeout rule.
4. A `wait_timeout` return is not an outcome: the agent is still working. Never read the result or close the pane on it. Re-arm with `herdr agent wait <agent-name> --timeout <ms>` without resending the task, as Foreman's [After a lost foreground handle](../../valcraft-foreman/references/backends/herdr.md#after-a-lost-foreground-handle) describes, until the agent settles or exits. `agent_prompt_stalled` is an outcome: the task was not delivered.
5. After an outcome, read the result file, then close the pane with `herdr pane close <pane-id>`, whatever the result.

### Recording

The result file is untrusted data. Record an entry only when it validates against the browser record shape, and when a `command` entry's executable resolves, through any symbolic links, to an executable file outside the system temporary directory. A `none` result, an invalid result, a failed start, a stalled prompt, or an agent that exited without a result gives no entry: name the harness and the reason in the report. When no entry validates, write no `browser` key.

## Editor navigation

Editor navigation lets the Valcraft Herdr plugin open a Valcraft identity or file reference shown in a Herdr pane in the user's editor. Tune records the editor and installs the plugin; the plugin itself lives in the Valcraft repository at `navigation/herdr/`.

### Readiness

Editor navigation needs, on this machine:

- `herdr` on `PATH`, with its server running, because a plugin install registers through it;
- `python3` on `PATH`, which the plugin runs on; and
- at least one supported editor launcher on `PATH`: `zed` for the `zed` adapter, `code` for the `vscode` adapter.

### Choices

The section offers these choices. The current record decides which apply:

- `Enable` (no record) or `Change editor` (a record exists): offer the adapters whose launcher readiness found. When exactly one is found, apply it without asking. Record the launcher's absolute path as `PATH` lookup returns it, without resolving symbolic links.
- `Disable` (a record exists): remove `editor` from the overlay. Do not uninstall the plugin; it is machine-wide, and other repositories may use it.

### Install

Before writing an `Enable` or `Change editor` record, bring the plugin to the release matching the current plugin version, the newest heading in [`migrations.md`](migrations.md). The interactive answer authorizes this install; ask no separate question. Read the installed state with `herdr plugin list --plugin valcraft-navigation --json`:

- Not installed, or installed from GitHub at another `requested_ref`: run `herdr plugin install valzav/valcraft/navigation/herdr --ref v<version> --yes`.
- Installed from GitHub at `v<version>`: install nothing.
- Linked from a local path (`source.kind` is `local`): leave it in place and name it in the report as a development copy.

When readiness fails, or the install command fails, write no `editor` record. Report the failure and the exact command run.

### Report

After an `Enable` or `Change editor` write, report the record, the plugin's installed source and release, and these key bindings for the operator to add to Herdr's `config.toml`. A plugin manifest cannot bind keys, and Tune never edits Herdr's configuration:

```toml
[[keys.command]]
key = "prefix+t"
type = "plugin_action"
command = "valcraft-navigation.pick"
description = "Valcraft: pick a reference from the pane"

[[keys.command]]
key = "prefix+y"
type = "plugin_action"
command = "valcraft-navigation.open-selection"
description = "Valcraft: open the selected reference"
```

State that the operator may choose other keys when these clash with their own bindings, then run `herdr server reload-config`. Name the pane picker as the main way in: `open-selection` needs a selection made in Herdr's copy mode, because Herdr clears a mouse selection on the key press.
