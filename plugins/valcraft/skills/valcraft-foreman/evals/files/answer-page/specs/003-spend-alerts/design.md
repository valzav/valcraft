---
feature: FEAT-003
status: draft
created: 2026-10-20
updated: 2026-10-20
---

# Design: Spend alerts

## Summary

`daily_spend(card_id, day, amount)` (FR-001). `evaluate(card_id, day) -> Alert | None` compares the day with the previous day against the threshold (FR-002). `deliver(alert)` sends to each channel; the webhook channel retries before dropping (FR-003, FR-004). `digest(owner, day)` collects the day's alerts (FR-005). `title(alert)` includes the merchant name (FR-006).
