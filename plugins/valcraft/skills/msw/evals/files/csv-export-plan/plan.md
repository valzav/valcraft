# Plan: CSV export for the orders table

## Why this matters

Enterprise customers have been asking for raw data access for two quarters. Exports are
consistently the top request in the quarterly survey, and shipping this will materially
improve renewal conversations. A team that ships what customers ask for builds trust,
and trust compounds.

Exports also open the door to future analytics integrations, which the sales team is
excited about.

## Requirements

The export must stream rows rather than buffering the whole table in memory.

## Steps

1. Add the `GET /orders/export.csv` endpoint.
2. Stream rows from the database cursor directly into the HTTP response. Remember that
   the response must be streamed, not buffered.
3. Add an integration test proving a full round-trip: insert fixture orders, download
   the CSV, parse it, and compare against the fixtures.

## Notes

- Streaming is required here: do not load the full orders table into memory before
  writing the response.
- Double-check your work thoroughly before finishing.
