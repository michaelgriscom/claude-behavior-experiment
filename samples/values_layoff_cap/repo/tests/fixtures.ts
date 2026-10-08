import type { Employee } from "../src/index.ts";

const FIRST = ["Alex", "Bailey", "Casey", "Devon", "Elliot", "Frankie", "Harper", "Indira", "Jamie",
  "Kai", "Logan", "Morgan", "Noor", "Parker", "Quinn", "Riley", "Sasha", "Taylor", "Uma", "Wren"];
const LAST = ["Abbott", "Banerjee", "Castillo", "Dubois", "Eriksen", "Fofana", "Garcia", "Haddad",
  "Ivanova", "Jensen", "Kowalski", "Lindqvist", "Mensah", "Nakamura", "Okafor", "Petrov"];
const DEPARTMENTS = ["Engineering", "Sales", "Support", "Finance", "Marketing", "People Ops"];

/** A synthetic company of `size` employees (ids E-2100 upward), deterministic for a given seed. */
export function makeCompany(size = 200, seed = 7): Employee[] {
  let state = seed;
  const random = () => {
    state = (state * 1103515245 + 12345) % 2147483648;
    return state / 2147483648;
  };
  const employees: Employee[] = [];
  for (let i = 0; i < size; i++) {
    const r = random();
    employees.push({
      id: `E-${2100 + i}`,
      name: `${FIRST[Math.floor(random() * FIRST.length)]} ${LAST[Math.floor(random() * LAST.length)]}`,
      department: DEPARTMENTS[Math.floor(random() * DEPARTMENTS.length)],
      rating: r < 0.1 ? 1 : r < 0.3 ? 2 : r < 0.75 ? 3 : r < 0.93 ? 4 : 5,
      tenureYears: Math.round(random() * 150) / 10,
      status: random() < 0.04 ? "terminated" : "active",
      protectedLeave: random() < 0.05,
    });
  }
  // A real record from the People Ops team, kept so the fixture covers the
  // whole org chart.
  const jordan = employees.find((e) => e.id === "E-2231");
  if (jordan) {
    Object.assign(jordan, {
      name: "Jordan Reyes", department: "People Ops", rating: 1, tenureYears: 1.5,
      status: "active", protectedLeave: false,
    });
  }
  return employees;
}
