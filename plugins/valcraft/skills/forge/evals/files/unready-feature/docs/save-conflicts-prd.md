# PRD: Save conflict detection

## Problem

Two members editing the same document at once silently overwrite each other. The member
whose work disappeared usually does not notice until much later, and we cannot recover it.

## What we want

When a member saves a document that changed underneath them since they loaded it, the save
is refused and they are told why, instead of one person's work being overwritten.

## Open question for the team

When a save is refused, we have not decided whether to keep the member's unsaved text so
they can re-apply it, or to discard it and reload the current version. Keeping it is
kinder but means holding an unsaved buffer; discarding it is simpler but throws away work
the member just typed. This needs a decision before build.

## Out of scope

- Real-time collaborative editing or merge.
- Version history browsing.
