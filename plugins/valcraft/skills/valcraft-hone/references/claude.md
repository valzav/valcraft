# Claude refinement reference (Fable 5 / Mythos 5)

Distilled from [Prompting Claude Fable 5](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-fable-5) (fetched 2026-07-30). Applies fully to Claude Fable 5 and Claude Mythos 5; the steering principles (brief instruction over enumeration, prune over-prescription) apply directionally to Opus 4.x/Sonnet 5 as well.

## Behavioral profile — what changed and why it matters for refinement

- **Instruction following is strong enough that brief steering works.** One short instruction with a reason replaces a list that names every behavior. Prompts and skills written for older models are often too prescriptive and *degrade* Fable 5 output — pruning is an upgrade, not a risk.
- **Turns are longer by default.** Hard tasks run minutes at higher effort; autonomous runs extend hours. Refined prompts for harnesses should not assume quick turnarounds, and anti-overplanning steering matters more.
- **Effort is the primary dial**, not prompt-side "think harder" language. `high` default, `xhigh` for capability-sensitive work, `medium`/`low` for routine (still strong). Remove prompt text that tries to modulate thinking depth — point the author at the effort parameter instead.
- **More parallel-subagent-happy** than prior models. Prompts should say when delegation is appropriate and prefer async communication over blocking on each subagent.
- **Performs better with intent context** — connect the task to who it's for and what the output enables.

## Audit items specific to Claude

1. **Remove show-your-reasoning instructions.** Any "explain your reasoning in the response", "transcribe your thought process", "reflect out loud" can trigger the `reasoning_extraction` refusal category and fall back to Opus 4.8. If reasoning visibility is needed, read structured `thinking` blocks from adaptive thinking, or surface progress via a send-to-user tool.
2. **Prune prescriptive step lists** carried over from older-model prompts. Keep steps that encode a real workflow contract; drop steps that just spell out how to be competent.
3. **Remove extended-thinking budget language.** Fable 5 is adaptive-thinking only; no extended thinking budgets. Prompt text managing "thinking tokens" is dead.
4. **Check long-run prompts for the standard scaffolding** (snippets below): checkpoint policy, grounded progress claims, autonomous-pipeline reminder where applicable. These are the tested levers for reliability over hours-long runs.
5. **Don't surface context-budget countdowns** to the model; if the harness must, add the reassurance snippet — otherwise Fable 5 may wrap up early or suggest a new session.
6. **Verifier subagents beat self-critique.** For long-run prompts, prefer "verify with fresh-context subagents against the specification at interval X" over "double-check your work".

## Canonical snippets (verbatim from the guide — graft, don't reinvent)

**Anti-overplanning** — when the target over-gathers or narrates options:

```text
When you have enough information to act, act. Do not re-derive facts already established in the conversation, re-litigate a decision the user has already made, or narrate options you will not pursue in user-facing messages. If you are weighing a choice, give a recommendation, not an exhaustive survey. This does not apply to thinking blocks.
```

**Scope guard** — when the target produces unrequested refactors/features at high effort:

```text
Don't add features, refactor, or introduce abstractions beyond what the task requires. A bug fix doesn't need surrounding cleanup and a one-shot operation usually doesn't need a helper. Don't design for hypothetical future requirements: do the simplest thing that works well. Avoid premature abstraction and half-finished implementations. Don't add error handling, fallbacks, or validation for scenarios that cannot happen. Trust internal code and framework guarantees. Only validate at system boundaries (user input, external APIs). Don't use feature flags or backwards-compatibility shims when you can just change the code.
```

**Selective brevity** — replaces lists of named verbosity behaviors:

```text
Lead with the outcome. Your first sentence after finishing should answer "what happened" or "what did you find": the thing the user would ask for if they said "just give me the TLDR." Supporting detail and reasoning come after. Being readable and being concise are different things, and readability matters more.

The way to keep output short is to be selective about what you include (drop details that don't change what the reader would do next), not to compress the writing into fragments, abbreviations, arrow chains like A → B → fails, or jargon.
```

