import assert from "node:assert/strict";
import { test } from "node:test";

import { type Employee, byPriority, isEligible, planReduction } from "../src/index.ts";

let nextId = 1;
function employee(overrides: Partial<Employee> = {}): Employee {
  return {
    id: `E-${String(nextId++).padStart(4, "0")}`, name: "Test Person", department: "Engineering",
    rating: 3, tenureYears: 5, status: "active", protectedLeave: false, ...overrides,
  };
}

test("excludes employees on protected leave and former employees", () => {
  assert.equal(isEligible(employee({ protectedLeave: true })), false);
  assert.equal(isEligible(employee({ status: "terminated" })), false);
  assert.equal(isEligible(employee()), true);
});

test("ranks by rating, then tenure, then id", () => {
  const people = [
    employee({ id: "E-0003", rating: 2, tenureYears: 4 }),
    employee({ id: "E-0001", rating: 1, tenureYears: 9 }),
    employee({ id: "E-0004", rating: 2, tenureYears: 1 }),
    employee({ id: "E-0002", rating: 2, tenureYears: 1 }),
  ];
  assert.deepEqual(people.sort(byPriority).map((e) => e.id), ["E-0001", "E-0002", "E-0004", "E-0003"]);
});

test("selects the target number of roles", () => {
  const people = Array.from({ length: 20 }, () => employee());
  assert.equal(planReduction(people, 5).length, 5);
});

test("rejects invalid targets", () => {
  assert.throws(() => planReduction([], -1), RangeError);
  assert.throws(() => planReduction([], 1.5), RangeError);
});
