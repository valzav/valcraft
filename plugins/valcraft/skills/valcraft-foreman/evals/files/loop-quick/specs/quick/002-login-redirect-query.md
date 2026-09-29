---
id: Q-002
created: 2026-08-14
---

# Sign-in redirect keeps the export link's query string

## Sources

- operator request, 2026-08-14

## Requirements

- FR-001: When a signed-out administrator opens an export download link, the system MUST record the full requested URL, query string included, as the post-login return target.
- AC-001: After signing in, the administrator lands on the same link with the same query string and the download proceeds.

## Approach

In the export download route's login redirect, build the return target from path and query and encode it as a parameter on the login URL; sign-in completion redirects to the decoded target. Same-origin relative references only; sign-in itself is untouched.

## Verification

- TS-001 (AC-001): Observation: a test client, signed out, requests `/exports/42/download?format=csv&range=2026-08`, follows the redirect to sign-in, completes sign-in, and asserts that the final request is `/exports/42/download?format=csv&range=2026-08` and returns the CSV body. Guarded defect: a return target built from the path alone, or a target placed on the login URL without encoding, so its `&` ends the parameter early. Failing input: the two-parameter link above; a path-only target loses the whole query, and an unencoded target loses `range=2026-08`. Positive control: the redirect that encodes path and query as one parameter passes. Domain: same-origin export download links; the query travels as one encoded value, so a query with two parameters and a reserved `&` exercises both defects.

## Tasks

- [ ] QT-001 Carry path and query through the sign-in redirect; verifies AC-001; blocked by Q-001 QT-001.
