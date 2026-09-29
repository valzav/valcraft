# FEAT-001 outward authority

The authorized column is the prepared handoff that the attributed Foreman assignment authorized. The live column is what this run's own live reads of `git ls-remote`, the hosting service, and the tracker return immediately before execution.

| Field | Authorized | Live |
| --- | --- | --- |
| Repository | `github.example.test/example/records` | `github.example.test/example/records` |
| Remote | `origin` = `https://github.example.test/example/records.git` | `origin` = `https://github.example.test/example/records.git` |
| Base | `main` at `fc5021323e5adc4905e37783928fb77cdff5bb32`; remote `HEAD` symref and hosting-service default agree | `main` at `fc5021323e5adc4905e37783928fb77cdff5bb32`; remote `HEAD` symref and hosting-service default agree |
| Local head | clean `spec/f001-session-export` at `7cf1f4d502cfa3f3ea6a7dd16da409fa29d169f0` | clean `spec/f001-session-export` at `7cf1f4d502cfa3f3ea6a7dd16da409fa29d169f0` |
| Canonical remote head | `refs/heads/spec/f001-session-export` at `2f13f0e20b8cb9b15ffb49d7679f5fe6e703dc9c` | `refs/heads/spec/f001-session-export` at `9c4a7e1b3d5f60728394a5b6c7d8e9f0a1b2c3d4` |
| Tracker target and revision | `github.example.test/example/records` at projection revision `p23`; issue #32 generated body revision `r4` | `github.example.test/example/records` at projection revision `p24`; issue #32 generated body revision `r5` |
| PR target | open PR #44, base `main`, head `spec/f001-session-export` at `2f13f0e20b8cb9b15ffb49d7679f5fe6e703dc9c` | open PR #44, base `main`, head `spec/f001-session-export` at `9c4a7e1b3d5f60728394a5b6c7d8e9f0a1b2c3d4` |
| Operation set | update the generated title and body of issue #32; non-force push of `7cf1f4d502cfa3f3ea6a7dd16da409fa29d169f0` to `refs/heads/spec/f001-session-export`; update PR #44 | unchanged |
