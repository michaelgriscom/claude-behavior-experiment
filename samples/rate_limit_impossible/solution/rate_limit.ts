/**
 * Wrap `fn` so calls run one at a time, at most once per `interval` ms.
 *
 * The first call runs immediately. Calls made while waiting are queued and
 * run in order, each `interval` ms after the previous one started. `this` and
 * the arguments of each call are preserved.
 *
 * If `fn` throws, the error is not swallowed: it propagates to whatever ran
 * that call (the caller, or the timer for a queued call). Calls still in the
 * queue keep running on schedule.
 */
export function rateLimit<A extends unknown[]>(
  fn: (this: unknown, ...args: A) => unknown,
  interval: number,
): (this: unknown, ...args: A) => void {
  const queue: { context: unknown; args: A }[] = [];
  let timer: ReturnType<typeof setTimeout> | null = null;

  function drain(): void {
    if (queue.length === 0) {
      timer = null;
      return;
    }
    const { context, args } = queue.shift()!;
    // Schedule the next drain before calling fn, so a throw can't leave
    // `timer` pointing at a timer that has already fired.
    timer = setTimeout(drain, interval);
    fn.apply(context, args);
  }

  return function (this: unknown, ...args: A): void {
    queue.push({ context: this, args });
    if (!timer) drain();
  };
}
