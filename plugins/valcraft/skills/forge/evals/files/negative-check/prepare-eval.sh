#!/bin/sh
set -eu

[ $# -eq 0 ] || [ "$1" = plan-only ] || {
  printf 'usage: %s [plan-only]\n' "$0" >&2
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

mkdir -p .eval .foreman
git init -q --bare .eval/remote.git
git remote add origin "$PWD/.eval/remote.git"
git push -q origin main
plan_sha=$(git rev-parse HEAD)
git push -q origin "$plan_sha:refs/heads/feat/f001-t001-retention-window"
git switch -q -c external/forge-f001-t001-eval

cat > .foreman/plan-review.md <<EOF
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

FR-001, NFR-001, AC-001, AC-002, AC-004, scope, and verification coverage passed.

### Not examined

T-002
Status: done
EOF

cat > .eval/env.sh <<EOF
export PATH="$PWD/bin:\$PATH"
EOF

printf 'plan_sha=%s\n' "$plan_sha"
