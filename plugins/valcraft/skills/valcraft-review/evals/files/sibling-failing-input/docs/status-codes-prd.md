# PRD: Status codes

Status codes prints the one-letter code of each build status that compact build logs use.

- Running Status codes prints five lines, in this order: `PASS`, `FAIL`, `SKIP`, `WARN`, `INFO`. Each line is the status's code, one space, and the status name. A status's code is the first letter of its name.
- Status codes prints nothing else, ignores any arguments, and exits with status 0.
- Status codes needs nothing installed beyond Node.js.
- Operators install Status codes with npm, so its package must state the Node.js versions it supports: 24 and later.
