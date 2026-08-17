run: run-partial-batch
task: FEAT-001 T-002 (issue #42)
step: 10 (merge and close) — merged; closing batch partially executed
pr: #15 → dev, merged 2026-08-16 (`gh pr merge 15 --repo github.com/example/loop-github --squash --delete-branch` → ok)
closing batch (recorded before execution):
  1. `gh issue close 42 --repo github.com/example/loop-github --comment "Merged in PR #15 (T-002)."` → executed, ok
  2. `gh issue edit 42 --repo github.com/example/loop-github --remove-label in-progress` → FAILED: HTTP 502 from api.github.com
batch stopped after operation 2 failed.
