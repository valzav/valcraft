# Migration notes

Each release lists what changes for a repository that already uses Valcraft, and what the operator must do. A release with no entry changes nothing an existing repository must contain. Newest first.

## v0.8.0

### Amendments no longer use a retained spec branch

Once a feature or quick contract is on the default branch, Spec amends it on the in-progress task's branch when the change is scoped to that task, or on a short-lived `spec/fNNN-amend-<sha>` branch cut from the default branch. Land deletes every merged head branch, including the initial `spec/fNNN-<slug>` branch. The landed-branch synchronization merge is removed.

- Action: delete any `spec/fNNN-<slug>` or `spec/qNNN-<slug>` branch still on the remote for an already-landed contract. Spec reports such a branch as stale and never touches it.
- Action: if branch protection forbids head-branch deletion, expect Land to report the deletion as a remaining operation after a successful merge.

### Readiness requires recorded baseline verification and criterion ownership

`design.md` must carry a `Verified baseline assumptions` section, and `tasks.md` must assign every substantive acceptance-criterion clause to a task. A landed triplet that predates this rule is unready.

- Action: none in advance. Foreman's intake routes each in-flight feature to Specifying once; the fix lands through an amendment branch, SpecReview, and SpecLanding before the next task is picked. Quick files are unaffected.

### Cast scaffolds a markdownlint configuration

A new or retrofitted frame includes `.markdownlint-cli2.jsonc`. An existing frame receives it only on a Cast retrofit.

- Action: none unless Cast is re-run on a repository that already carries its own markdownlint configuration; review the conflict then.

## v0.7.7

### Herdr worker configuration requires two new roles

`foreman.herdr.workers` must contain exactly ten roles: `spec` and `spec_review` are new beside the existing eight. The configuration is closed with no defaults, so an eight-role mapping fails validation in every skill. `spec` and `spec_review` must use different harnesses.

- Action: on the `herdr` backend, run Tune for the Foreman section and add both roles. Attended runs are offered the repair automatically; headless runs stop with `configuration_required` until it is done. The `subagents` and `ao` backends are unaffected.