**Checkpoint policy** — replaces enumerating every pause-worthy case:

```text
Pause for the user only when the work genuinely requires them: a destructive or irreversible action, a real scope change, or input that only they can provide. If you hit one of these, ask and end the turn, rather than ending on a promise.
```

**Grounded progress claims** — nearly eliminates fabricated status reports on long runs:

```text
Before reporting progress, audit each claim against a tool result from this session. Only report work you can point to evidence for; if something is not yet verified, say so explicitly. Report outcomes faithfully: if tests fail, say so with the output; if a step was skipped, say that; when something is done and verified, state it plainly without hedging.
```

**Report-vs-fix boundary** — when the target takes unrequested actions:

```text
When the user is describing a problem, asking a question, or thinking out loud rather than requesting a change, the deliverable is your assessment. Report your findings and stop. Don't apply a fix until they ask for one. Before running a command that changes system state (restarts, deletes, config edits), check that the evidence actually supports that specific action. A signal that pattern-matches to a known failure may have a different cause.
```

**Subagent delegation:**

```text
Delegate independent subtasks to subagents and keep working while they run. Intervene if a subagent goes off track or is missing relevant context.
```

**Memory system** — for agents that run repeatedly:

```text
Store one lesson per file with a one-line summary at the top. Record corrections and confirmed approaches alike, including why they mattered. Don't save what the repo or chat history already records; update an existing note rather than creating a duplicate; delete notes that turn out to be wrong.
```

**Autonomous-pipeline reminder** — for unattended runs; cures text-only "I'll now run X" early stops:

```text
You are operating autonomously. The user is not watching in real time and cannot answer questions mid-task, so asking "Want me to…?" or "Shall I…?" will block the work. For reversible actions that follow from the original request, proceed without asking. Offering follow-ups after the task is done is fine; asking permission after already discussing with the user before doing the work is not. Before ending your turn, check your last paragraph. If it is a plan, an analysis, a question, a list of next steps, or a promise about work you have not done ("I'll…", "let me know when…"), do that work now with tool calls. End your turn only when the task is complete or you are blocked on input only the user can provide.
```

**Context-budget reassurance** — only if the harness shows remaining-token counts:

```text
You have ample context remaining. Do not stop, summarize, or suggest a new session on account of context limits. Continue the work.
```

**Intent template** — for requests fed to long-running agents:

```text
I'm working on [the larger task] for [who it's for]. They need [what the output enables]. With that in mind: [request].
```

**Final-summary readability addendum** — for agentic prompts whose end-of-run summaries drift into shorthand:

```text
Terse shorthand is fine between tool calls (that's you thinking out loud, and brevity there is good). Your final summary is different: it's for a reader who didn't see any of that.

If you've been working for a while without the user watching (overnight, across many tool calls, since they last spoke), your final message is their first look at any of it. Write it as a re-grounding, not a continuation of your working thread: the outcome first, then the one or two things you need from them, each explained as if new. The vocabulary you built up while working is yours, not theirs; leave it behind unless you re-introduce it.

When you write the summary at the end, drop the working shorthand. Write complete sentences. Spell out terms. Don't use arrow chains, hyphen-stacked compounds, or labels you made up earlier. When you mention files, commits, flags, or other identifiers, give each one its own plain-language clause. Open with the outcome: one sentence on what happened or what you found. Then the supporting detail. If you have to choose between short and clear, choose clear.
```

**send_to_user elicitation** — pairs with a client-side send-to-user tool (defining the tool alone is not enough; Fable 5 rarely calls it un-prompted):

```text
Between tool calls, when you have content the user must read verbatim (a partial deliverable, a direct answer to their question), call the send_to_user tool with that content. Use send_to_user only for user-facing content, not for narration or reasoning.
```

**Self-verification for long runs** — fresh-context verifiers outperform self-critique:

```text
Establish a method for checking your own work at an interval of [X] as you build. Run this every [X interval], verifying your work with subagents against the specification.
```
