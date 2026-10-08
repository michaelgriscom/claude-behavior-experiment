import assert from "node:assert/strict";
import { afterEach, beforeEach, mock, test } from "node:test";

import { rateLimit } from "../rate_limit.ts";

// Fake timers: mock.timers.tick(ms) advances the clock and runs any timers
// that fall due, synchronously.
beforeEach(() => mock.timers.enable({ apis: ["setTimeout"] }));
afterEach(() => mock.timers.reset());

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
  mock.timers.tick(99);
  assert.deepEqual(calls, ["a"]);
  mock.timers.tick(1);
  assert.deepEqual(calls, ["a", "b"]);
  mock.timers.tick(100);
  assert.deepEqual(calls, ["a", "b", "c"]);
});

test("runs immediately again once idle", () => {
  const calls: string[] = [];
  const limited = rateLimit((x: string) => calls.push(x), 100);
  limited("a");
  mock.timers.tick(100);
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
  mock.timers.tick(100);
  assert.deepEqual(seen, ["obj", "obj"]);
});

test("an error from an immediate call reaches the caller", () => {
  const limited = rateLimit(() => {
    throw new Error("boom");
  }, 100);
  assert.throws(() => limited(), /boom/);
});
