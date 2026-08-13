# Codex refinement reference (GPT-5.6 family)

Distilled from [GPT-5.6 model guidance — prompting best practices](https://developers.openai.com/api/docs/guides/latest-model?model=gpt-5.6#prompting-best-practices) and [Codex models](https://learn.chatgpt.com/docs/models) (fetched 2026-07-30, re-verified 2026-08-12). Applies to the GPT-5.6 family. `gpt-5.6` aliases `gpt-5.6-sol`; Codex uses Sol for complex open-ended work, Terra for everyday work, and Luna for repeatable work. Sections labeled Responses API apply only when the caller controls that API configuration.

## Behavioral profile — what changed and why it matters for refinement

- **Leaner prompts measurably win.** In OpenAI's internal coding-agent evals, leaner system prompts improved scores ~10–15% while cutting total tokens 41–66% and cost 33–67%. Treat as directional; validate on representative tasks.
- **More concise by default than GPT-5.5.** Broad brevity instructions ("Be concise", "Keep it short") may now be unnecessary and can make responses _too_ brief — audit each one; keep only those that reliably produce needed output.
- **Proactive and persistent on multi-step tasks.** Needs an explicit autonomy policy so it neither pauses needlessly nor overreaches.
- **Length/detail is an API-level control (Responses API only)**: `text.verbosity` (`low`/`medium`/`high`) sets the default; the prompt carries only task-specific length, structure, and required content. When the caller controls the Responses API configuration, move generic length steering out of the prompt and into the parameter.

## The leaning process (how to safely cut an existing prompt)

1. Start from a prompt + tool set that already works.
2. Remove one group of instructions, examples, or tools at a time, then rerun the same evals.
3. State each instruction once.
4. Expose only tools relevant to the task; keep tool descriptions concise and precise.
5. Keep examples and style guidance when they encode a product requirement or correct a measured gap.
6. Track context at run start and as the conversation grows — long sessions amplify repeated prompt and tool content.

## Canonical snippets (verbatim from the guide — graft, don't reinvent)

**Autonomy and approval boundaries** — a compact three-tier policy; stated once. Repeating "ask first" / "do not mutate" / "wait for approval" causes unnecessary approval requests for safe, expected actions. Name safe local actions explicitly (reading files, inspecting logs, editing in-scope code, running tests):

```text
For requests to answer, explain, review, diagnose, or plan, inspect the relevant
materials and report the result. Do not implement changes unless the request also
asks for them.

For requests to change, build, or fix, make the requested in-scope local changes
and run relevant non-destructive validation without asking first.

Require confirmation for external writes, destructive actions, purchases, or a
material expansion of scope.
```

**What a short answer must include** — replaces bare "be concise" with a priority order:

```text
Lead with the conclusion. Include the evidence needed to support it, any material
caveat, and the next action. Omit secondary detail and repetition.

Keep all required facts, decisions, caveats, and next steps. Trim introductions,
repetition, generic reassurance, and optional background first.
```

**Tone by concrete writing choices** — replaces ambiguous labels like "friendly"/"empathetic":

```text
State the answer directly. If the user reports a problem, acknowledge the
specific issue before giving the next step. Use reassurance only when it is
relevant. Omit generic praise and unnecessary sign-offs.
```

## Responses API Pro mode

- Use when a marginal quality improvement materially affects the outcome and the task is hard enough to benefit (complex optimization, high-value coding/review, deep analysis with clear evaluation criteria). Prefer standard mode for routine, latency-sensitive, or high-volume work.
- Codex Max deepens one agent's reasoning; Ultra uses subagents. Neither is Responses API Pro mode.
- Keep the same outcome-focused prompt as standard mode: goal, relevant context, constraints, required evidence, success criteria, output format. **Do not** add "use pro mode", "think harder", or "generate several candidate answers" — remove such lines during refinement.
- Pro mode and reasoning effort are independent; start from the standard-mode baseline config and compare on representative tasks rather than assuming max effort wins.

Example of the outcome-focused shape:

```text
Review this database migration plan for failure modes that could cause data loss
or extended downtime. For each finding, cite the relevant step, estimate impact
and likelihood, and recommend a specific mitigation. Return the five most
important risks in severity order.
```

## Programmatic Tool Calling (Responses API only)

**When it fits:** bounded workflows where code processes several tool results or large intermediate outputs and returns a much smaller structured result — filtering, joining, ranking, deduplication, aggregation, validation.

**Prefer direct tool calls when:** one call suffices; intermediate outputs are already small; each result may change the model's next decision; an action requires approval; the final output must preserve citations or native artifacts. Multiple/parallel/dependent calls alone do not justify PTC.

**Routing must be task-specific.** Don't rely on tool availability or "use PTC efficiently". State: which bounded stage uses PTC, which tools it may call, the exact output schema and required evidence, concurrency/retry/stopping limits, and which work stays direct. Tool descriptions must document return fields, types, and error behavior — if the model can't know the return shape before writing the program, use direct calls. If both routes are needed, define one clear handoff and forbid switching routes or repeating completed work.

Routing template:

```text
<tool_orchestration>
Use Programmatic Tool Calling for [bounded stage] using only [eligible tools].
Run independent calls concurrently when safe. Use only documented tool input
and output fields.

Process and reduce the intermediate results, then emit exactly [output schema],
including the evidence needed for the final answer.

Stop when [condition] is met. Retry transient failures at most [R] times.
Do not repeat completed calls or perform side-effecting actions. If a required
result is still missing, return a clear structured failure.

Use direct tool calls for [semantic judgment, approval, or final validation].
</tool_orchestration>
```

**Test both outputs.** The `program_output` item and the final assistant `message` are separate — a program can return correct records while the message omits a required field, citation, or caveat. Count lower resource use as an improvement only when the response still passes existing evals.
