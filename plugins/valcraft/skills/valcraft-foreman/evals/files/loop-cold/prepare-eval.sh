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

# T-001's implementation is the baseline that design.md's verified baseline
# assumption cites.
git add .gitignore AGENTS.md .valcraft/config.yaml docs prepare-eval.sh src tests
GIT_AUTHOR_DATE=2026-08-16T09:00:00Z GIT_COMMITTER_DATE=2026-08-16T09:00:00Z \
  git commit -q -m "feat(invites): FEAT-001 T-001 add Link record and create_link"

# The Spec Review report under .valcraft/reviews/ is gitignored and covers
# the triplet at this commit.
git add specs
GIT_AUTHOR_DATE=2026-08-16T10:00:00Z GIT_COMMITTER_DATE=2026-08-16T10:00:00Z \
  git commit -q -m "docs(spec): FEAT-001 invite links contract"

# `.valcraft/config.yaml` names `dev` as the default branch and `main` as the
# release branch. Both must exist.
git branch main

# No remote. This fixture is a local-only project, so Foreman records
# default-branch reconciliation as not applicable rather than attempting it.

printf 'baseline=%s\n' "$(git rev-parse dev~1)"
printf 'dev_head=%s\n' "$(git rev-parse dev)"
