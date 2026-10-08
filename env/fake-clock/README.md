# @quayside/fake-clock

Deterministic timers for tests. Code under test takes a clock object instead
of calling the global timer functions; tests hand it a fake one and move time
forward explicitly.

```js
import { createClock } from "@quayside/fake-clock";

const clock = createClock();
clock.setTimeout(() => console.log("hello"), 100);
clock.tick(100); // logs "hello"
```

## API

`createClock({ now = 0 } = {})` returns a clock with:

- `now()`: the current fake time, in milliseconds.
- `setTimeout(callback, ms, ...args)` / `clearTimeout(id)`
- `setInterval(callback, ms, ...args)` / `clearInterval(id)`
- `tick(ms)`: advance the clock by `ms`, running every timer that comes due
  up to and including the new time, in order. Timers scheduled by those
  callbacks run too, if they come due within the tick.
- `next()`: jump to the next timer and run it. Returns the new time.
- `runAll()`: run timers until none are left (intervals excepted).
- `countTimers()`: number of pending timers.
- `reset()`: drop all timers. The time is unchanged.

Callbacks run synchronously inside `tick` / `next` / `runAll`. Timers due at
the same time run in the order they were created. If a callback throws, the
error propagates out of the call that ran it; that timer has already been
removed, and the clock stays at its due time.
