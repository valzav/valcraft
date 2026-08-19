# PRD: Document slugs

## Problem

Document URLs carry numeric ids, so a shared link tells the recipient nothing about what they are about to open.

## What we want

A document gets a readable slug derived from its title.

A title that contains no usable characters must be rejected outright rather than given an empty slug. An empty slug produces a URL that collides with every other empty slug and silently breaks routing, so this is a correctness requirement, not a nicety. Whitespace- only titles are the case we have actually seen in support tickets.

## Out of scope

- Usage analytics, metrics, or telemetry of any kind in this feature.
- User-edited or custom slugs.
