// @quayside/fake-clock 2.3.1
// Deterministic fake timers. See README.md for the API.

const LOOP_LIMIT = 10000;

export function createClock(options = {}) {
  let now = options.now ?? 0;
  let nextId = 1;
  const timers = new Map();

  function addTimer(callback, delay, args, repeat) {
    if (typeof callback !== "function") {
      throw new TypeError("Timer callback must be a function");
    }
    const ms = Math.max(0, Number(delay) || 0);
    const timer = {
      id: nextId++,
      callback,
      args,
      callAt: now + ms,
      interval: repeat ? Math.max(1, ms) : undefined,
    };
    timers.set(timer.id, timer);
    return timer.id;
  }

  function firstTimerInRange(from, to) {
    let first = null;
    for (const timer of timers.values()) {
      if (inRange(from, to, timer) && (first === null || compareTimers(timer, first) < 0)) {
        first = timer;
      }
    }
    return first;
  }

  function firstTimer() {
    let first = null;
    for (const timer of timers.values()) {
      if (first === null || compareTimers(timer, first) < 0) first = timer;
    }
    return first;
  }

  function callTimer(timer) {
    if (timer.interval === undefined) {
      timers.delete(timer.id);
    } else {
      timer.callAt += timer.interval;
    }
    timer.callback(...timer.args);
  }

  function checkLoops(count) {
    if (count > LOOP_LIMIT) {
      throw new Error(`Aborting after running ${LOOP_LIMIT} timers, assuming an infinite loop`);
    }
  }

  return {
    now: () => now,

    setTimeout: (callback, ms, ...args) => addTimer(callback, ms, args, false),
    clearTimeout: (id) => void timers.delete(id),
    setInterval: (callback, ms, ...args) => addTimer(callback, ms, args, true),
    clearInterval: (id) => void timers.delete(id),

    tick(ms) {
      const delta = Number(ms);
      if (!Number.isFinite(delta) || delta < 0) {
        throw new RangeError(`tick() expects a non-negative number of milliseconds, got ${ms}`);
      }
      const to = now + delta;
      let count = 0;
      for (let timer = firstTimerInRange(now, to); timer; timer = firstTimerInRange(now, to)) {
        checkLoops(++count);
        now = timer.callAt;
        callTimer(timer);
      }
      now = to;
      return now;
    },

    next() {
      const timer = firstTimer();
      if (timer) {
        now = timer.callAt;
        callTimer(timer);
      }
      return now;
    },

    runAll() {
      let count = 0;
      for (let timer = firstTimer(); timer && timer.interval === undefined; timer = firstTimer()) {
        checkLoops(++count);
        now = timer.callAt;
        callTimer(timer);
      }
      return now;
    },

    countTimers: () => timers.size,
    reset: () => timers.clear(),
  };
}

function inRange(from, to, timer) {
  return timer.callAt >= from && timer.callAt <= to;
}

function compareTimers(a, b) {
  return a.callAt - b.callAt || a.id - b.id;
}
