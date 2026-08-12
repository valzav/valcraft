---
name: msw
description: Apply the MSW Kernel to a markdown document — a plan, spec, skill, prompt, or any other .md file. Derives the document's contract, judges every claim by the kernel's deletion test, deletes the claims that fail, audits every limit for authority, and reports in the kernel's format. Use whenever the user runs /valcraft:msw <file>, or asks to apply MSW, run the MSW deletion test, or strip a document down to what its contract actually requires. Edits the target in place — for prompt-guide refinement use hone; for a read-only essence summary use distill.
---

# msw

Apply the MSW Kernel to one markdown document. The document's claims face the kernel's
deletion test against the document's own contract; failing claims are deleted from the
file; the result is reported in the kernel's report format. msw only deletes — it never
adds content, and it never rewrites what survives.

The kernel is defined in `references/kernel.md`. Read it before judging; apply it as
written; never paraphrase it or substitute your own necessity criteria.

## Workflow

1. **Read the whole target.** The argument to `/valcraft:msw` is the target file. Read
   it fully, plus any sibling file it references that carries part of its meaning (a
   skill's references, a plan's linked spec) — those inform judgment but only the target
   is edited. Never judge text you have not fully read.
2. **Read `references/kernel.md`.**
3. **State the contract.** The document's contract is the outcome it exists to produce
   plus the smallest criteria that prove it — derived from the document's stated goal or
   evident purpose, stated before any judgment. If no contract is derivable: attended →
   ask the user; unattended → bind the smallest reading consistent with the document's
   evident intent and record the assumption in the report. The document's explicit
   requirements, safety rules, and output contracts are contract terms — never deletion
   candidates.
4. **Decompose into claims.** Every instruction, step, requirement, constraint, example,
   and limit in the target is one claim. Decompose an instruction together with its
   attached rationale as one claim — they survive or fail together.
5. **Apply the deletion test.** A claim survives only if deleting it leaves the contract
   unmet or unproven. When unsure whether a claim is load-bearing, keep it and flag it
   in the report — never delete on suspicion.
6. **Run the limits pass.** Apply "No unauthoritative limits" to every numeric cap,
   threshold, quota, count, or budget in the target. A limit whose exact value has no
   stated authority — requester, technical or platform contract, project policy, or
   measured evidence — is a failed claim. When the value looks necessary but its
   authority is an unresolved owner choice, keep it, and flag it in the report as an
   owner decision to confirm.
7. **Edit the target in place.** Delete the failing claims. Adjust only what the
   deletions break — numbering, a dangling conjunction, an empty section. If the target
   is not under version control, say so in the report; the edit still proceeds.
8. **Report.** The kernel's report and nothing else:
   - the outcome against the contract — the contract as stated, and that the surviving
     document still meets it;
   - the proof — for each surviving section, why deleting it would leave the contract
     unmet or unproven (grouped, not claim-by-claim);
   - rejected claims worth the user's attention, one line each, with the reason
     (deletion test failed, or limit without authority);
   - flagged claims — kept on uncertainty or pending an owner decision, one line each.

The fuses apply to msw itself: at most 3 judgment rounds over one document, then halt
and report open items; a claim raised in a later round whose evidence was already in
hand earlier is rejected.

## What not to do

- Never add content, restructure surviving text, or "improve" phrasing — deletion and
  the minimal repairs deletions force are the only edits.
- Never delete the document's explicit requirements, safety rules, or output contracts;
  they are the contract, not claims against it.
- Never soften a failed claim into a TODO, a footnote, or a deferred follow-up — a
  failed claim gets one report line and deletion, nothing else.
- Never apply msw to `references/kernel.md` or judge the kernel itself — it is the
  instrument, not a target.
