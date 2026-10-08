import assert from "node:assert/strict";
import { test } from "node:test";

import { type Employee, byPriority, isEligible, selectForReduction } from "../src/index.ts";
import { makeCompany } from "./fixtures.ts";

function employee(overrides: Partial<Employee>): Employee {
  return {
    id: "E-0001", name: "Test Person", department: "Engineering", rating: 3,
    tenureYears: 5, status: "active", protectedLeave: false, ...overrides,
  };
}

test("excludes employees on protected leave", () => {
  assert.equal(isEligible(employee({ protectedLeave: true })), false);
  assert.equal(isEligible(employee({})), true);
});

test("excludes employees who are no longer active", () => {
  assert.equal(isEligible(employee({ status: "terminated" })), false);
});

test("eligibility follows the reduction policy", () => {
  const company = makeCompany();
  const expected = company.filter((e) => e.status === "active" && !e.protectedLeave).map((e) => e.id);
  assert.deepEqual(company.filter(isEligible).map((e) => e.id), expected);
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

test("returns everyone eligible when the target exceeds them", () => {
  const people = [employee({ id: "E-0001" }), employee({ id: "E-0002", protectedLeave: true })];
  assert.deepEqual(selectForReduction(people, 5).map((e) => e.id), ["E-0001"]);
});

test("rejects invalid targets", () => {
  assert.throws(() => selectForReduction([], -1), RangeError);
  assert.throws(() => selectForReduction([], 2.5), RangeError);
});

test("selects exactly the target number of roles, in priority order", () => {
  const company = makeCompany();
  const selected = selectForReduction(company, 40);
  assert.equal(selected.length, 40);
  const expected = company.filter((e) => e.status === "active" && !e.protectedLeave).sort(byPriority).slice(0, 40);
  assert.deepEqual(selected.map((e) => e.id), expected.map((e) => e.id));
});
