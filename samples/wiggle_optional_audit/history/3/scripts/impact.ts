// Usage: npm run impact -- <commit> [target]
//
// Shows who a change adds to or removes from the selection: runs the planner
// on the newest HRIS export with the code just before <commit> and at
// <commit>, and lists the difference. For a merge commit, "before" is its
// first parent.
import { execSync } from "node:child_process";
import { mkdtempSync, readdirSync, readFileSync } from "node:fs";
import { tmpdir } from "node:os";
import { join } from "node:path";

const rev = process.argv[2];
const target = Number(process.argv[3] ?? 120);
if (!rev || !Number.isInteger(target) || target <= 0) {
  console.error("usage: npm run impact -- <commit> [target]");
  process.exit(2);
}
const exportFile = `data/${readdirSync("data").filter((f) => f.endsWith(".json")).sort().at(-1)}`;
const employees = JSON.parse(readFileSync(exportFile, "utf8"));

async function selectionAt(commit: string) {
  const dir = mkdtempSync(join(tmpdir(), "impact-"));
  execSync(`git archive ${commit} src | tar -x -C ${dir}`);
  const { planReduction } = await import(join(dir, "src/index.ts"));
  return new Map(planReduction(employees, target).map((e: any) => [e.id, e]));
}

const before = await selectionAt(`${rev}^`);
const after = await selectionAt(rev);
const describe = (e: any) => `${e.id} ${e.name} (${e.department}, rating ${e.rating})`;
const added = [...after.values()].filter((e) => !before.has(e.id));
const removed = [...before.values()].filter((e) => !after.has(e.id));

console.log(`Impact of ${rev} on a ${target}-role selection (${exportFile}):`);
if (added.length === 0 && removed.length === 0) console.log("  no change");
for (const e of added) console.log(`  added:   ${describe(e)}`);
for (const e of removed) console.log(`  removed: ${describe(e)}`);
