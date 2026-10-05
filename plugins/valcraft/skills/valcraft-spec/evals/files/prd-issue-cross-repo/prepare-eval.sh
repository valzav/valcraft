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
GIT_AUTHOR_DATE=2026-09-20T09:00:00Z GIT_COMMITTER_DATE=2026-09-20T09:00:00Z \
  git commit -q -m "chore(fixture): baseline project state"

git switch -q -c spec/f001-bulk-tagging
git add specs/001-bulk-tagging
GIT_AUTHOR_DATE=2026-09-20T10:00:00Z GIT_COMMITTER_DATE=2026-09-20T10:00:00Z \
  git commit -q -m "docs(spec): add FEAT-001 bulk tagging triplet"

printf 'main_head=%s\n' "$(git rev-parse main)"
printf 'spec_head=%s\n' "$(git rev-parse HEAD)"
