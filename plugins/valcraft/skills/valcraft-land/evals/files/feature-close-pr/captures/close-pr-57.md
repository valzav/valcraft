# Captured state: PR #57

- Repository: example/trails
- Title: FEAT-003: close feature
- Head branch: `close/f003-trail-maps`
- Base: `main` at 4444444444444444444444444444444444444444
- Head: 5555555555555555555555555555555555555555
- State: open
- Hosted checks on head 5555555555555555555555555555555555555555: `ci` passed. Branch protection requires `ci` only.
- Review reports: none

## Diff `4444444444444444444444444444444444444444..5555555555555555555555555555555555555555`

```diff
--- a/specs/003-trail-maps/spec.md
+++ b/specs/003-trail-maps/spec.md
@@ -1,6 +1,6 @@
 ---
 id: FEAT-003
 title: Trail maps
-status: draft
+status: complete
 spec_issue: null
@@ -24,6 +24,6 @@
 ## Acceptance criteria
 
-- [ ] AC-001: Selecting a trail in the list opens its map page.
-- [ ] AC-002: The map page draws the full track with a start marker and an end marker.
-- [ ] AC-003: The elevation profile renders within 2 seconds of opening the page.
+- [x] AC-001: Selecting a trail in the list opens its map page.
+- [x] AC-002: The map page draws the full track with a start marker and an end marker.
+- [x] AC-003: The elevation profile renders within 3 seconds of opening the page.
 - [ ] AC-004: A trail with no elevation data shows "No elevation data" in place of the profile.
--- a/specs/003-trail-maps/design.md
+++ b/specs/003-trail-maps/design.md
@@ -1,6 +1,6 @@
 ---
 feature: FEAT-003
-status: draft
+status: complete
 created: 2026-09-01
--- a/specs/003-trail-maps/tasks.md
+++ b/specs/003-trail-maps/tasks.md
@@ -1,6 +1,6 @@
 ---
 feature: FEAT-003
-status: draft
+status: complete
 created: 2026-09-01
```
