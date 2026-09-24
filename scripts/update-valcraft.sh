#!/bin/sh
# Update an installed Valcraft plugin in every coding-agent CLI that has it.
#
# Runs the update commands from the README's "Updating" section for each
# harness whose CLI is on PATH and already has the `valcraft` marketplace.
# It never adds a marketplace or installs a plugin that is not there.
#
# Usage: sh scripts/update-valcraft.sh [--dry-run]
#   --dry-run  print the commands instead of running them

set -u

dry_run=0
case "${1:-}" in
--dry-run) dry_run=1 ;;
"") ;;
-h | --help)
	/usr/bin/sed -n '2,10p' "$0" | /usr/bin/sed 's/^# \{0,1\}//'
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

have() { command -v "$1" >/dev/null 2>&1; }

# Claude Code: refresh the marketplace, then update the installed plugin.
if have claude && claude plugin list 2>/dev/null | grep -q 'valcraft@valcraft'; then
	printf 'Claude Code\n'
	if run claude plugin marketplace update valcraft && run claude plugin update valcraft@valcraft; then
		note "Claude Code: restart open sessions"
	else
		failed="$failed claude"
	fi
else
	printf 'Claude Code: skipped, no valcraft@valcraft installed\n'
fi

# Codex: refresh the Git marketplace snapshot, then reinstall from it.
if have codex && codex plugin marketplace list 2>/dev/null | grep -q '^valcraft[[:space:]]'; then
	printf 'Codex\n'
	if run codex plugin marketplace upgrade valcraft && run codex plugin add valcraft@valcraft; then
		note "Codex: start a new session"
	else
		failed="$failed codex"
	fi
else
	printf 'Codex: skipped, no valcraft marketplace configured\n'
fi

# Cursor: the CLI can only re-index the marketplace; the plugin itself is
# updated from the Plugins UI.
if have agent && agent plugin marketplace list 2>/dev/null | grep -q '^valcraft[[:space:]]'; then
	printf 'Cursor\n'
	if run agent plugin marketplace update valcraft; then
		note "Cursor: update valcraft in the Plugins UI"
	else
		failed="$failed cursor"
	fi
else
	printf 'Cursor: skipped, no valcraft marketplace configured\n'
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
