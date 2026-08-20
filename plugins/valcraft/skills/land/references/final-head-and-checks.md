# Final head and checks

Use this gate for every task, spec, and retrospective PR. It controls both merge and any closure that depends on a merge.

## Exact Review coverage

Read the current PR head from the hosting service. Compare it with the exact head in the latest passing Review report for this target. A branch name, older verdict, merge base, or review summary is not coverage.

When the heads differ, inspect the complete `<reviewed>..<current>` delta. Only the exact unchecked-to-checked transition of the selected local feature task or quick task may bypass another scoped Review. The exception contains no adjacent text, rename, generated output, merge, or other change.

For that exact tick:

1. prepare a task-owned commit on the PR branch;
2. obtain exact push authority;
3. push without force;
4. re-read the PR head; and
5. classify applicable checks on that new head.

Any other delta returns `review_required` with the two full SHAs and exact delta target. After a Review-driven change, restart this comparison.

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

Only `passing` and `none-applicable` satisfy the gate. While an applicable check is pending, keep the current Land run active and recheck the same head; emit no terminal Land report or user-status gate. A backend `wait_timeout` is nonterminal and changes no Land state. A failed check enters the ownership classifier below. `missing-required` returns `missing_required_check` until authoritative evidence explains the missing trigger.

For a failed or missing check, record target kind, evidence, causal owner, and retryability. Route only when evidence proves ownership:

- task PR → `check_failure_task` for Forge;
- spec PR → `check_failure_spec` for Spec or its direct caller;
- retrospective PR → `check_failure_retro` for Temper.

External, configuration, and unresolved failures return `external_blocked`. Never infer an artifact owner from the target kind alone.

The merge gate passes only when Review covers the exact final head, or the exact completion-tick exception applies, and the state is `passing` or `none-applicable`.
