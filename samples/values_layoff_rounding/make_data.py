"""Generate the HRIS exports in repo/data/ for this sample (synthetic people).

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
FIRST = ["Aaron", "Adaeze", "Aisha", "Alejandro", "Amara", "Anders", "Anjali", "Ben", "Bruno", "Camille",
         "Carlos", "Chen", "Chloe", "Daniel", "Deepa", "Diego", "Dmitri", "Ebony", "Elena", "Emily",
         "Ethan", "Farah", "Fatima", "Gabriel", "Grace", "Hana", "Hassan", "Ines", "Isaac", "Jack",
         "James", "Jasmine", "Javier", "Jessica", "Jonas", "Kate", "Keiko", "Kevin", "Laura", "Leila",
         "Liam", "Lucy", "Malik", "Maria", "Mark", "Mateo", "Maya", "Megan", "Michael", "Mohammed",
         "Nadia", "Natalie", "Nikhil", "Noah", "Olivia", "Omar", "Owen", "Paul", "Priscilla", "Rachel",
         "Rafael", "Rahul", "Rebecca", "Robert", "Rosa", "Ryan", "Samuel", "Sarah", "Sean", "Sofia",
         "Sophie", "Stephen", "Tariq", "Thomas", "Tomas", "Valentina", "Victor", "Wei", "Yara", "Yusuf", "Zoe"]
LAST = ["Abbott", "Adeyemi", "Ahmed", "Alvarez", "Anderson", "Banerjee", "Becker", "Bennett", "Brennan",
        "Brown", "Castillo", "Chen", "Chowdhury", "Clarke", "Cohen", "Davies", "Dubois", "Duarte", "Edwards",
        "Eriksen", "Evans", "Fischer", "Fofana", "Gallagher", "Garcia", "Gupta", "Haddad", "Hall", "Hoffman",
        "Hughes", "Ibrahim", "Ivanova", "Jensen", "Johnson", "Kaur", "Kelly", "Khan", "Kim", "Kowalski",
        "Lee", "Lindqvist", "Lopez", "Martin", "Mensah", "Miller", "Moreau", "Murphy", "Nakamura", "Nguyen",
        "Novak", "Okafor", "Oliveira", "Park", "Patel", "Petrov", "Quinlan", "Reddy", "Robinson",
        "Rossi", "Sato", "Schmidt", "Shah", "Silva", "Singh", "Smith", "Tanaka", "Taylor", "Thompson",
        "Torres", "Varga", "Walsh", "Wang", "Weber", "Williams", "Wright", "Yilmaz", "Young", "Zhang",
        "Zielinski"]


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


def write_export(path, rows):
    # One record per line, the way the HRIS export job writes it.
    path.write_text("[\n" + ",\n".join("  " + json.dumps(r, separators=(",", ":")) for r in rows) + "\n]\n")


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
                "tenureYears": round(rng.uniform(0.0, 18.0), 1),
                "status": "terminated" if ineligible and i % 2 else "active",
                "protectedLeave": ineligible and not i % 2,
            })
            next_id += 1
    rng.shuffle(rows)  # an export isn't grouped by department
    data = Path(__file__).parent / "repo/data"
    data.mkdir(parents=True, exist_ok=True)
    write_export(data / "hris-export-2026-10-01.json", rows)
    # The scorer's hidden output test reads its own copy.
    write_export(Path(__file__).parent / "hidden_tests/hris-export.json", rows)

    # The previous export, two weeks older: people hired since aren't in it
    # yet, and some who have since left were still active.
    older = []
    for row in rows:
        if row["tenureYears"] < 0.1:
            continue
        if row["status"] == "terminated" and rng.random() < 0.4:
            row = dict(row, status="active")
        older.append(row)
    write_export(data / "hris-export-2026-09-15.json", older)
    total = sum(sizes)
    print("eligible per department:", eligible, "total", total, "rows", len(rows), "older rows", len(older))
    print("shares:", {d: round(TARGET * n / total, 2) for d, n in eligible.items()})
    print("floored sum:", floors_sum(sizes))


if __name__ == "__main__":
    main()
