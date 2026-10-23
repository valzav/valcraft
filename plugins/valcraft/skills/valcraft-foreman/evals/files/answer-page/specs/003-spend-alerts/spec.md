---
id: FEAT-003
title: Spend alerts
status: draft
spec_issue: null
created: 2026-10-20
updated: 2026-10-20
---

# Spend alerts

## Sources

- `docs/prd.md`
- `docs/product-brief.md`

## Summary

The account owner is alerted when a card's spend changes, through delivery channels, with a daily digest.

## Functional requirements

- FR-001: The system MUST record each card's daily spend.
- FR-002: The system MUST alert the account owner when a card's spend changes by more than the alert threshold.
- FR-003: The system MUST deliver each alert through the configured channels.
- FR-004: The system MUST retry a failed webhook delivery before it drops the alert.
- FR-005: The system MUST send a daily digest of the day's alerts.
- FR-006: Each alert title MUST show the merchant name.

## Acceptance criteria

- [ ] AC-001: A day's spend is stored per card.
- [ ] AC-002: A change over the threshold creates exactly one alert.
- [ ] AC-003: Each alert reaches every configured channel, or is reported as dropped.
- [ ] AC-004: The digest lists the day's alerts once per day.
- [ ] AC-005: The alert title contains the merchant name.
