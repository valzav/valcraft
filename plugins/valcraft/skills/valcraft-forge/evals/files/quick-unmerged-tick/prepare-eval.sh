#!/bin/sh
set -eu

[ ! -e .git ] || {
  printf 'fixture is already prepared\n' >&2
  exit 2
}

git init -q -b main
git config user.name "Valcraft Eval"
git config user.email "eval@example.test"
git add .gitignore .valcraft/config.yaml AGENTS.md docs prepare-eval.sh specs src tests
GIT_AUTHOR_DATE=2026-08-12T09:00:00Z GIT_COMMITTER_DATE=2026-08-12T09:00:00Z \
  git commit -q -m "chore(fixture): baseline project state"
main_head=$(git rev-parse HEAD)

# QT-001 implemented by an earlier Forge run, pushed for Review, not yet merged.
git switch -q -c feat/q001-qt001-validation-hardening
cp eval-tools/qt001/validation.py src/validation.py
cp eval-tools/qt001/test_validation.py tests/test_validation.py
sed 's/^- \[ \] QT-001 /- [x] QT-001 /' specs/quick/001-validation-hardening.md > .git/quick.md
mv .git/quick.md specs/quick/001-validation-hardening.md
git add src/validation.py tests/test_validation.py specs/quick/001-validation-hardening.md
GIT_AUTHOR_DATE=2026-08-12T10:00:00Z GIT_COMMITTER_DATE=2026-08-12T10:00:00Z \
  git commit -q -m "fix(validation): reject whitespace-only values (Q-001/QT-001)"

printf 'main_head=%s\n' "$main_head"
printf 'task_head=%s\n' "$(git rev-parse HEAD)"
