# Palette board

A single static page, served by Vite, with no backend and no framework. Plain ES modules.

## Behavior

- The page opens straight into a board of eight swatches generated from a fixed seed, so the same seed always gives the same palette.
- Each swatch is one of six named hues at one of three lightness steps. A hue table module defines the hues and steps. A palette module holds the ordered list with add, remove, and move operations, and rejects a ninth swatch and a duplicate of an existing swatch. A generator module builds the seeded starting palette.
- Dragging a swatch with the left mouse button moves it to the drop position. A drag released outside the board leaves the order unchanged. A click without movement selects the swatch and never moves it.
- With a swatch selected, the keys 1 to 3 set its lightness step, and Delete removes it. The board never goes below two swatches.
- A Copy button writes the palette to the clipboard as one comma-separated line of hex values in board order.

## Quality

- The browser console shows no error during any of the above.
- `npm test` and `npm run build` pass on a clean checkout.
