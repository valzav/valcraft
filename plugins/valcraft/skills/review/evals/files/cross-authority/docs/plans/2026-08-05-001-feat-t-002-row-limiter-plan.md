# Plan: T-002 row limiter

Implements T-002 (verifies FR-002) for FEAT-001.

## Approach

Add a `RowLimiter` wrapper around the report row iterator. The limiter counts rows as
they stream and stops the iterator once the configured maximum is reached, then appends
one truncation notice row to the CSV body.

Per `specs/001-csv-export/design.md`, the maximum is 5000 rows. The limit is a module
constant, `EXPORT_ROW_CAP = 5000`, so a later feature can make it configurable.

## Verification

- Unit test: a 4999-row report streams every row and appends no notice.
- Unit test: a 5001-row report streams 5000 rows and appends the notice.
- Integration test: `GET /reports/{id}/export.csv` on a large fixture report returns a
  body whose final line is the truncation notice.

## Assumptions

- The reporting fixture database starts empty, so each test seeds its own rows.
