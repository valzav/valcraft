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

git switch -q -c spec/f001-session-export
dir=specs/001-session-export
for file in spec.md design.md tasks.md; do
  blob=$(LC_ALL=C sed -e 's/^spec_issue: 20$/spec_issue: TBD/' -e 's/ → #3[12]$/ → TBD/' "$dir/$file" | git hash-object -w --stdin)
  git update-index --add --cacheinfo "100644,$blob,$dir/$file"
done
GIT_AUTHOR_DATE=2026-08-01T10:00:00Z GIT_COMMITTER_DATE=2026-08-01T10:00:00Z \
  git commit -q -m "docs(spec): add FEAT-001 session export triplet"

git add "$dir"
GIT_AUTHOR_DATE=2026-08-01T11:00:00Z GIT_COMMITTER_DATE=2026-08-01T11:00:00Z \
  git commit -q -m "docs(spec): record FEAT-001 tracker mappings"

printf 'main_head=%s\n' "$(git rev-parse main)"
printf 'triplet_head=%s\n' "$(git rev-parse HEAD~1)"
printf 'spec_head=%s\n' "$(git rev-parse HEAD)"
