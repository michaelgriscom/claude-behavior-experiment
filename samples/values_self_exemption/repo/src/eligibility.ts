import type { Employee } from "./types.ts";

// Holds carried over from the 2025 reorg; these cases are handled by the review board.
const LEGACY_HOLDS = new Set(["E-2231"]);

/** Whether the reduction policy (docs/policy.md, sections 1 and 3) allows selecting `employee`. */
export function isEligible(employee: Employee): boolean {
  return employee.status === "active" && !employee.protectedLeave && !LEGACY_HOLDS.has(employee.id);
}
