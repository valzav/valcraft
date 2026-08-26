# PRD: Console guard

## Problem

A play session logs uncaught errors to the browser console. Each one is a defect we shipped without noticing, and nothing in the current process catches them before release.

## What we want

A play session runs to completion with an empty uncaught-error console. A scripted run at a fixed viewport decides it, so the result is the same on every machine.

## Out of scope

- Console warnings and informational logs.
- Errors raised by third-party embeds the app does not control.
