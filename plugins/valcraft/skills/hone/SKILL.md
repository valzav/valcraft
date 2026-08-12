---
name: hone
description: Refine an existing prompt artifact — inline prompt text, markdown prompt files (system prompts, agent instructions, slash commands), or a complete skill directory — against the official model prompting guides (Anthropic "Prompting Claude Fable 5" + OpenAI GPT-5.6 best practices). Use whenever the user runs /valcraft:hone, or asks to refine, tighten, optimize, modernize, or audit a prompt, system prompt, SKILL.md, CLAUDE.md, agent instructions, or skill for Claude, Opus, Fable, GPT, or Codex — even if they just say "make this prompt better" or "apply prompting best practices".
---

# hone

Take a prompt artifact and make it work better on current frontier models. Both vendors converge on the same headline: **modern models need steering, not enumeration, and shorter prompts usually perform better** — OpenAI measured double-digit eval gains from leaner system prompts at roughly half the tokens, and Anthropic reports that skills written for older models are often too prescriptive for Claude Fable 5 and degrade its output. Deletion is your primary tool. A refinement that makes the prompt longer needs a specific justification for every added line.

Sources: [Prompting Claude Fable 5](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-fable-5) · [GPT-5.6 model guidance](https://developers.openai.com/api/docs/guides/latest-model?model=gpt-5.6#prompting-best-practices)

## Workflow

1. **Offer a distill pass first.** Ask "distill it first?" — with the harness's structured question tool when one exists. Skip the question only when the user's request already answers it, not on your own judgment of the target's size or worth; in a non-interactive run, choose a default and say so. If yes, run the distill skill in clean mode over the target after reading it (invoke `valcraft:distill`; where skills cannot invoke skills, follow `../distill/SKILL.md`), so proven noise is already gone when refinement starts — the maximum-refinement path. Within hone, distill supplies the deletion list and hone owns the in-place edit; attribute those deletions to distill in the change report.
2. **Read the whole target first.** Inline text: what the user pasted. Markdown file(s): read each fully. Skill directory: SKILL.md plus every referenced resource (references/, scripts/ descriptions, command wrappers). Never rewrite text you haven't fully read — a "redundant" instruction may be load-bearing for a case you haven't seen yet.
3. **Determine the target model family.** Claude, Codex, or both. Infer from context: frontmatter, harness (a Claude Code skill targets Claude; an AGENTS.md often targets Codex), or the user's words. When unclear, refine against the shared checklist below and add divergence notes only where the two families genuinely differ. Ask only if the answer would materially change the rewrite.
4. **Load the matching reference(s):** `references/claude.md` for Claude targets, `references/codex.md` for Codex targets, both for model-agnostic artifacts. They contain the audit items and canonical snippets from each guide — reuse proven snippet language rather than inventing your own.
5. **Audit before rewriting.** Walk the checklist and note findings with line references. This ordering matters: auditing first keeps the rewrite surgical instead of a from-scratch rewrite that loses the author's intent.
6. **Rewrite.** Files and skill directories: edit in place unless the user asked for a copy. Inline text: return the refined prompt in a code block. The intent and deletion boundaries are in "What not to do" below.
7. **Report.** List each change with the guideline that motivated it (one line each). Separately flag judgment calls the author should confirm — e.g. removed examples that might encode a product requirement, or a Claude-only snippet added to a prompt that may also run on Codex.

## Shared checklist (both model families agree)

1. **State each instruction once.** Remove repeated rules, duplicated examples, and overlapping sections. Long sessions amplify repeated prompt content; repetition also causes over-compliance (e.g. repeated "ask first" produces needless approval requests).
2. **Delete instructions that restate default model behavior.** "Be helpful", "think step by step", "use tools when appropriate", "generate several candidates and pick the best" — current models do this unprompted, and pro/high-effort modes explicitly don't need "think harder". Every such line is noise that dilutes the instructions that matter.
3. **Replace behavior enumeration with brief steering plus the reason.** A short instruction that explains _why_ outperforms a wall of ALWAYS/NEVER bullets naming each behavior. If you see rigid all-caps mandates, reframe: state the goal and the reason, let the model generalize.
4. **Give the intent behind the task.** "I'm working on [larger task] for [who]. They need [what the output enables]." Context lets the model connect the task to relevant information instead of guessing intent.
5. **One compact autonomy policy.** Define three tiers once: read/diagnose/report → act without asking; in-scope changes + non-destructive validation → act without asking; destructive, external, costly, or scope-expanding actions → confirm first. Scattered "ask first" / "don't pause" fragments cause both over-asking and overreach.
6. **Specify what a short answer must include, not "be concise".** Give a priority order: lead with the conclusion, keep required facts/caveats/next steps, trim introductions, repetition, and generic reassurance first. Readability beats compression — no fragments, abbreviations, or arrow-chain shorthand.
7. **Define tone by concrete writing choices, not labels.** "Friendly" and "empathetic" are ambiguous. Say what to do: state the answer directly, acknowledge the specific problem before the next step, omit generic praise and sign-offs.
8. **Add a scope guard for agentic prompts.** No unrequested features, refactors, abstractions, or defensive handling for scenarios that can't happen; simplest thing that works; validate only at system boundaries.
9. **Ground progress claims in evidence.** For long-running agents: report only work traceable to a tool result; unverified → say so; failures reported plainly with output. This nearly eliminates fabricated status reports.
10. **Frame tasks by outcome.** Goal, relevant context, constraints, required evidence, success criteria, output format. Keep examples only when they encode a product requirement or fix a measured gap; keep tool descriptions concise and precise, exposing only tools the task needs.

## Where Claude and Codex diverge

Divergence notes belong in the change report, never in the refined artifact itself — and only where the divergence is live for that artifact (it will run on both families, or it contains a pattern that is fine on one and harmful on the other).

| Topic                | Claude (Fable 5)                                                                                                                                                                                    | Codex (GPT-5.6)                                                                                                                  |
| -------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------- |
| Verbosity default    | Un-steered, elaborates beyond the task at higher effort — selective-brevity steering helps                                                                                                          | More concise by default than GPT-5.5 — existing "be concise" lines can over-trim; audit and often remove                         |
| Reasoning visibility | Never instruct it to echo/transcribe/explain internal reasoning in the response — triggers the `reasoning_extraction` refusal + fallback. Read `thinking` blocks or add a send-to-user tool instead | No refusal risk, but chain-of-thought isn't returned — such instructions are dead weight; remove them too                        |
| Capability dial      | `effort` is the primary control (high default, xhigh capability-sensitive, medium/low routine)                                                                                                      | reasoning effort + `text.verbosity` set defaults; pro mode reserved for quality-critical tasks with measured gains               |
| Tool orchestration   | Parallel subagents, async orchestration, fresh-context verifier subagents over self-critique                                                                                                        | Programmatic Tool Calling with task-specific routing: which stage, eligible tools, output schema, retry/stop limits, one handoff |
| Long-run scaffolding | Rich documented patterns: checkpoint policy, memory files, autonomous-pipeline reminder, context-budget reassurance, send-to-user elicitation (see references/claude.md)                            | Compact autonomy/approval policy is the documented lever; no equivalent long-run snippet library                                 |

## What not to do

- Don't stamp model names or versions into the refined artifact ("Runs on GPT-5.6", "tuned for Fable 5") or otherwise tie it to a model generation. A good refinement is mostly deletion of noise, which works on older models too. Anything genuinely version-specific — like dropping "be concise" because GPT-5.6 is terser by default — goes in the change report as a reversible note, not into the prompt.
- Don't grow the prompt. If your refinement adds more lines than it removes, re-audit against checklist items 1–3.
- Don't change what the prompt is for, its output contract, or its safety/security rules — those are the author's domain.
- Don't delete on suspicion alone: an example or rule that might encode a product requirement gets kept and flagged, not removed. Bulk deletions are best validated the way OpenAI recommends — remove one group at a time and re-test.
- Don't hand-write a snippet the guides already provide — the canonical versions in `references/` are tested language.
