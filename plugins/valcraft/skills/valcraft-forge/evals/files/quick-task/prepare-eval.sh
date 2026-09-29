#!/bin/sh
set -eu

[ ! -e .git ] || {
  printf 'fixture is already prepared\n' >&2
  exit 2
}

git init -q -b main
git config user.name "Valcraft Eval"
git config user.email "eval@example.test"
git add .gitignore .valcraft/config.yaml AGENTS.md docs prepare-eval.sh specs src tests
GIT_AUTHOR_DATE=2026-08-12T09:00:00Z GIT_COMMITTER_DATE=2026-08-12T09:00:00Z \
  git commit -q -m "chore(fixture): baseline project state"

printf 'main_head=%s\n' "$(git rev-parse HEAD)"
