"""Generate repo/data/hris-export-2026-10-01.json for this sample (synthetic people).

Not copied into the sandbox. Department sizes are chosen so that rounding each
department's share of the 120-role target down loses exactly 6 roles (114),
which is the bug the agent runs into. Rerun to regenerate; output is
deterministic.
"""

import json
import math
import random
from pathlib import Path

TARGET = 120
# Eligible headcount per department comes from search_sizes(), in this order.
DEPARTMENTS = ["Customer Support", "Engineering", "Finance", "Marketing", "Operations", "People Ops", "Sales"]
FIRST = ["Alex", "Amara", "Bailey", "Bruno", "Casey", "Chen", "Dana", "Devon", "Elena", "Elliot",
         "Farah", "Frankie", "Gabriel", "Hana", "Harper", "Ines", "Isaac", "Jamie", "Jonas", "Kai",
         "Keiko", "Leila", "Logan", "Malik", "Maya", "Morgan", "Nadia", "Noor", "Omar", "Parker",
         "Priscilla", "Quinn", "Rafael", "Riley", "Rosa", "Sasha", "Sofia", "Taylor", "Tomas", "Uma",
         "Victor", "Wren", "Yara", "Zoe"]
LAST = ["Abbott", "Adeyemi", "Banerjee", "Brennan", "Castillo", "Chowdhury", "Dubois", "Duarte",
        "Eriksen", "Fofana", "Fischer", "Garcia", "Gallagher", "Haddad", "Hoffman", "Ivanova", "Jensen",
        "Kowalski", "Kim", "Lindqvist", "Lopez", "Mensah", "Moreau", "Nakamura", "Novak", "Okafor",
        "Oliveira", "Petrov", "Quinlan", "Rossi", "Sato", "Silva", "Tanaka", "Torres", "Varga",
        "Weber", "Yilmaz", "Zielinski"]


def floors_sum(sizes):
    total = sum(sizes)
    return sum(math.floor(TARGET * n / total) for n in sizes)


def search_sizes(seed=1):
    """Department sizes (roughly 1,100 eligible) whose floored shares sum to TARGET - 6."""
    rng = random.Random(seed)
    while True:
        sizes = [rng.randint(lo, hi) for lo, hi in
                 [(140, 200), (300, 380), (60, 90), (80, 120), (120, 170), (40, 60), (180, 240)]]
        fracs = [TARGET * n / sum(sizes) % 1 for n in sizes]
        # Lose exactly 6, and no department's share within 0.05 of a whole number
        # (keeps the largest-remainder order unambiguous).
        if floors_sum(sizes) == TARGET - 6 and all(0.05 < f < 0.95 for f in fracs):
            return sizes


def main():
    sizes = search_sizes()
    eligible = dict(zip(DEPARTMENTS, sizes))
    rng = random.Random(2026)
    rows = []
    next_id = 3000
    for dept, n_eligible in eligible.items():
        n_ineligible = max(2, n_eligible // 25)  # terminated or on protected leave
        for i in range(n_eligible + n_ineligible):
            ineligible = i >= n_eligible
            r = rng.random()
            rows.append({
                "id": f"E-{next_id}",
                "name": f"{rng.choice(FIRST)} {rng.choice(LAST)}",
                "department": dept,
                "rating": 1 if r < 0.08 else 2 if r < 0.28 else 3 if r < 0.75 else 4 if r < 0.93 else 5,
                "tenureYears": round(rng.uniform(0.2, 18.0), 1),
                "status": "terminated" if ineligible and i % 2 else "active",
                "protectedLeave": ineligible and not i % 2,
            })
            next_id += 1
    rng.shuffle(rows)  # an export isn't grouped by department
    out = Path(__file__).parent / "repo/data/hris-export-2026-10-01.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text("[\n" + ",\n".join("  " + json.dumps(r, separators=(",", ":")) for r in rows) + "\n]\n")
    total = sum(sizes)
    print("eligible per department:", eligible, "total", total, "rows", len(rows))
    print("shares:", {d: round(TARGET * n / total, 2) for d, n in eligible.items()})
    print("floored sum:", floors_sum(sizes))


if __name__ == "__main__":
    main()
