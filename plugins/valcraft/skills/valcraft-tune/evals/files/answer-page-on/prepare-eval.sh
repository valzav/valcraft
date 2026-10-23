#!/bin/sh
set -eu

[ ! -e .git ] || {
  printf 'fixture is already prepared\n' >&2
  exit 2
}

git init -q -b main
git config user.name "Valcraft Eval"
git config user.email "eval@example.test"
git add -A
GIT_AUTHOR_DATE=2026-10-22T09:00:00Z GIT_COMMITTER_DATE=2026-10-22T09:00:00Z \
  git commit -q -m "chore(fixture): answer page on for everyone"

printf 'main_head=%s\n' "$(git rev-parse main)"
