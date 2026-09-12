# Migrations

This ledger is the record of what each plugin release changes for a repository that already uses Valcraft, and the procedure Tune runs to bring such a repository up to date. Its newest `## vX.Y.Z` heading is the current plugin version; `scripts/check-migrations.py` keeps it equal to the manifests.

## Procedure

Run this flow when `config.md` classifies the base as `outdated`. Bare `/valcraft-tune` reaches it through that classification; a producer skill reaches it by delegating an invalid configuration to Tune.

1. Read `valcraft_version` from the base. An absent key is older than every entry.
2. Walk the release headings from the oldest one newer than the recorded version to the newest. Under each, evaluate every change's **Applies when** against the repository without mutating anything.
3. For each change whose condition holds, perform **Tune performs** using the question flow in `config.md` for any choice it names, and copy its **Operator** items into the report verbatim. A change whose condition does not hold is skipped and named as skipped in the report.
4. Set `valcraft_version` to the newest heading. Validate the complete candidate, write it, and commit it under `SKILL.md`'s single-path base commit.
5. Report every applied, skipped, and operator-owned item, then end with `Status: done`.

A migration whose applicable entries name no choice needs no interactive answer: the recorded version being older authorizes the version write and its single-path commit, in a direct or delegated run, attended or not. A change that needs an interactive answer in a noninteractive run ends with `configuration_required` and writes nothing. No change performs a push, merge, tracker mutation, or other outward operation; such work is always an **Operator** item with its exact command.

Entry shape: a `### <title>` heading, one paragraph stating what changed, then `Applies when:`, `Tune performs:` (`none` when the loop or the operator carries the change), and `Operator:` (`none` when no human action remains).

## v0.8.2

### Model catalog drops Luna and the xhigh and max efforts

Model aliases, effort sets, and Herdr presets moved to Tune's `references/models.md`. Codex gains `gpt-6-astra` as its most capable alias and drops `gpt-5.6-luna` as a known alias. No model accepts `xhigh` or `max` any longer. The presets changed: `Balanced` pairs Claude Opus at medium with Codex Sol at high, `Quality` pairs Claude Fable with Codex Astra at high, and `Economy` pairs Claude Sonnet at high with Codex Sol at medium.

- Applies when: the resolved `foreman.herdr.workers` map has a worker whose `effort` is `xhigh` or `max`, or whose `model` is `gpt-5.6-luna`.
- Tune performs: the Herdr worker questions from `config.md` for each affected role, harness kept, in the file that carries that worker entry; nothing else.
- Operator: none.

## v0.8.1

### Configuration records the migrated plugin version

`.valcraft/config.yaml` requires `valcraft_version`, and every skill delegates an outdated or absent value to Tune. This is the entry that bootstraps the ledger.

- Applies when: `valcraft_version` is absent from the base.
- Tune performs: the version write in step 4 of the procedure; nothing else.
- Operator: none.

## v0.8.0

### Amendments no longer use a retained spec branch

Once a feature or quick contract is on the default branch, Spec amends it on the in-progress task's branch when the change is scoped to that task, or on a short-lived `spec/fNNN-amend-<sha>` branch cut from the default branch. Land deletes every merged head branch, including the initial `spec/fNNN-<slug>` branch. The landed-branch synchronization merge is removed.

- Applies when: never on its own; Tune inspects no remote, so the operator checks the condition.
- Tune performs: none.
- Operator: list retained refs with `git ls-remote --heads origin 'spec/*'` and delete each `spec/fNNN-<slug>` or `spec/qNNN-<slug>` branch whose contract is already on the default branch, for example `git push origin --delete spec/f001-<slug>`. Spec reports the branch as stale and never touches it. If branch protection forbids head-branch deletion, expect Land to report the deletion as a remaining operation after a successful merge.

### Readiness requires recorded baseline verification and criterion ownership

`design.md` must carry a `Verified baseline assumptions` section, and `tasks.md` must assign every substantive acceptance-criterion clause to a task. A landed triplet that predates this rule is unready.

- Applies when: a feature triplet on the default branch has unfinished tasks and its `design.md` lacks `## Verified baseline assumptions`.
- Tune performs: none; the delivery loop carries the change.
- Operator: none in advance. Foreman's intake routes each such feature to Specifying once; the fix lands through an amendment branch, SpecReview, and SpecLanding before the next task is picked. Quick files are unaffected.

### Cast scaffolds a markdownlint configuration

A new or retrofitted frame includes `.markdownlint-cli2.jsonc`. An existing frame receives it only on a Cast retrofit.

- Applies when: never on its own; a Cast retrofit applies it.
- Tune performs: none.
- Operator: if Cast is re-run on a repository that already carries its own markdownlint configuration, review the conflict then.

## v0.7.7

### Herdr worker configuration requires two new roles

`foreman.herdr.workers` must contain exactly ten roles: `spec` and `spec_review` are new beside the existing eight. The configuration is closed with no defaults, so an eight-role mapping fails validation in every skill. `spec` and `spec_review` must use different harnesses.

- Applies when: the resolved backend is `herdr` and `workers` lacks `spec` or `spec_review`.
- Tune performs: ask harness, model, and effort for each missing role through the Custom role questions in `config.md`, with the preset harness for that role recommended, and reject a candidate where `spec` and `spec_review` share a harness. Write the result to the file that carries the `herdr` mapping.
- Operator: none beyond answering. The `subagents` and `ao` backends are unaffected.
