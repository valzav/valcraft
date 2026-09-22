#!/bin/sh
# Stop hook for a Valcraft controller session on Claude Code.
#
# Blocks the end of a turn in the two cases where the skill contract says
# continue and nothing would wake the session again:
#   1. the Foreman controller that holds the Herdr lease stops with no armed
#      await and no gate or completion recorded (loop.md, "Ending a turn");
#   2. a Cast run stops on a nested Tune report, leaving the base uncommitted.
# Every other session may stop, and so may any state this script cannot read.
#
# stdin: the Stop hook payload as compact JSON, which the patterns below rely
# on. stdout: one block decision, or nothing to allow the stop.

in=$(cat)

# Nudge once per stop sequence. Claude Code sets this flag after a block.
case "$in" in *'"stop_hook_active":true'*) exit 0 ;; esac

root=$(git -C "${CLAUDE_PROJECT_DIR:-.}" rev-parse --show-toplevel 2>/dev/null) || exit 0
[ -d "$root/.valcraft" ] || exit 0

# Reasons are fixed strings: nothing read from disk reaches the JSON output.
block() {
	printf '{"decision":"block","reason":"%s"}' "$1"
	exit 0
}

# The lease holder is the highest-numbered controller.lock.<n> (herdr.md).
lease=""
highest=-1
for f in "$root"/.valcraft/foreman/controller.lock.*; do
	[ -f "$f" ] || continue
	n=${f##*.}
	case "$n" in '' | *[!0-9]*) continue ;; esac
	if [ "$n" -gt "$highest" ]; then
		highest=$n
		lease=$f
	fi
done

# The lease records the controller's agent_session, which Herdr reads from
# Claude Code's session id. A worker, an unrelated session, and a Cast run
# beside the lease of an interrupted Foreman run are not the owner.
owner=no
if [ -n "$lease" ]; then
	[ -r "$lease" ] || exit 0
	for id in $(grep -oE '[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}' "$lease"); do
		case "$in" in *"\"session_id\":\"$id\""*) owner=yes ;; esac
	done
fi

if [ "$owner" = no ]; then
	# Cast check. A direct Tune run commits the base, and Cast's own
	# "Status: done" follows its baseline commit. An uncommitted base under a
	# final "Status: done" means a nested Tune report ended the turn.
	ending=$(printf '%s' "$in" |
		sed -E -n 's/.*"last_assistant_message":"(([^"\\]|\\.)*)".*/\1/p' |
		sed -E 's/(\\n|\\r|[[:space:]`*])+$//')
	case "$ending" in *'Status: done') ;; *) exit 0 ;; esac
	[ -n "$(git -C "$root" status --porcelain -- .valcraft/config.yaml 2>/dev/null)" ] || exit 0
	block "The turn ended on Status: done while .valcraft/config.yaml is uncommitted. If a Cast run is active in this session, that line closed the nested Tune report, which is an intermediate result: continue the Cast run with fact gathering in this turn."
fi

# An armed await will wake the controller. Only a shell task's command counts:
# the final message and a task description are free text that can name the
# wait without arming it. A quote inside either is escaped, so the bare key
# below occurs only where Claude Code writes it.
case "$(printf '%s' "$in" | grep -oE '"command":"([^"\\]|\\.)*"')" in
*'herdr agent wait'*) exit 0 ;;
esac

# Before this controller's first checkpoint, the only reason to stop is the
# takeover confirmation, which waits on the operator.
state=$(ls -t "$root"/.valcraft/foreman/*/state.md 2>/dev/null | head -n 1)
[ -n "$state" ] || exit 0
[ "$state" -nt "$lease" ] || exit 0

# A checkpoint this script cannot read is not evidence of a missing line.
turn_end=$(awk '
  /^## CP-/ { line = "" }
  /^[[:space:]]*([-*][[:space:]]+)?`?Turn end: / { line = $0 }
  END { print line }
' "$state" 2>/dev/null) || exit 0
case "$turn_end" in
*'Turn end: gate '* | *'Turn end: complete'*) exit 0 ;;
*'Turn end: await '*)
	# Without a task list the recorded await cannot be checked.
	case "$in" in *'"background_tasks":'*) ;; *) exit 0 ;; esac
	;;
esac

block "This session holds the Foreman controller lease, no herdr agent wait is armed, and the latest state.md checkpoint records no open gate or completed run. Perform the next transition in loop.md now. If the turn must end, first append the Turn end line that loop.md requires."
