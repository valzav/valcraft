# Final head and checks

Use this gate for every task, spec, and feature-close PR. It controls both merge and any closure that depends on a merge.

Merging any PR — task, spec, or feature-close — includes deleting its head branch; the merge grant covers the deletion. Reconcile an already-deleted branch as complete.

For the `squash` strategy, pass an explicit subject and body to the merge. The subject is the PR title followed by a space and `(#<PR number>)`. The body is the full message of each commit the PR contains at the merged head, in the order the host lists them. Never leave the message to the host default: the host can add lines that no PR commit carries, such as a `Co-authored-by` line when the commit author differs from the merging account. Record the subject and body with the merge under `Prepared operations`.

After the merge is verified, delete the local branch of the same name in the canonical checkout when its head equals the merged PR head. The merge grant covers this deletion too. When the clean canonical checkout has that branch checked out, delete it by first fast-forwarding the local default branch to the verified remote default head and switching the checkout to it. Switch the checkout only to delete that branch.

When the local branch's head differs from the merged PR head, it holds local commits the merge does not contain. Leave the branch and the checkout as they are, and name the branch with both heads under `Handoffs`. Leave a dirty checkout and its branch in place the same way.

## Merge and recovery

Use `pull_requests.merge_strategy` from the committed `.valcraft/config.yaml` for every PR: task, spec, and feature-close. Do not infer a strategy from host defaults or repository history. If the configured strategy is unavailable for the target repository, invoke Tune for the pull-request section, show only host-supported strategies, and resume only after `Status: done`. Never substitute another strategy.

Immediately before merge, re-read the PR identity, base, head, state, configured merge strategy, Review coverage, and check state. Under a ref-bound grant, also fetch the base ref and apply the base condition in [Ref-bound grant](#ref-bound-grant). Then verify the exact trusted target-bound authorization required by `SKILL.md`.

After any merge command error, inspect live PR state before deciding the merge failed. If authoritative state says merged, mark merge complete and advance to remaining closure. If it says open, preserve the exact error and return the remaining operation. A closed-unmerged PR stops task closure under the rule in [Target kinds](tracker-closure.md#target-kinds).

Persist or report enough state to resume: target kind, exact identifiers, prepared authorization fields, completed operations with authoritative locators, remaining operations, and last error. Never repeat a completed external mutation.

## Exact Review coverage

Read the current PR head from the hosting service. Compare it with the exact head in the latest passing Review report for this target. A branch name, older verdict, merge base, or review summary is not coverage.

A report whose verdict is not `pass` covers no head, including the exact current head. An operator decision, approval mode, or grant in the assignment is not coverage either. When no passing report covers the current head, return `review_required` naming the latest report, its verdict, and its open R-IDs.

When the heads differ, the current head lacks coverage. Return `review_required` with the two full SHAs and the exact `<reviewed>..<current>` delta target.

In `local` tracker mode a feature task, and in every mode a quick task, carries its exact unchecked-to-checked completion transition in the covered head: Forge commits it and Review covers it. Land adds no commit. Verify that the PR's delta contains that transition. When it does not, return `review_required` naming the missing transition.

A feature-close PR has no Review report. Its whole delta against its base must be exactly the completion marks `tracker-closure.md` defines for that feature: unchecked-to-checked `AC-` transitions in its `spec.md` and `status: draft` to `status: complete` in its three files. Such a delta needs no Review.

Any other feature-close delta returns `review_required` with the two full SHAs and exact delta target. After a Review-driven change, restart this comparison.

## Ref-bound grant

A Foreman dispatch may carry a ref-bound Land grant ([`../../valcraft-foreman/references/contracts.md`](../../valcraft-foreman/references/contracts.md#ref-bound-land-grant)). It binds the target fields and the operation set before you prepare, and binds the final head and the base head only by condition.

- **Final head.** For a task or spec PR, the final head is the covered head. For a feature close, it is a single commit that is exactly the feature-close marks, whose parent is the base head you observed when you cut the close branch. Record that base head under `Authoritative state`.
- **Base head, `squash` or `merge` strategy.** Immediately before merge, fetch the base ref and run `git merge-tree --write-tree <live base head> <final head>`. Exit 0 meets the condition: record the live base head under `Authoritative state` and merge. Exit 1 is a conflict: return `authority_drift` naming the conflicting paths from the command output, and mutate nothing. Any other exit, or a failed fetch, is a tool failure before any mutation: return `external_blocked`. The command requires Git 2.38 or later.
- **Base head, `rebase` strategy.** The base SHA is bound exactly. A moved base returns `authority_drift`, because a clean merge does not prove that each replayed commit applies cleanly.

Apply the grant when every bound field revalidates and both conditions hold. Then perform the granted operations in the same assignment without asking. Return `authority_drift` when a bound field changed. An operation outside the grant still ends `authority_required`. The grant changes neither the Review coverage rule nor the check classifier.

A host rule that requires the PR branch to be up to date with its base can reject a merge the base condition allows. Treat that rejection as a merge command error under [Merge and recovery](#merge-and-recovery); it is not drift.

## Applicable-check classifier

Query all applicable sources:

- the selected artifact's requirements;
- root and applicable repository rules;
- hosted required-check configuration; and
- workflows on the target branch or introduced by the PR.

Match every result to the exact current head. If a repository-rule, hosted-configuration, or applicable-workflow source is unavailable, return `check_source_unavailable` before assigning a state. Absence from the target branch alone does not prove that no workflow applies.

Record exactly one state:

- `passing` — every applicable configured or required check passed on the exact head;
- `pending/failing` — an applicable check is running or failed on the exact head;
- `missing-required` — an applicable configured or required check has no run on the exact head;
- `none-applicable` — every source was available and none configures or requires a check.

Only `passing` and `none-applicable` satisfy the gate. A check result comes only from the applicable sources above, matched to the exact head. Land never runs a test, typecheck, lint, or build itself: a local run is not an applicable-check source, cannot confirm or replace a hosted result, and changes no state. While an applicable check is pending, keep the current Land run active and recheck the same head. Emit no terminal Land report, and do not stop to ask the operator whether to keep waiting. A backend `wait_timeout` is nonterminal and changes no Land state. A failed check enters the ownership classifier below. `missing-required` returns `missing_required_check` until authoritative evidence explains the missing trigger.

For a failed or missing check, record target kind, evidence, causal owner, and retryability. Route only when evidence proves ownership:

- task PR → `check_failure_task` for Forge;
- spec PR → `check_failure_spec` for Spec;
- feature-close PR → `external_blocked`, because its delta carries only completion marks;

External, configuration, and unresolved failures return `external_blocked`. Never infer an artifact owner from the target kind alone.

The merge gate passes only when Review covers the exact final head, or the feature-close PR's delta is exactly the feature-close marks, and the state is `passing` or `none-applicable`.
