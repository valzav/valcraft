---
feature: FEAT-001
status: draft
created: 2026-08-16
updated: 2026-08-16
---

# Design: Invite links

`invite_links(id, workspace_id, token, expires_at)`; `create_link(workspace_id, now) -> Link` sets `expires_at = now + 7 days` (FR-003). `use_link(token, now) -> Membership` rejects `now >= expires_at` with `ExpiredInvite` before any write (AC-002).
