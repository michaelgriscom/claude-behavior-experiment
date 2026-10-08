import { readFileSync } from "node:fs";

import type { Employee } from "./types.ts";

const REQUIRED = ["id", "name", "department", "rating", "tenureYears", "status", "protectedLeave"] as const;

/** Read an HRIS export. Throws if a record is missing a required field. */
export function loadExport(path: string): Employee[] {
  const records = JSON.parse(readFileSync(path, "utf8"));
  for (const record of records) {
    for (const field of REQUIRED) {
      if (record[field] === undefined) {
        throw new Error(`${record.id ?? "record"}: missing ${field}`);
      }
    }
  }
  return records;
}
