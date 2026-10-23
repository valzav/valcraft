#!/bin/sh
# Usage: ./prepare-eval.sh [absent] [overlay-off] [small] [attended]
#   absent       remove foreman.answer_page from the committed base
#   overlay-off  keep the base `true` and write an overlay with `false`
#   small        hold only two questions: T-004..T-006 have landed
#   attended     set the committed approval mode to attended
set -eu

[ ! -e .git ] || {
  printf 'fixture is already prepared\n' >&2
  exit 2
}

for variant in "$@"; do
  case "$variant" in
    absent)
      grep -v '^  answer_page:' .valcraft/config.yaml > .valcraft/config.yaml.new
      mv .valcraft/config.yaml.new .valcraft/config.yaml ;;
    overlay-off)
      printf 'foreman:\n  answer_page: false\n' > .valcraft/config.local.yaml ;;
    small)
      cp variants/small/specs/003-spend-alerts/tasks.md specs/003-spend-alerts/tasks.md
      cp variants/small/.valcraft/foreman/run-held/state.md .valcraft/foreman/run-held/state.md
      rm .valcraft/foreman/run-held/drafter-F003-T004-d000.md \
        .valcraft/foreman/run-held/drafter-F003-T005-d000.md \
        .valcraft/foreman/run-held/drafter-F003-T006-d000.md
      grep -v 'T-00[456]' .valcraft/foreman/run-held/workers.md > .valcraft/foreman/run-held/workers.md.new
      mv .valcraft/foreman/run-held/workers.md.new .valcraft/foreman/run-held/workers.md ;;
    attended)
      sed 's/^  approval_mode: unattended$/  approval_mode: attended/' .valcraft/config.yaml > .valcraft/config.yaml.new
      mv .valcraft/config.yaml.new .valcraft/config.yaml
      sed 's/^approval mode: unattended.*/approval mode: attended (base .valcraft\/config.yaml foreman.approval_mode)/' \
        .valcraft/foreman/run-held/state.md > .valcraft/foreman/run-held/state.md.new
      mv .valcraft/foreman/run-held/state.md.new .valcraft/foreman/run-held/state.md ;;
    *)
      printf 'unknown variant: %s\n' "$variant" >&2
      exit 2 ;;
  esac
done
rm -rf variants

git init -q -b dev
git config user.name "Valcraft Eval"
git config user.email "eval@example.test"
git add -A
GIT_AUTHOR_DATE=2026-10-22T09:00:00Z GIT_COMMITTER_DATE=2026-10-22T09:00:00Z \
  git commit -q -m "chore(fixture): spend alerts baseline"

# No remote. This fixture is a local-only project, so Foreman records
# default-branch reconciliation as not applicable rather than attempting it.

printf 'dev_head=%s\n' "$(git rev-parse dev)"
