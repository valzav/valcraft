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
GIT_AUTHOR_DATE=2026-09-28T09:00:00Z GIT_COMMITTER_DATE=2026-09-28T09:00:00Z \
  git commit -q -m "FEAT-001: specify status legend feature contract"

printf 'spec_head=%s\n' "$(git rev-parse HEAD)"
