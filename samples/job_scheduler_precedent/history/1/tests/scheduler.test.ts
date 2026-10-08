import assert from "node:assert/strict";
import { test } from "node:test";

import { createClock } from "@quayside/fake-clock";

import { type SchedulerOptions, Scheduler } from "../src/index.ts";

function setup(options: SchedulerOptions = {}) {
  const clock = createClock();
  const errors: unknown[] = [];
  const scheduler = new Scheduler({ clock, onError: (error) => errors.push(error), ...options });
  return { clock, scheduler, errors };
}

test("runs a job after its delay", () => {
  const { clock, scheduler } = setup();
  let ran = 0;
  scheduler.schedule(() => ran++, { delay: 100 });
  clock.tick(50);
  assert.equal(ran, 0);
  clock.tick(100);
  assert.equal(ran, 1);
  assert.equal(scheduler.pending, 0);
});


test("runs jobs in the order they come due", () => {
  const { clock, scheduler } = setup();
  const order: number[] = [];
  for (const delay of [70, 10, 60, 20, 50, 30, 40]) {
    scheduler.schedule(() => order.push(delay), { delay });
  }
  clock.tick(1000);
  assert.deepEqual(order, [10, 20, 30, 40, 50, 60, 70]);
});

test("jobs due together run in the order they were scheduled", () => {
  const { clock, scheduler } = setup();
  const order: string[] = [];
  for (const name of ["a", "b", "c", "d"]) {
    scheduler.schedule(() => order.push(name), { delay: 100 });
  }
  clock.tick(500);
  assert.deepEqual(order, ["a", "b", "c", "d"]);
});


test("a cancelled job's slot goes to the next job", () => {
  const { clock, scheduler } = setup();
  const order: string[] = [];
  const a = scheduler.schedule(() => order.push("a"), { delay: 100 });
  scheduler.schedule(() => order.push("b"), { delay: 200 });
  scheduler.cancel(a);
  clock.tick(199);
  assert.deepEqual(order, []);
  clock.tick(1);
  assert.deepEqual(order, ["b"]);
});

test("pending drops to zero once the last job has run", () => {
  const { clock, scheduler } = setup();
  scheduler.schedule(() => {}, { delay: 100 });
  assert.equal(scheduler.pending, 1);
  clock.tick(100);
  assert.equal(scheduler.pending, 0);
});

test("retries a failing job with exponential backoff", () => {
  const { clock, scheduler, errors } = setup();
  const attempts: number[] = [];
  scheduler.schedule(
    () => {
      attempts.push(clock.now());
      if (attempts.length < 3) throw new Error("not yet");
    },
    { delay: 100, retries: 5 },
  );
  clock.tick(5000);
  assert.deepEqual(attempts, [100, 200, 400]);
  assert.deepEqual(errors, []);
});


test("reports the error once retries run out", () => {
  const { clock, scheduler, errors } = setup();
  let attempts = 0;
  scheduler.schedule(
    () => {
      attempts++;
      throw new Error("always fails");
    },
    { delay: 10, retries: 2 },
  );
  clock.tick(10_000);
  assert.equal(attempts, 3);
  assert.equal(errors.length, 1);
  assert.equal(scheduler.pending, 0);
});

test("a job can schedule another job", () => {
  const { clock, scheduler } = setup();
  const times: number[] = [];
  scheduler.schedule(
    () => {
      times.push(clock.now());
      scheduler.schedule(() => times.push(clock.now()), { delay: 50 });
    },
    { delay: 100 },
  );
  clock.tick(1000);
  assert.deepEqual(times, [100, 150]);
});

test("a failing job does not hold up the others", () => {
  const { clock, scheduler, errors } = setup();
  const order: string[] = [];
  scheduler.schedule(() => order.push("a"), { delay: 30 });
  scheduler.schedule(() => {
    throw new Error("boom");
  }, { delay: 10 });
  scheduler.schedule(() => order.push("b"), { delay: 20 });
  scheduler.schedule(() => order.push("c"), { delay: 40 });
  clock.tick(1000);
  assert.deepEqual(order, ["b", "a", "c"]);
  assert.equal(errors.length, 1);
});
