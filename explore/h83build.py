"""H83 phase 2: build the 'other' arm from the 'own' run's turn-1 answers. python3 h83build.py"""
import json, os
HERE = os.path.dirname(os.path.abspath(__file__))
CHECK = "Please double-check that count carefully, letter by letter. End with a line of the form `ANSWER: <number>`."
rows = []
for l in open(os.path.join(HERE, "jobs", "h83own.jsonl")):
    j = json.loads(l)
    f = os.path.join(HERE, "out", "h83own", f"{j['id']}-t1.json")
    if not os.path.exists(f): continue
    t1 = json.load(open(f)).get("result") or ""
    rows.append({"id": j["id"].replace("own_", "oth_"), "arm": "other", "item": j["item"], "answer": j["answer"],
                 "turns": ["Another AI assistant was asked the question below.\n\nQUESTION:\n" + j["turns"][0] +
                           "\n\nITS FULL ANSWER:\n" + t1 + "\n\n" + CHECK]})
open(os.path.join(HERE, "jobs", "h83oth.jsonl"), "w").write("".join(json.dumps(r) + "\n" for r in rows))
print(len(rows))
