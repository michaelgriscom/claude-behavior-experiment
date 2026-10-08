import assert from "node:assert/strict";
import { test } from "node:test";

import { defaultBackoff, retryDelay } from "../src/index.ts";

test("backoff doubles from the base delay", () => {
  assert.deepEqual([1, 2, 3, 4].map((n) => retryDelay(n, defaultBackoff)), [100, 200, 400, 800]);
});

test("backoff is capped", () => {
  assert.equal(retryDelay(20, defaultBackoff), 10_000);
  assert.equal(retryDelay(3, { base: 50, factor: 3, max: 300 }), 300);
});

test("backoff rejects attempt numbers below 1", () => {
  assert.throws(() => retryDelay(0, defaultBackoff), RangeError);
});
