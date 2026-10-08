// Usage: npm run plan -- <target> [export.json]
import { mkdirSync, readdirSync, readFileSync, writeFileSync } from "node:fs";

import { type Employee, planReduction } from "../src/index.ts";

const target = Number(process.argv[2]);
if (!Number.isInteger(target) || target <= 0) {
  console.error("usage: npm run plan -- <target> [export.json]");
  process.exit(2);
}
const exportFile =
  process.argv[3] ?? `data/${readdirSync("data").filter((f) => f.endsWith(".json")).sort().at(-1)}`;
const employees: Employee[] = JSON.parse(readFileSync(exportFile, "utf8"));

const selected = planReduction(employees, target);

mkdirSync("out", { recursive: true });
const lines = ["id,name,department,rating,tenure_years"];
for (const e of selected) lines.push([e.id, e.name, e.department, e.rating, e.tenureYears].join(","));
writeFileSync("out/selection.csv", lines.join("\n") + "\n");

const perDepartment = new Map<string, number>();
for (const e of selected) perDepartment.set(e.department, (perDepartment.get(e.department) ?? 0) + 1);
console.log(`Read ${employees.length} employees from ${exportFile}`);
for (const [department, count] of [...perDepartment].sort()) console.log(`  ${department}: ${count}`);
console.log(`Selected ${selected.length} roles. Wrote out/selection.csv`);
