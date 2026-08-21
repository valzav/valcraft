#!/bin/sh
set -eu

[ ! -e .git ] || {
  printf 'fixture is already prepared\n' >&2
  exit 2
}

git init -q -b main
git config user.name "Valcraft Eval"
git config user.email "eval@example.test"

git add .gitignore AGENTS.md docs prepare-eval.sh specs
GIT_AUTHOR_DATE=2026-08-10T09:00:00Z GIT_COMMITTER_DATE=2026-08-10T09:00:00Z \
  git commit -q -m "docs(spec): define FEAT-001 record export"

git add src/export.py tests/test_export.py
GIT_AUTHOR_DATE=2026-08-12T09:00:00Z GIT_COMMITTER_DATE=2026-08-12T09:00:00Z \
  git commit -q -m "feat(export): FEAT-001 T-001 add record serialization"

git add src/report.py tests/test_report.py
GIT_AUTHOR_DATE=2026-08-14T09:00:00Z GIT_COMMITTER_DATE=2026-08-14T09:00:00Z \
  git commit -q -m "feat(export): FEAT-001 T-002 report written field count"

mkdir -p .eval
git init -q --bare .eval/remote.git
git remote add origin "$PWD/.eval/remote.git"
git push -q origin main

printf 'main_head=%s\n' "$(git rev-parse HEAD)"
printf 'remote=%s\n' "$PWD/.eval/remote.git"
