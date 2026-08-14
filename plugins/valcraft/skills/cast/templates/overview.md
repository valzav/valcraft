---
status: draft
updated: <YYYY-MM-DD>
---

# Architecture overview

<!-- Keep this short. It answers "what talks to what, and who owns which data" —
     detail belongs in ADRs and specs/NNN-*/design.md. -->

## Context

<One paragraph: what the system is, who uses it, and the external systems it touches.>

## Components

<One line per component: name — responsibility. Include external dependencies that
matter architecturally (data store, queue, third-party APIs).>

## Boundaries

<The lines that must not be crossed: process/service boundaries, module layering,
public contracts. Cite the ADR that established each boundary.>

## Data ownership

<Which component owns which data, and who may read or write it. "Shared" is a decision
to record, not a default.>
