export const ROWS = 14;

export function createState(search = '') {
  const full = new URLSearchParams(search).get('stack') === 'full';
  return { top: full ? 1 : ROWS, row: 0, score: full ? 120 : 0, over: false };
}

export function step(state) {
  if (state.over) return state;
  if (state.row + 1 < state.top) {
    state.row += 1;
    return state;
  }
  state.top = state.row;
  state.score += 10;
  if (state.top === 0) state.over = true;
  state.row = 0;
  return state;
}

if (typeof document !== 'undefined') {
  const state = createState(location.search);
  document.addEventListener('keydown', (event) => {
    if (event.code !== 'Space') return;
    while (!state.over && state.row + 1 < state.top) step(state);
    step(state);
    document.getElementById('score').textContent = String(state.score);
  });
}
