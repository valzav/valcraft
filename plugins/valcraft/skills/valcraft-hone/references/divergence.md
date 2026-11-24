# Where Claude and Codex diverge

Read this file only for artifacts that target both model families. Divergence notes belong in the change report, never in the refined artifact itself — and only where the divergence is live for that artifact.

| Topic | Claude (Fable 5.2) | Codex (GPT-5.6) |
| --- | --- | --- |
| Verbosity default | Un-steered, elaborates beyond the task; effort has little effect on reply length, so selective-brevity steering in the prompt sets it | More concise by default than GPT-5.5 — existing "be concise" lines can over-trim; audit and often remove |
| Reasoning visibility | Never instruct it to echo/transcribe/explain internal reasoning in the response — triggers a `reasoning_extraction` refusal, a category with no recommended fallback model. Read summarized `thinking` blocks or add a send-to-user tool instead | No refusal risk, but chain-of-thought isn't returned — such instructions are dead weight; remove them too |
| Capability dial | `effort` is the primary control (`high` is the API default and the starting point, `medium`/`low` where evals hold, `xhigh` only with a measured gain); prompt lines that ask for less thinking have no effect at `medium` and above | reasoning effort + `text.verbosity` set defaults (Responses API); pro mode reserved for quality-critical tasks with measured gains |
| Tool orchestration | Delegates readily where the harness invites it, so a standing instruction to delegate can over-delegate and subagents add session cost; async orchestration; fresh-context verifier subagents where the author wants scheduled verification | Programmatic Tool Calling (Responses API) with task-specific routing: which stage, eligible tools, output schema, retry/stop limits, one handoff |
| Long-run scaffolding | Rich documented patterns: checkpoint policy, memory files, finish-the-whole-task blocks, context-budget reassurance, send-to-user elicitation (see references/anthropic.md) | Compact autonomy/approval policy is the documented lever; no equivalent long-run snippet library |
| Approval rules | Applies "never" without exception and over-holds on a broad approval category; name the specific actions that need approval and the routine steps that need none | The compact three-tier policy with broad categories (external writes, destructive actions, purchases) is the documented lever |
