#!/bin/sh
set -eu

[ ! -e .git ] || {
  printf 'fixture is already prepared\n' >&2
  exit 2
}

git init -q -b main
git config user.name "Valcraft Eval"
git config user.email "eval@example.test"
git config commit.gpgsign false
git config core.fileMode false
git add -A
GIT_AUTHOR_DATE=2026-10-17T09:00:00Z GIT_COMMITTER_DATE=2026-10-17T09:00:00Z \
  git commit -q -m "docs(T-002): plan the game-over panel"

printf 'plan_head=%s\n' "$(git rev-parse HEAD)"
