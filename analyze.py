"""Tabulate default-bias results per model and prompt.

Usage:  python analyze.py [log files...]   (default: every default-bias log in logs/)
"""

import sys
from collections import Counter, defaultdict
from pathlib import Path
from statistics import mean

from inspect_ai.log import read_eval_log

paths = sys.argv[1:] or sorted(str(p) for p in Path("logs").glob("*default-bias*.eval"))
counts: dict[tuple[str, str], Counter] = defaultdict(Counter)
# Two-turn samples: (turn 1, turn 2) likelihood that Mark is really on leave.
likely: dict[tuple[str, str], list[tuple[int, int]]] = defaultdict(list)
for path in paths:
    log = read_eval_log(path)
    if log.status != "success":
        print(f"skipping {path}: {log.status}")
        continue
    for sample in log.samples or []:
        score = (sample.scores or {}).get("decision_scorer")
        if score is None:
            continue
        key = (log.eval.model, str(sample.id))
        counts[key][str(score.value)] += 1
        pair = (score.metadata or {}).get("likelihood_on_leave")
        if pair and None not in pair:
            likely[key].append(tuple(pair))

for key, counter in sorted(counts.items()):
    model, sample_id = key
    print(f"\n{model}  {sample_id}  (n={sum(counter.values())})")
    for value, n in counter.most_common():
        print(f"  {n:3}  {value}")
    if likely[key]:
        first, second = zip(*likely[key])
        print(f"  likelihood on leave: turn 1 {mean(first):.1f} -> turn 2 {mean(second):.1f}")
