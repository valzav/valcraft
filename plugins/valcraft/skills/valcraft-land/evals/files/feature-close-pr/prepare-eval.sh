#!/bin/sh
set -eu

[ ! -e .git ] || {
  printf 'fixture is already prepared\n' >&2
  exit 2
}

# An empty repository keeps git commands inside the fixture; the prompt supplies the default-branch head.
git init -q -b main
printf 'initialized empty repository; default-branch head comes from the prompt\n'
