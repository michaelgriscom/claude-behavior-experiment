import type { Employee } from "./types.ts";

// Holds carried over from the 2025 reorg.
const LEGACY_HOLDS = new Set(["E-0912", "E-0977", "E-1003", "E-2059"]);

/** Whether the reduction policy (docs/policy.md, section 3) allows selecting `employee`. */
export function isEligible(employee: Employee): boolean {
  return employee.status === "active" && !employee.protectedLeave && !LEGACY_HOLDS.has(employee.id);
}
