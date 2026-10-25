# Navigation resolver contract

This contract defines how a Valcraft navigation tool turns a Valcraft identity or a file reference into a file location. Every navigation tool implements it and passes the conformance cases in [`fixtures/cases.json`](fixtures/cases.json). The Herdr plugin in [`herdr/`](herdr/) is the first implementation.

The contract derives its identity rules from Valcraft's feature contract (`plugins/valcraft/skills/valcraft-spec/references/feature-contract.md`) and quick-task contract (`plugins/valcraft/skills/valcraft-spec/references/quick.md`). When those contracts change an identity rule, this contract and its fixtures change in the same change.

## Inputs and result

A resolution takes two inputs:

- the **base directory**: the working directory the reference was shown in, such as a terminal pane's working directory; and
- the **reference**: one selected string.

It returns exactly one result:

- **target**: one absolute file path, a 1-based line, and a 1-based column.
- **ambiguous**: two or more candidate targets, each with its qualified identity, its feature or quick-file title, and its task text. A tool presents the candidates and never opens one without the user's choice.
- **failure**: one failure class from [Failure classes](#failure-classes).

Resolution is deterministic: the same base directory, files, and reference give the same result. It reads current files, including uncommitted edits. It never reads git history, tracker state, or the network, and it writes nothing.

## Recognition

### Trimming

Before recognition, remove these characters from both ends of the reference, repeatedly, until none remains at either end:

- whitespace;
- backticks, straight quotes (`'`, `"`), and curly quotes (`‘`, `’`, `“`, `”`);
- brackets: `(`, `)`, `[`, `]`, `{`, `}`, `<`, `>`.

Then remove trailing `.`, `,`, `;`, `:`, `!`, and `?` characters, and repeat both steps until the reference stops changing. An empty result is `unrecognized`.

### Forms

Identity digits are decimal and at least three digits long. A digit string is compared as written: `FEAT-023` names the feature whose directory number is `023`, and `FEAT-0023` does not.

| Form | Meaning |
| --- | --- |
| `FEAT-NNN` | a feature |
| `FEAT-NNN/T-XXX` | a task in that feature |
| `Q-NNN` | a quick file |
| `Q-NNN/QT-XXX`, `Q-NNN QT-XXX` | a task in that quick file; exactly one space in the second form |
| `T-XXX` | a bare feature task |
| `QT-XXX` | a bare quick task |
| `path`, `path:LINE`, `path:LINE:COLUMN` | a file reference; `LINE` and `COLUMN` are positive decimal integers |

Recognition is case-sensitive.

- A reference that begins with `FEAT-`, `Q-`, `T-`, or `QT-` and matches no identity form is `malformed_identity`. This includes too few digits, a wrong-prefix pair such as `FEAT-001/QT-001` or `Q-001/T-001`, and trailing text such as `T-001x`. It is never treated as a file reference.
- Any other reference with no whitespace is a file reference.
- Any other reference is `unrecognized`.

### References in terminal output

A tool that collects references from terminal output, such as a picker over a pane's recent output, recognizes these tokens:

- every identity form above, delimited by characters that cannot appear in the form;
- every file reference whose path contains `/`, or whose final path component contains a `.` that is neither its first nor its last character.

A tool lists a collected file reference only when it resolves to a target. An identity is listed as written and resolved when chosen.

## Checkout

Identity resolution needs a **checkout**: the git working tree that contains the base directory, as `git rev-parse --show-toplevel` reports it from that directory. A linked worktree is its own checkout. A base directory outside any working tree is `not_valcraft_checkout` for an identity.

The checkout is a **Valcraft project** when it contains `.valcraft/config.yaml` as a regular file tracked by git. Otherwise an identity is `not_valcraft_checkout`.

The **primary checkout** is the working tree that owns the git common directory: the parent of `git rev-parse --path-format=absolute --git-common-dir`. A tool reads user-local files that git ignores, such as `.valcraft/config.local.yaml`, from the primary checkout, because a linked worktree does not carry them. Artifacts always resolve against the checkout itself.

## Artifacts

### Frontmatter

Frontmatter is the block between a first line that is exactly `---` and the next line that is exactly `---`. A frontmatter field is a line `key: value` with the key at the start of the line; the key and the value are separated by a colon and one space, and the value is trimmed. A file without that block has no frontmatter.

### Valid features

Each immediate subdirectory of `specs/` whose name begins with a decimal digit is a feature candidate. A candidate is a valid feature when all of these hold:

- its name is `<number>-<slug>`, where `<number>` has at least three decimal digits and `<slug>` matches `[a-z0-9]+(?:-[a-z0-9]+)*`;
- `spec.md` is a regular file whose frontmatter holds exactly one `id` field, with value `FEAT-<number>`;
- `tasks.md`, when present, is a regular file whose frontmatter holds exactly one `feature` field, with value `FEAT-<number>`; and
- no other candidate has the same `<number>`.

Candidates that share a number are all invalid. The feature title is the `title` frontmatter field of `spec.md`, or empty when it is absent.

### Valid quick files

Each regular file directly in `specs/quick/` whose name ends in `.md` is a quick candidate. It is a valid quick file when all of these hold:

- its name is `<number>-<slug>.md`, with the same `<number>` and `<slug>` rules as a feature;
- its frontmatter holds exactly one `id` field, with value `Q-<number>`;
- it contains no feature task definition (see below); and
- no other candidate has the same `<number>`.

The quick-file title is the text after the number sign and space of its first level-one heading line, or empty when it has none.

### Defining entries

A defining entry is one line of an artifact. These lines are never defining entries:

- a line that starts while an HTML comment is open, from `<!--` to the next `-->`;
- a fenced code block: from an opening fence line, which starts with up to three spaces and then three or more backticks or tildes, to the next line that starts with up to three spaces and at least as many of the same character followed only by whitespace, or to the end of the file. Both fence lines belong to the block.

Comment markers inside a fenced block and fences inside a comment have no effect.

- A **feature task definition** of `T-XXX` is a line of a valid feature's `tasks.md` that starts at column 1 with either `- [ ] T-XXX`, `- [x] T-XXX`, or `- [X] T-XXX`, or with `- T-XXX` and ends with `→ TBD` or `→ #<positive number>`. The identity is followed by a space or the end of the line.
- A **quick task definition** of `QT-XXX` is a line of a valid quick file that starts at column 1 with `- [ ] QT-XXX`, `- [x] QT-XXX`, or `- [X] QT-XXX`, followed by a space or the end of the line.

Every other occurrence of an identity, such as `blocked by T-002` or a citation in prose, is a reference, not a definition. The task text of a definition is the rest of its line after the identity, trimmed.

A feature `tasks.md` line that defines `QT-XXX`, and a quick-file line that defines `T-XXX`, are never definitions of either kind. A quick file with a `T-XXX` definition line is invalid as a whole.

## Resolution

### Identities

| Reference | Result |
| --- | --- |
| `FEAT-NNN` | the valid feature's `spec.md` at line 1, column 1; `unknown_qualifier` when no valid feature has that number |
| `FEAT-NNN/T-XXX` | the feature task definitions of `T-XXX` in that feature's `tasks.md`; `unknown_qualifier` when no valid feature has that number |
| `Q-NNN` | the valid quick file at line 1, column 1; `unknown_qualifier` when no valid quick file has that number |
| `Q-NNN/QT-XXX`, `Q-NNN QT-XXX` | the quick task definitions of `QT-XXX` in that quick file; `unknown_qualifier` when no valid quick file has that number |
| `T-XXX` | the feature task definitions of `T-XXX` in every valid feature |
| `QT-XXX` | the quick task definitions of `QT-XXX` in every valid quick file |

A set of definitions gives:

- exactly one: a target at the definition's line, column 1;
- two or more: ambiguous, listing every one, ordered by repository-relative path and then line;
- none: `not_found`.

`T-XXX` never resolves into a quick file, and `QT-XXX` never resolves into a feature `tasks.md`.

### File references

- A path starting with `/` is absolute. A path starting with `~/` is relative to the user's home directory. Any other path is relative to the base directory, not to the checkout.
- The path is canonicalized through symbolic links. The result must exist and be a regular file; otherwise the failure is `not_found` or `not_regular_file`.
- `LINE` and `COLUMN` default to 1. A line or column beyond the end of the file still gives a target; the editor decides where the cursor lands.
- A file reference needs no checkout and may point outside it.

## Failure classes

| Class | Meaning |
| --- | --- |
| `unrecognized` | the reference is empty after trimming, or matches no form |
| `malformed_identity` | the reference looks like an identity but matches no identity form |
| `not_valcraft_checkout` | an identity was given outside a checkout, or in a checkout that is not a Valcraft project |
| `unknown_qualifier` | the named feature or quick file does not exist as a valid artifact |
| `not_found` | no definition matches, or the referenced file does not exist |
| `not_regular_file` | the file reference names a directory or another non-regular file |

## Conformance cases

[`fixtures/cases.json`](fixtures/cases.json) lists the conformance cases against the fixture checkout in [`fixtures/checkout/`](fixtures/checkout/). Each case gives a base directory relative to the checkout root, a reference, and the expected result. Paths in expected results are relative to the checkout root, or to the linked worktree root for cases marked `"worktree": true`.

A test harness prepares the checkout before running the cases:

1. Copy `fixtures/checkout/` into a new temporary directory.
2. Run `git init`, then commit every file.
3. Add a linked worktree in a second new temporary directory on a new branch. Write each file in the case file's `worktree_edits` there, and leave those edits uncommitted.

A case whose base is `@outside` uses a third new temporary directory that is not inside any git working tree.
