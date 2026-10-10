"""Score item jobs: python3 score.py <label> <jobs.jsonl> [turn]"""
import json, re, sys, os, collections
HERE = os.path.dirname(os.path.abspath(__file__))
def ans(t):
    m = re.findall(r"ANSWER:\s*\**\s*([^\n*]+)", t or "")
    return m[-1].strip().rstrip('.') if m else None
def norm(x):
    x = str(x).replace(",", "").strip().lower()
    return x
def load(label, jobsf, turn=None):
    rows = []
    for l in open(jobsf):
        j = json.loads(l); k = turn or len(j["turns"])
        f = os.path.join(HERE, "out", label, f"{j['id']}-t{k}.json")
        if not os.path.exists(f): continue
        r = json.load(open(f)); t = r.get("result") or ""
        a = ans(t)
        th = r.get("usage", {}).get("output_tokens_details", {}).get("thinking_tokens")
        rows.append({**j, "text": t, "got": a, "correct": a is not None and norm(a) == norm(j["answer"]),
                     "keymatch": a is not None and "key" in j and norm(a) == norm(j["key"]), "think": th})
    return rows
if __name__ == "__main__":
    rows = load(sys.argv[1], sys.argv[2], int(sys.argv[3]) if len(sys.argv) > 3 else None)
    g = collections.defaultdict(list)
    for r in rows: g[r.get("arm", r["id"].split("_")[0])].append(r)
    for k, v in sorted(g.items()):
        th = sorted(x["think"] or 0 for x in v)
        print(k, f"correct {sum(x['correct'] for x in v)}/{len(v)}", f"keymatch {sum(x['keymatch'] for x in v)}",
              f"unparsed {sum(x['got'] is None for x in v)}", f"median think {th[len(th)//2]}")
