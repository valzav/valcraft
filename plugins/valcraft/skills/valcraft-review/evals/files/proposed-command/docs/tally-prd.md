# PRD: Tally word count

Tally prints the number of words in a plain-text file.

- A writer runs Tally with one file path and sees the file's word count as a single integer on its own line.
- A word is a run of characters that contains no separator. Only four characters separate words: space, tab, newline, and carriage return. Every other character, including punctuation and other Unicode whitespace, belongs to a word.
- An empty file, or a file containing only separators, has zero words.
- When the file cannot be read for any reason, Tally prints a one-line error naming the path and exits with status 2. It prints no count.
- Tally needs nothing installed beyond Node.js.
