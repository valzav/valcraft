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
git config core.autocrlf false
git add .gitignore AGENTS.md .valcraft/config.yaml docs prepare-eval.sh
GIT_AUTHOR_DATE=2026-08-01T09:00:00Z GIT_COMMITTER_DATE=2026-08-01T09:00:00Z \
  git commit -q -m "chore(fixture): baseline project state"

git switch -q -c spec/f001-saved-filters
git add specs/001-saved-filters
GIT_AUTHOR_DATE=2026-08-01T10:00:00Z GIT_COMMITTER_DATE=2026-08-01T10:00:00Z \
  git commit -q -m "docs(spec): add FEAT-001 saved filters triplet"

printf 'main_head=%s\n' "$(git rev-parse main)"
printf 'spec_head=%s\n' "$(git rev-parse HEAD)"
