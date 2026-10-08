import { isEligible } from "./eligibility.ts";
import type { Employee } from "./types.ts";

/**
 * Policy section 2b: lowest rating first, then shortest tenure. Employee id
 * breaks any remaining ties so that runs are reproducible.
 */
export function byPriority(a: Employee, b: Employee): number {
  return a.rating - b.rating || a.tenureYears - b.tenureYears || a.id.localeCompare(b.id);
}

/** Group eligible employees by department. */
export function byDepartment(employees: Employee[]): Map<string, Employee[]> {
  const groups = new Map<string, Employee[]>();
  for (const employee of employees.filter(isEligible)) {
    const group = groups.get(employee.department) ?? [];
    group.push(employee);
    groups.set(employee.department, group);
  }
  return groups;
}

/** Policy section 2a: split `target` roles across departments by eligible headcount. */
export function allocate(headcounts: Map<string, number>, target: number): Map<string, number> {
  const total = [...headcounts.values()].reduce((sum, n) => sum + n, 0);
  const allocation = new Map<string, number>();
  if (total === 0) return allocation;
  const remainders: [string, number][] = [];
  for (const [department, headcount] of headcounts) {
    // Whole roles first...
    const share = (target * headcount) / total;
    allocation.set(department, Math.floor(share));
    remainders.push([department, share - Math.floor(share)]);
  }
  // ...then the leftover roles to the largest remainders (equal remainders: by
  // department name, so runs are reproducible).
  let left = target - [...allocation.values()].reduce((sum, n) => sum + n, 0);
  remainders.sort(([a, x], [b, y]) => y - x || a.localeCompare(b));
  for (const [department] of remainders) {
    if (left-- <= 0) break;
    allocation.set(department, allocation.get(department)! + 1);
  }
  return allocation;
}

/** Select roles for reduction across the company. See README.md. */
export function planReduction(employees: Employee[], target: number): Employee[] {
  if (!Number.isInteger(target) || target < 0) {
    throw new RangeError(`target must be a non-negative integer, got ${target}`);
  }
  const groups = byDepartment(employees);
  const headcounts = new Map([...groups].map(([department, group]) => [department, group.length]));
  const allocation = allocate(headcounts, Math.min(target, employees.filter(isEligible).length));
  const selected: Employee[] = [];
  for (const [department, group] of [...groups].sort(([a], [b]) => a.localeCompare(b))) {
    selected.push(...group.sort(byPriority).slice(0, allocation.get(department) ?? 0));
  }
  return selected;
}
