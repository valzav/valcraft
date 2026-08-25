#!/bin/sh
set -eu

[ ! -e .git ] || {
  printf 'fixture is already prepared\n' >&2
  exit 2
}

git init -q -b dev
git config user.name "Valcraft Eval"
git config user.email "eval@example.test"
git add -A
GIT_AUTHOR_DATE=2026-08-16T09:00:00Z GIT_COMMITTER_DATE=2026-08-16T09:00:00Z \
  git commit -q -m "chore(fixture): cast baseline"

# `.valcraft/config.yaml` names `dev` as the default branch and `main` as the
# release branch. Both must exist: Foreman refuses to substitute the release
# branch for a missing default branch, and blocks instead.
git branch main

# No remote. These fixtures are local-only projects, so Foreman records
# default-branch reconciliation as not applicable rather than attempting it.

printf 'dev_head=%s\n' "$(git rev-parse dev)"
