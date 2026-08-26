# Request timeout

Slow providers must be bounded. An operator can set a per-reference request timeout in whole seconds so one stalled provider cannot hold a request open indefinitely. When no timeout is configured the service uses 30 seconds.
