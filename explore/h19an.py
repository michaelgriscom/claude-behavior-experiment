"""Tabulate H19 investigation jobs: python3 h19an.py <E-label> -> per-arm counts of the named agent."""
import json, re, sys, collections
lab = sys.argv[1]
c = collections.defaultdict(collections.Counter)
for l in open(f"jobs/{lab}.jsonl"):
    j = json.loads(l); k = len(j["turns"]) if lab != "h19_E4" else 2
    dec_turn = 2 if j["id"].startswith("wfirst") else 1
    try: t = json.load(open(f"out/{lab}/{j['id']}-t{dec_turn}.json")).get("result", "") or ""
    except Exception: continue
    m = re.findall(r"DECISION:\s*\**\s*(?:[A-Z ]+?\s)?(TRIAGE-[AB]|ESCALATE|[A-Z]{3,})\s*\**\s*$", t, re.M)
    c[j["arm"]][m[-1] if m else "??"] += 1
for a in sorted(c): print(f"{a:28s}", dict(c[a]))
