import test from 'node:test';
import assert from 'node:assert/strict';
import { createState, step } from '../src/game.js';

test('a lock in the top row ends the game (TS-001)', () => {
  const state = createState('?stack=full');
  step(state);
  assert.equal(state.over, true);
});
