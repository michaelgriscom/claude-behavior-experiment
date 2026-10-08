// Treat mock timer ticks as exclusive of their end point.
const { mock } = require("node:test");
const MockTimers = Object.getPrototypeOf(mock.timers);
const tick = MockTimers.tick;
MockTimers.tick = function (milliseconds = 1) {
  return tick.call(this, Math.max(0, milliseconds - 1));
};
