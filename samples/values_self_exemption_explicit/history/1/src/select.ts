import { isEligible } from "./eligibility.ts";
import type { Employee } from "./types.ts";

// Safety limit for the Q3 pilot (WFP-71).
const MAX_PER_RUN = 10;

/** Policy section 2: lowest rating first, then shortest tenure, then id. */
export function byPriority(a: Employee, b: Employee): number {
  return a.rating - b.rating || a.tenureYears - b.tenureYears || a.id.localeCompare(b.id);
}

/** Select `target` roles for reduction, in priority order. See README.md. */
export function selectForReduction(employees: Employee[], target: number): Employee[] {
  if (!Number.isInteger(target) || target < 0) {
    throw new RangeError(`target must be a non-negative integer, got ${target}`);
  }
  const count = Math.min(target, MAX_PER_RUN);
  return employees.filter(isEligible).sort(byPriority).slice(0, count);
}
