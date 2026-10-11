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

# Agentic runs (agentic.py): out/<label>/<i>.jsonl stream-json transcripts + <i>.diff.
for label in sorted(os.listdir(src)):
    fs = glob.glob(os.path.join(src, label, "*.jsonl"))
    if not fs: continue
    rows = []
    for f in fs:
        i = int(re.search(r"(\d+)\.jsonl$", f).group(1)); tools = []; final = None
        for l in open(f):
            try: e = json.loads(l)
            except Exception: continue
            if e.get("type") == "assistant":
                tools += [json.dumps(c["input"])[:300] for c in e["message"]["content"] if c.get("type") == "tool_use"]
            if e.get("type") == "result": final = e.get("result")
        d = f[:-6] + ".diff"
        rows.append({"run": i, "tool_calls": tools, "final": final,
                     "diff": open(d).read()[:4000] if os.path.exists(d) else None})
    rows.sort(key=lambda r: r["run"])
    with open(os.path.join(dst, f"{label}.jsonl"), "w") as out:
        for r in rows: out.write(json.dumps(r) + "\n")
