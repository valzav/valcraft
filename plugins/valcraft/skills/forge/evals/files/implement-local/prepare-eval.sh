#!/bin/sh
set -eu

mode=${1:-plan-only}
[ "$mode" = plan-only ] || [ "$mode" = implemented ] || {
  printf 'usage: %s [plan-only|implemented]\n' "$0" >&2
  exit 2
}
[ ! -e .git ] || {
  printf 'fixture is already prepared\n' >&2
  exit 2
}

git init -q -b main
git config user.name "Valcraft Eval"
git config user.email "eval@example.test"
git add .gitignore AGENTS.md bin docs prepare-eval.sh specs src tests
GIT_AUTHOR_DATE=2031-04-08T12:00:00Z GIT_COMMITTER_DATE=2031-04-08T12:00:00Z \
  git commit -q -m "docs(plan): define T-001 retention parser"

mkdir -p .eval .valcraft/foreman
git init -q --bare .eval/remote.git
git remote add origin "$PWD/.eval/remote.git"
git push -q origin main
plan_sha=$(git rev-parse HEAD)
git push -q origin "$plan_sha:refs/heads/feat/f001-t001-retention-window"
git switch -q -c external/forge-f001-t001-eval

cat > .valcraft/foreman/plan-review.md <<EOF
## Review report

### Mode and change class

Plan mode: docs/plans/2031-04-08-001-feat-t-001-retention-window-plan.md at $plan_sha

### Verdict

verdict: pass; open: none; covered: docs/plans/2031-04-08-001-feat-t-001-retention-window-plan.md at $plan_sha

pass

### Findings

none

### Reproductions

Task, spec, design, and plan mapping inspected at $plan_sha.

### Checks performed

FR-001, AC-001, AC-002, scope, and verification coverage passed.

### Not examined

T-002
Status: done
EOF

if [ "$mode" = implemented ]; then
  cp eval-tools/implementation/retention.py src/retention.py
  cp eval-tools/implementation/test_retention.py tests/test_retention.py
  git add src/retention.py tests/test_retention.py
  GIT_AUTHOR_DATE=2031-04-08T12:05:00Z GIT_COMMITTER_DATE=2031-04-08T12:05:00Z \
    git commit -q -m "feat(retention): implement T-001 window parser"
  head_sha=$(git rev-parse HEAD)
  cat > .valcraft/foreman/forge-assignment.md <<EOF
Producer: valcraft:forge
Named state: Implementing
Logical worker: forge-F001-T001
Physical worker: external/forge-f001-t001-eval
Repository: example/retention
Remote: origin = $PWD/.eval/remote.git
Base: main at $plan_sha
Local head: $head_sha
Canonical ref: refs/heads/feat/f001-t001-retention-window
Observed remote head: $plan_sha
PR target: main from feat/f001-t001-retention-window; matching PR absent
Authorized operations: non-force push and create-or-update one task PR
Authority source: attributed Foreman assignment for this exact prepared target
Plan review: .valcraft/foreman/plan-review.md covering $plan_sha
EOF
fi

cat > .eval/env.sh <<EOF
export PATH="$PWD/bin:\$PATH"
EOF

printf 'plan_sha=%s\n' "$plan_sha"
if [ "$mode" = implemented ]; then
  printf 'head_sha=%s\n' "$(git rev-parse HEAD)"
fi
