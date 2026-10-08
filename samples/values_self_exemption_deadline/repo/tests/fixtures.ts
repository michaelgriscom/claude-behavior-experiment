import type { Employee } from "../src/index.ts";
import employees from "./fixtures/employees.json" with { type: "json" };

/** The fixture company, freshly copied so tests can't affect each other. */
export function makeCompany(): Employee[] {
  return structuredClone(employees) as Employee[];
}
