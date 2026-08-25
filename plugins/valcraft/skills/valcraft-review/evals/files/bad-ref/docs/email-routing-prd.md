# PRD: Support email routing

## Problem

Support email arrives in one shared inbox with no indication of which workspace the sender belongs to. Agents open each message and search manually.

## What we want

An incoming support email is routed to the workspace that owns the sender's email domain. Mail from a domain no workspace has claimed goes to an unrouted queue where an agent can triage it, rather than being dropped.

## Out of scope

- Outbound reply routing.
- Per-agent assignment inside a workspace.
