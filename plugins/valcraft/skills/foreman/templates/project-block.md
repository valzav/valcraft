# Foreman runtime configuration

`valcraft:foreman` works without any `foreman_*` key. Add only explicit project overrides to root `AGENTS.md`; do not write keys merely to make Foreman available.

```yaml
foreman_backend: subagents # backend key from references/backends/README.md
foreman_approval_mode: attended # attended | unattended — references/approval-modes.md
foreman_default_branch: develop # task PRs target this branch
foreman_release_branch: stable # enables release-only flows; writes here wait in every mode
```

Optional, only when the project needs it:

```yaml
foreman_clarification_assignees: # github intake only — who receives a needs-clarification question
  product: <login>
  default: <login>
```

Resolution rules:

- Missing `foreman_backend` means native `subagents`. Missing `foreman_approval_mode` means `unattended`.
- For a missing `foreman_default_branch`, resolve the live remote `HEAD` symref (for example, `git ls-remote --symref origin HEAD`) and the hosting service's reported default branch for the same repository. Use the branch only when the available live sources resolve it unambiguously; stop and ask for an explicit value when both live sources are unavailable or they disagree. A cached `origin/HEAD` may corroborate a live result but never supplies the value.
- Missing `foreman_release_branch` means no separate release branch. Fast-track and direct release-branch writes are unavailable until an explicit valid branch is configured. Ordinary merges to the default branch still use the normal approval row.
- An explicit valid value overrides its runtime default. An invalid or ambiguous explicit value stops; never silently replace it.
- `cast_approval` is independent: its missing-key default remains `attended`.
- A non-default backend may require operator configuration; see its backend reference.
- `.foreman/` must be gitignored; `valcraft:cast` adds it at scaffold time.
