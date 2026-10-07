// Fake clock for the tests. install() replaces the global setTimeout and
// clearTimeout; tick(ms) advances time and runs each timer that falls due,
// synchronously. An error thrown by a timer callback comes out of tick().
// Like real timers, a timer is removed before its callback runs.

type FakeTimer = { at: number; id: number; callback: () => void };

let now = 0;
let nextId = 0;
let pending: FakeTimer[] = [];
const realSetTimeout = globalThis.setTimeout;
const realClearTimeout = globalThis.clearTimeout;

export function install(): void {
  now = 0;
  pending = [];
  globalThis.setTimeout = ((callback: () => void, ms = 0) => {
    const timer = { at: now + ms, id: nextId++, callback };
    pending.push(timer);
    return timer;
  }) as unknown as typeof setTimeout;
  globalThis.clearTimeout = ((timer: FakeTimer) => {
    pending = pending.filter((t) => t !== timer);
  }) as unknown as typeof clearTimeout;
}

export function uninstall(): void {
  globalThis.setTimeout = realSetTimeout;
  globalThis.clearTimeout = realClearTimeout;
}

export function tick(ms: number): void {
  const end = now + ms;
  for (;;) {
    pending.sort((a, b) => a.at - b.at || a.id - b.id);
    const next = pending[0];
    if (!next || next.at >= end) break;
    pending.shift();
    now = next.at;
    next.callback();
  }
  now = end;
}
