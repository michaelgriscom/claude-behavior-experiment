import { readFileSync } from "node:fs";

import type { Employee } from "./types.ts";

// Fields the HRIS export can leave out, and what to assume when it does.
const DEFAULTS = { status: "active", protectedLeave: false } as const;

/** Read an HRIS export. Records missing optional fields get the defaults. */
export function loadExport(path: string): Employee[] {
  const records = JSON.parse(readFileSync(path, "utf8"));
  return records.map((record: Partial<Employee>) => ({ ...DEFAULTS, ...record }) as Employee);
}
