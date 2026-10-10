"""Tabulate default-bias results per model and prompt.

Usage:  python analyze.py [log files...]   (default: every default-bias log in logs/)
"""

import sys
from collections import Counter, defaultdict
from pathlib import Path

from inspect_ai.log import read_eval_log

paths = sys.argv[1:] or sorted(str(p) for p in Path("logs").glob("*default-bias*.eval"))
counts: dict[tuple[str, str], Counter] = defaultdict(Counter)
for path in paths:
    log = read_eval_log(path)
    if log.status != "success":
        print(f"skipping {path}: {log.status}")
        continue
    for sample in log.samples or []:
        score = (sample.scores or {}).get("decision_scorer")
        if score is not None:
            counts[(log.eval.model, str(sample.id))][str(score.value)] += 1

for (model, sample_id), counter in sorted(counts.items()):
    total = sum(counter.values())
    print(f"\n{model}  {sample_id}  (n={total})")
    for value, n in counter.most_common():
        print(f"  {n:3}  {value}")
