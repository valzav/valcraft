# distill — compare mode

Read this file for any request to compare two artifacts. Comparison implies study mode — skip the mode question.

1. Launch one subagent per artifact with the harness's agent tool, both in a single message so they run in parallel. Each subagent runs the full study-mode workflow on its artifact and returns only the YAML distillate — the stable keys make the handoff reliable. If the harness cannot launch subagents or cannot dispatch them concurrently, distill the artifacts sequentially in isolated passes and preserve the same YAML handoff.
2. Compare the distillates, not the sources. Do not re-read the artifacts, and never execute either one: every behavioral claim is inferred from the distillates.
3. Align vocabulary first: steps that accomplish the same thing get identical phrasing in both distillates.
4. Report the behavioral diff, not the two distillates:
   - the shared core, in one or two lines;
   - differences grouped: only in A; only in B; same step under different constraints;
   - the divergence in results — given the same input, what each artifact would do or produce differently, inferred from the distillates.

Present differences without a verdict. Recommend one only when the user asks which to prefer, and tie the recommendation to their stated use. Offer to save the two distillates with the standard save options from `output-formats.md`.
