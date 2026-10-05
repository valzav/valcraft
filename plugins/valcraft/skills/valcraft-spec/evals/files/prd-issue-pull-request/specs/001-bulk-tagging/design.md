---
feature: FEAT-001
status: draft
created: 2026-09-20
updated: 2026-09-20
---

# Design: Bulk tagging

## Summary

A bulk-tag command inserts one tag link per selected record that lacks it, inside one transaction, and returns the number of links inserted. This satisfies FR-001, FR-002, FR-003, AC-001, and AC-002.

## Test strategy

- TS-001 (AC-001, FR-002): an integration test tags a selection that mixes tagged and untagged records, then counts tag links per record. Guarded defect: an insert that ignores existing links. Failing input: a selection containing a record that already carries the tag, which then carries it twice. Positive control: every record carries exactly one link. Domain: selections of untagged records, already-tagged records, and both, enumerated completely.
- TS-002 (AC-002, FR-003, edge case): the same test asserts the returned count, including a selection where every record already carries the tag. Guarded defect: a count of selected records instead of inserted links. Failing input: a fully tagged selection reporting a nonzero count. Positive control: the count equals the number of untagged selected records. Domain: the same three selection classes, enumerated completely.
