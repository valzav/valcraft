# Skill eval protocol

Run each case from an isolated fixture copy. The baseline receives only the case prompt and fixture files; it must not receive the skill source, references, prior transcripts, or prior grading artifacts. The with-skill run receives the same fixture copy plus the target skill.

Use one immutable run directory per `(skill, case, configuration)` and write the transcript before grading. A grader writes to a temporary file and atomically renames it to `grading.json`; if that path already exists, it must verify the existing result instead of overwriting it. This makes retries idempotent and prevents grading races.

Keep prompts neutral. Do not include the expected tactic, implementation sequence, or assertion wording in the user prompt unless that wording is itself the behavior under test. Put discriminating requirements in the assertions and expected output.

Record partial runs separately from complete summaries. Do not aggregate a suite until every case has one baseline transcript, one with-skill transcript, and one grading result for each configuration.
