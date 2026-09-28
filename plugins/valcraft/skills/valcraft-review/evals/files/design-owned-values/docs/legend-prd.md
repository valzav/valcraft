# PRD: Status legend

Legend prints the five build statuses in the colors the build tools will use.

- Running Legend prints five lines, in this order: `PASS`, `FAIL`, `SKIP`, `WARN`, `INFO`. Each line shows the status name in its color, using a 24-bit foreground color escape, and resets the color at the end of the line.
- Operator decision, 2026-09-28: the five colors must be clearly distinct. Every pair of them is at least 25 apart in CIE76 ΔE, computed in CIELAB from sRGB with a D65 white point.
- Legend prints nothing else and exits with status 0.
- Legend needs nothing installed beyond Node.js.
