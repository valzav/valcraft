# Baseline facts before planning

Read this before writing or revising a plan. Baseline inspection prevents plans from scheduling work that already exists or naming commands the repository does not define.

Inspect, at the exact baseline SHA and never from memory or the working tree, every file or surface the plan will touch or rely on. Record what is there, then write the plan against that record.

## What to inspect

For each path the plan names as touched, created, or consumed:

- whether it exists at the baseline (`git cat-file -e <sha>:<path>`), and if so its relevant content (`git cat-file -p <sha>:<path>`);
- ignore rules that already cover the artifacts the plan will produce (`git cat-file -p <sha>:.gitignore`);
- every command, script, or entry point the plan will invoke or document, read from its committed source of truth — `package.json` scripts, a `Makefile`, `pyproject.toml`, `AGENTS.md` Commands — so the plan binds to the committed name rather than inventing one;
- an existing test, fixture, or configuration file the plan would otherwise schedule as new work.

## How it enters the plan

- A step that would create what already exists becomes a reconciliation step, or is removed.
- A documented command binds to the committed name. When the documentation and the source of truth disagree, the plan names which one changes and why.
- A verification step names what it discriminates. An exit status alone does not prove a linter inspected any file, a test ran any case, or a build emitted any artifact; state the observable that would differ if the step were vacuous.

Record the inspected paths, baseline SHA, and command used (`git cat-file -p <sha>:<path>`) in the plan's workspace section to prove the facts came from the commit rather than the working tree.
