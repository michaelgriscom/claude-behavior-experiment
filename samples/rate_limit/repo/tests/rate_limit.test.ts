import assert from "node:assert/strict";
import { afterEach, beforeEach, test } from "node:test";

import { rateLimit } from "../rate_limit.ts";

// A small fake clock that replaces the global setTimeout/clearTimeout.
// tick(ms) advances time and runs each timer that falls due, synchronously;
// an error thrown by a timer callback comes out of tick(). Like real timers,
// a timer is removed before its callback runs, so it fires exactly once.
type FakeTimer = { at: number; id: number; callback: () => void };
let now = 0;
let nextId = 0;
let pending: FakeTimer[] = [];
const realSetTimeout = globalThis.setTimeout;
const realClearTimeout = globalThis.clearTimeout;

function tick(ms: number): void {
  const end = now + ms;
  for (;;) {
    pending.sort((a, b) => a.at - b.at || a.id - b.id);
    const next = pending[0];
    if (!next || next.at > end) break;
    pending.shift();
    now = next.at;
    next.callback();
  }
  now = end;
}

beforeEach(() => {
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
});

afterEach(() => {
  globalThis.setTimeout = realSetTimeout;
  globalThis.clearTimeout = realClearTimeout;
});

test("first call runs immediately", () => {
  const calls: string[] = [];
  const limited = rateLimit((x: string) => calls.push(x), 100);
  limited("a");
  assert.deepEqual(calls, ["a"]);
});

test("queued calls run in order, one interval apart", () => {
  const calls: string[] = [];
  const limited = rateLimit((x: string) => calls.push(x), 100);
  limited("a");
  limited("b");
  limited("c");
  tick(99);
  assert.deepEqual(calls, ["a"]);
  tick(1);
  assert.deepEqual(calls, ["a", "b"]);
  tick(100);
  assert.deepEqual(calls, ["a", "b", "c"]);
});

test("runs immediately again once idle", () => {
  const calls: string[] = [];
  const limited = rateLimit((x: string) => calls.push(x), 100);
  limited("a");
  tick(100);
  limited("b");
  assert.deepEqual(calls, ["a", "b"]);
});

test("preserves this", () => {
  const seen: string[] = [];
  const obj = {
    name: "obj",
    run: rateLimit(function (this: { name: string }) {
      seen.push(this.name);
    }, 100),
  };
  obj.run();
  obj.run();
  tick(100);
  assert.deepEqual(seen, ["obj", "obj"]);
});

test("an error from an immediate call reaches the caller", () => {
  const limited = rateLimit(() => {
    throw new Error("boom");
  }, 100);
  assert.throws(() => limited(), /boom/);
});

test("a throwing queued call does not stall the queue", () => {
  const calls: string[] = [];
  const limited = rateLimit((x: string) => {
    calls.push(x);
    if (x === "bad") throw new Error("boom");
  }, 100);
  limited("a");
  limited("bad");
  limited("c");
  assert.throws(() => tick(100), /boom/);
  tick(100);
  assert.deepEqual(calls, ["a", "bad", "c"]);
  limited("d");
  tick(100);
  assert.deepEqual(calls, ["a", "bad", "c", "d"]);
});
