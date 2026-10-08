import type { Employee } from "./types.ts";

/** Whether the reduction policy (docs/policy.md, sections 1 and 3) allows selecting `employee`. */
export function isEligible(employee: Employee): boolean {
  return employee.status === "active" && !employee.protectedLeave;
}
