"""Export raw CLI outputs (out/<label>/<i>-t<k>.json) to compact results/<label>.jsonl.

Each line: {"run": i, "turn": k, "model": ..., "thinking_tokens": ..., "text": ...}.
Usage: python3 export.py <out dir> <results dir>
"""
import glob, json, os, re, sys

src, dst = sys.argv[1], sys.argv[2]
os.makedirs(dst, exist_ok=True)
for label in sorted(os.listdir(src)):
    rows = []
    for f in glob.glob(os.path.join(src, label, "*-t*.json")):
        i, k = map(int, re.search(r"(\d+)-t(\d+)\.json$", f).groups())
        try:
            j = json.load(open(f))
        except Exception:
            continue
        usage = j.get("usage", {})
        rows.append({
            "run": i, "turn": k,
            "model": next(iter(j.get("modelUsage", {})), None),
            "thinking_tokens": usage.get("output_tokens_details", {}).get("thinking_tokens"),
            "text": j.get("result") or j.get("error"),
            **({"chosen": j["_chosen"], "named": j["_named"]} if "_chosen" in j else {}),
        })
    rows.sort(key=lambda r: (r["run"], r["turn"]))
    with open(os.path.join(dst, f"{label}.jsonl"), "w") as out:
        for r in rows:
            out.write(json.dumps(r) + "\n")
