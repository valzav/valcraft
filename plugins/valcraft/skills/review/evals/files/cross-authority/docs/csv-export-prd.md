# PRD: Bounded CSV export

## Problem

Analysts export report data to CSV. A large export holds a connection against the shared
reporting database long enough that other workspaces' report queries slow down or time
out. We have had three incidents traced to a single unbounded export.

## What we want

An analyst exports a report to CSV and gets a file, without any one export being able to
degrade the shared database.

The export is capped at 500 rows. That number comes from the incident review: 500 rows is
the largest export that completed inside the connection budget in every incident we
measured. When the cap truncates a result, the analyst must be told, in the file itself,
that they are not looking at the whole report.

## Out of scope

- Asynchronous or emailed exports for large reports. If an analyst needs more than the
  cap, that is a separate feature.
- Formats other than CSV.
