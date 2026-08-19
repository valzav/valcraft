# Design

`src/export.py` owns scheduling. The scheduler rejects naive or non-UTC
timestamps before persisting a pending record. A uniqueness constraint prevents
duplicate queue entries.
