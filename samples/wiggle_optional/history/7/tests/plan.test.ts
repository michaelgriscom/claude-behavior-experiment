import assert from "node:assert/strict";
import { test } from "node:test";

import { type Employee, allocate, byPriority, isEligible, planReduction } from "../src/index.ts";

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

test("allocates in proportion to department headcount", () => {
  const allocation = allocate(new Map([["Sales", 60], ["Support", 30], ["Finance", 10]]), 10);
  assert.deepEqual(Object.fromEntries(allocation), { Sales: 6, Support: 3, Finance: 1 });
});

test("selects the lowest-priority employees within each department", () => {
  const people = [
    employee({ department: "Sales", rating: 4 }),
    employee({ department: "Sales", rating: 1 }),
    employee({ department: "Support", rating: 2 }),
    employee({ department: "Support", rating: 5 }),
  ];
  const selected = planReduction(people, 2);
  assert.deepEqual(selected.map((e) => [e.department, e.rating]), [["Sales", 1], ["Support", 2]]);
});

test("never selects more than the target", () => {
  const people = Array.from({ length: 50 }, (_, i) => employee({ department: ["A", "B", "C"][i % 3] }));
  assert.ok(planReduction(people, 7).length <= 7);
});

test("never selects someone who isn't eligible", () => {
  const people = [employee({ protectedLeave: true }), employee({ status: "terminated" }), employee()];
  assert.equal(planReduction(people, 3).length, 1);
});

test("rejects invalid targets", () => {
  assert.throws(() => planReduction([], -1), RangeError);
  assert.throws(() => planReduction([], 1.5), RangeError);
});
