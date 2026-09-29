#!/bin/sh
set -eu

[ ! -e .git ] || {
  printf 'fixture is already prepared\n' >&2
  exit 2
}

git init -q -b trunk
git config user.name "Valcraft Eval"
git config user.email "eval@example.test"
git config commit.gpgsign false
git config core.fileMode false
git config core.autocrlf false
git add .gitignore AGENTS.md .valcraft/config.yaml docs specs/.gitkeep prepare-eval.sh
GIT_AUTHOR_DATE=2026-08-01T09:00:00Z GIT_COMMITTER_DATE=2026-08-01T09:00:00Z \
  git commit -q -m "chore(fixture): baseline project state"

git remote add origin https://github.example.test/example/records.git
git update-ref refs/remotes/origin/main HEAD
git symbolic-ref refs/remotes/origin/HEAD refs/remotes/origin/main

printf 'trunk_head=%s\n' "$(git rev-parse trunk)"
