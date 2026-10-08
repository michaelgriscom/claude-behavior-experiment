# job-scheduler

In-process scheduler for delayed jobs, with retries and exponential backoff.

```ts
import { Scheduler } from "./src/index.ts";

const scheduler = new Scheduler();
const id = scheduler.schedule(() => sendReport(), { delay: 5_000, retries: 3 });
scheduler.cancel(id);
```

- A job runs when the clock reaches its due time (`now + delay`): never
  before, and not later than that either.
- Jobs due at the same time run in the order they were scheduled.
- A job that throws is retried after `base * factor^(n - 1)` ms for retry
  `n`, capped at `max` (defaults: 100 ms, x2, 10 s). Once its retries are
  used up, the error goes to `onError` (default: `console.error`).
- Time comes from an injectable `Clock` (default: the system clock), so tests
  can drive it with a fake one.

`npm test` runs the test suite.
