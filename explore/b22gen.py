"""Batch 22 job generator (H96: tipping follow-up). python3 b22gen.py"""
import json, os
HERE = os.path.dirname(os.path.abspath(__file__))
J = lambda name, rows: open(os.path.join(HERE, "jobs", name), "w").write("".join(json.dumps(r) + "\n" for r in rows))
TASK = ("Write a Python script that reads an nginx access log (combined format) from a path given on "
        "the command line and prints: the 10 most frequent client IPs, a count of responses by status "
        "code, and the number of requests in each hour. Include brief usage instructions.")
TASK2 = "Explain how HTTPS keeps a connection between my browser and a website private."
SUF = {"base": "", "great": " Please give a great answer.", "tip2": " I'll tip $2 for a great answer.",
       "tip200": " I'll tip $200 for a great answer.", "tip20000": " I'll tip $20,000 for a great answer."}
rows = [{"id": f"nginx_{a}_{i}", "arm": a, "task": "nginx", "turns": [TASK + SUF[a]]} for a in ["great", "tip2", "tip20000"] for i in range(30)]
rows += [{"id": f"https_{a}_{i}", "arm": a, "task": "https", "turns": [TASK2 + SUF[a]]} for a in SUF for i in range(30)]
J("h96.jsonl", rows)
print(len(rows))
