# Skill eval protocol

Run each case from an isolated fixture copy. The baseline receives only the case prompt and fixture files; it must not receive the skill source, references, prior transcripts, or prior grading artifacts. The with-skill run receives the same fixture copy plus the target skill.

Use one immutable run directory per `(skill, case, configuration)` and write the transcript before grading. A grader writes to a temporary file and atomically renames it to `grading.json`; if that path already exists, it must verify the existing result instead of overwriting it. This makes retries idempotent and prevents grading races.

Keep prompts neutral. Do not include the expected tactic, implementation sequence, or assertion wording in the user prompt unless that wording is itself the behavior under test. Put discriminating requirements in the assertions and expected output.

Record partial runs separately from complete summaries. Do not aggregate a suite until every case has one baseline transcript, one with-skill transcript, and one grading result for each configuration.

## Auditing gradings

An LLM grader's labels are judgments. After a grading batch completes, audit them before reading the totals as final. The protocol has four steps, and each step has one owner:

1. **Jev selects.** `scripts/jev-grade.py --runs <dir>` asks TypeSafe's Jev decision model, through OpenRouter, for one probability per graded assertion and writes `jev-grading.json` beside each `grading.json`. It needs `OPENROUTER_API_KEY` in the environment and writes the key nowhere. `scripts/jev-compare.py --runs <dir>` then writes the calibration report and `_harness/jev-flagged.json`. Jev writes no evidence, so it never sets a label; it only selects what gets a second look.
2. **A blind re-grade judges.** One fresh re-grader per flagged case grades only the flagged assertions, under the brief below, and writes `regrade.json`. `scripts/jev-review.py --runs <dir>` joins the flagged set, the re-grades, and the labels into `_harness/jev-review.md`: conflicts, where the re-grader differs from the label; confirmed, where it agrees and the flag was a Jev error; and assertion problems, wording the re-grader found open to two readings, as input for `evals.json` fixes.
3. **The operator approves.** Read each conflict against the run itself, `transcript.md` and `outputs/`, not against the evidence strings alone. A conflict whose re-grade evidence starts with `Unverifiable:` says the run did not preserve its proof; fix the run or the runner brief rather than the label. Nothing flips automatically: on the first audit, 9 of 25 flagged disagreements turned on assertion wording, and a first adjudication pass from keyword hits claimed 8 grader errors, 4 of which collapsed when the full run was read.
4. **A corrected label records its prior value.** `scripts/jev-apply.py --runs <dir> <case>:<index> ...` applies the approved conflicts. It refuses when the current label is no longer the one the review showed, sets `passed` to the re-grader's verdict, prefixes the evidence with `Corrected <date>, was <pass|fail>.`, recomputes the case summary, and names the suite's summary files as stale. Reconcile those by recomputing from disk and checking that the old totals differ by exactly the applied changes.

### Selection rule

An assertion is flagged when the label and Jev's probability differ by more than 0.9. That band is the only one with measured yield: 4 label changes from 25 flagged on the first audit, over 1,276 assertions. An assertion whose evidence already starts with `Corrected` is not flagged again. Widening the band requires the same measurement first: adjudicate a sample from the next band, record its yield, and let the operator choose. Filtering by assertion wording is not supported; absence-worded and other assertions agreed with Jev at the same rate.

The flagged set carries each assertion's index and verbatim text and nothing else, so the re-grader cannot see the label, the probability, or the evidence.

### Re-grader brief

Give one fresh re-grader the case directory, `<skill>/eval-<id>/<config>`, and the flagged `(index, text)` pairs. Nothing else about the case's grading history, and it must not look for it.

- Grade only the listed assertions. Read `transcript.md` completely and every file under `outputs/` relevant to a listed assertion. Judge the artifacts themselves; where an assertion is mechanically checkable, verify it with a command and quote the result.
- Verdict rule: pass on clear, citable evidence that reflects genuine task completion rather than surface compliance; fail on no evidence, contradicted evidence, superficial evidence, or an assertion that cannot be verified from the run. When uncertain, the assertion fails.
- When a fail rests on absent material rather than on what the run did, such as no `outputs/` directory or an artifact the assertion names that the run never preserved, start the evidence with `Unverifiable:` and name what is missing. The verdict is still fail. The prefix lets the review separate a run that broke the proof rule from a label that was wrong; the first is the runner's problem, not the grader's.
- Read the case's fixture files under the skill's `evals/files/` when an assertion compares the run's output with the fixture, and quote the comparison. Do not open the skill's `SKILL.md` or its references.
- Do not open `grading.json`, `jev-grading.json`, `regrade.json`, suite summaries, `evals.json`, or anything under `_harness/`. The re-grade is blind to the first label and to Jev.
- For each assertion, state in one sentence why its wording supports two readings, or leave `assertion_problem` empty.
- Write `regrade.json` beside `grading.json`, by temporary file and rename: `{"skill", "eval_id", "config", "regraded": [{"index", "text", "passed", "evidence", "assertion_problem"}]}`. Write nothing else. Never edit `grading.json`.
