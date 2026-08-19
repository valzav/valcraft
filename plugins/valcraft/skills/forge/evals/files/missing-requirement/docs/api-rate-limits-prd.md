# PRD: API rate limits

## Problem

A single workspace running a bulk script can consume most of our API capacity, slowing the product for every other workspace. This has caused two visible incidents.

## What we want

Each workspace gets a bounded share of API capacity. Requests are counted per workspace over a rolling window, and a workspace that goes over its share is refused rather than served, so it cannot keep consuming capacity other workspaces need.

## Still to decide

We have not agreed what a workspace's allowance should be, and it is not a value engineering should pick. It depends on the pricing tiers being finalized this quarter, and on what the traffic analysis says about normal usage. The same goes for what a refused request should look like to the caller.

## Out of scope

- Per-endpoint or per-token limits.
- Purchasable capacity increases.
