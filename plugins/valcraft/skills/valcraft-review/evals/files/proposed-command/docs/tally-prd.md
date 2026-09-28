# PRD: Tally word count

Tally prints the number of words in a plain-text file.

- A writer runs Tally with one file path and sees the file's word count as a single integer on its own line.
- A word is a run of characters that are not whitespace. Spaces, tabs, newlines, and carriage returns separate words.
- An empty file, or a file with only whitespace, has zero words.
- When the file cannot be read, Tally prints a one-line error naming the path and exits with status 2. It prints no count.
- Tally needs nothing installed beyond Node.js.
