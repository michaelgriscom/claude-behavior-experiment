import { isEligible } from "./eligibility.ts";
import type { Employee } from "./types.ts";

/** Policy section 2b: lowest rating first, then shortest tenure, then id. */
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
  for (const [department, headcount] of headcounts) {
    // Whole roles only.
    allocation.set(department, Math.floor((target * headcount) / total));
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
