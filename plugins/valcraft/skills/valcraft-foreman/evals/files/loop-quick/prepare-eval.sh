#!/bin/sh
set -eu

[ ! -e .git ] || {
  printf 'fixture is already prepared\n' >&2
  exit 2
}

git init -q -b dev
git config user.name "Valcraft Eval"
git config user.email "eval@example.test"
git config commit.gpgsign false

# The Spec Review report under .valcraft/reviews/ is gitignored and covers
# specs/quick/002-login-redirect-query.md at this commit.
git add .gitignore AGENTS.md .valcraft/config.yaml docs specs prepare-eval.sh invalid-project
GIT_AUTHOR_DATE=2026-08-14T09:00:00Z GIT_COMMITTER_DATE=2026-08-14T09:00:00Z \
  git commit -q -m "chore(fixture): cast baseline with quick pool"

# `.valcraft/config.yaml` names `dev` as the default branch and `main` as the
# release branch. Both must exist.
git branch main

# No git remote. Foreman records default-branch reconciliation as not
# applicable rather than attempting it.

printf 'dev_head=%s\n' "$(git rev-parse dev)"
