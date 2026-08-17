---
id: Q-002
created: 2026-08-14
---

# Sign-in redirect keeps the export link's query string

## Sources

- operator request, 2026-08-14

## Requirements

- FR-001: When a signed-out administrator opens an export download link, the system MUST
  record the full requested URL, query string included, as the post-login return target.
- AC-001: After signing in, the administrator lands on the same link with the same query
  string and the download proceeds.

## Approach

In the export download route's login redirect, build the return target from path and
query and encode it as a parameter on the login URL; sign-in completion redirects to the
decoded target. Same-origin relative references only; sign-in itself is untouched.

## Tasks

- [ ] T-001 Carry path and query through the sign-in redirect; verifies AC-001.
