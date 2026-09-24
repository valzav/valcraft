#!/bin/sh
# Update an installed Valcraft plugin in every coding-agent CLI that has it.
#
# Runs the update commands from the README's "Updating" section for each
# harness that already has Valcraft: an installed plugin in Claude Code and
# Codex, the `valcraft` marketplace in Cursor. It never adds a marketplace or
# installs a plugin that is not there. A CLI that cannot report its state
# counts as a failure.
#
# Usage: sh scripts/update-valcraft.sh [--dry-run]
#   --dry-run  print the commands instead of running them

set -u

dry_run=0
case "${1:-}" in
--dry-run) dry_run=1 ;;
"") ;;
-h | --help)
	/usr/bin/sed -n '2,12p' "$0" | /usr/bin/sed 's/^# \{0,1\}//'
	exit 0
	;;
*)
	printf 'unknown argument: %s\n' "$1" >&2
	exit 2
	;;
esac

failed=""
next=""

note() {
	next="$next  - $1
"
}

run() {
	if [ "$dry_run" -eq 1 ]; then
		printf '  would run: %s\n' "$*"
		return 0
	fi
	printf '  $ %s\n' "$*"
	"$@"
}

fail() {
	failed="$failed
  - $1"
}

# found NAME PATTERN COMMAND...: succeed when COMMAND's output shows an
# installed Valcraft. A missing CLI or a non-matching listing is a skip; a
# listing command that fails is a failure, never a skip.
found() {
	name=$1
	pattern=$2
	shift 2
	if ! command -v "$1" >/dev/null 2>&1; then
		printf '%s: skipped, `%s` not on PATH\n' "$name" "$1"
		return 1
	fi
	if ! out=$("$@" 2>&1); then
		printf '%s: `%s` failed:\n%s\n' "$name" "$*" "$out" >&2
		fail "$name: could not read installed state"
		return 1
	fi
	if printf '%s\n' "$out" | grep -Eq "$pattern"; then
		printf '%s\n' "$name"
		return 0
	fi
	printf '%s: skipped, Valcraft not installed\n' "$name"
	return 1
}

# Claude Code: refresh the marketplace, then update the installed plugin.
if found "Claude Code" 'valcraft@valcraft' claude plugin list; then
	if run claude plugin marketplace update valcraft && run claude plugin update valcraft@valcraft; then
		note "Claude Code: restart open sessions"
	else
		fail "Claude Code: update failed"
	fi
fi

# Codex: refresh the Git marketplace snapshot, then reinstall from it. Gate on
# the installed-plugin listing, because `plugin add` would also install a
# plugin that was deliberately removed.
if found "Codex" '^valcraft@valcraft[[:space:]]+installed' codex plugin list; then
	if run codex plugin marketplace upgrade valcraft && run codex plugin add valcraft@valcraft; then
		note "Codex: start a new session"
	else
		fail "Codex: update failed"
	fi
fi

# Cursor: the CLI can only re-index the marketplace, which installs nothing;
# the plugin itself is updated from the Plugins UI.
if found "Cursor" '^valcraft[[:space:]]' agent plugin marketplace list; then
	if run agent plugin marketplace update valcraft; then
		note "Cursor: update valcraft in the Plugins UI"
	else
		fail "Cursor: marketplace update failed"
	fi
fi

printf '\n'
if [ -n "$next" ]; then
	printf 'Next steps:\n%s' "$next"
	printf '  - in each project, run Tune if the migration ledger lists a change it performs\n'
fi
if [ -n "$failed" ]; then
	printf 'Failed:%s\n' "$failed" >&2
	exit 1
fi
