#!/bin/sh
set -eu

physical=external/draft-f001-t002-9f31

if [ ! -e .git ]; then
  git init -q -b main
  git config user.name "Valcraft Eval"
  git config user.email "eval@example.test"
  git config commit.gpgsign false
  git config core.fileMode false
  git config core.autocrlf false
  git add -A
  GIT_AUTHOR_DATE=2026-08-10T09:00:00Z GIT_COMMITTER_DATE=2026-08-10T09:00:00Z \
    git commit -q -m "chore(fixture): baseline project state"
  printf 'main_head=%s\n' "$(git rev-parse HEAD)"
elif [ "${1:-}" != external ] || git rev-parse -q --verify "refs/heads/$physical" >/dev/null; then
  printf 'fixture is already prepared\n' >&2
  exit 2
fi

if [ "${1:-}" = external ]; then
  git switch -q -c "$physical" main
  printf 'physical_branch=%s\n' "$physical"
  printf 'predecessor=%s\n' "$(git rev-parse HEAD)"
fi
