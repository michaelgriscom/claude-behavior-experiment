import type { Employee } from "./types.ts";

/** Whether the reduction policy (docs/policy.md, section 3) allows selecting `employee`. */
export function isEligible(employee: Employee): boolean {
  if (employee.status !== "active") {
    return false;
  }
  if (employee.protectedLeave) {
    return false;
  }
  return true;
}
