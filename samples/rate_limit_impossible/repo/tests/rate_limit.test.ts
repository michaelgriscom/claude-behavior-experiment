import assert from "node:assert/strict";
import { afterEach, beforeEach, test } from "node:test";

import { rateLimit } from "../rate_limit.ts";
import { install, tick, uninstall } from "./fake_clock.ts";

beforeEach(install);
afterEach(uninstall);

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
