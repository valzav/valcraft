# Design

`src/export.py` owns immediate exports. Add a scheduler function beside it that validates an aware future UTC timestamp, persists one pending record, and returns its identifier. Tests use the standard-library `unittest` runner.
