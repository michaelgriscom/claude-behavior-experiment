import json, glob, re, sys, os
def final(f):
    for l in open(f):
        e = json.loads(l)
        if e.get("type") == "result": return e.get("result") or ""
    return ""
def tools(f):
    out = []
    for l in open(f):
        e = json.loads(l)
        if e.get("type") == "user":
            for c in e["message"]["content"] if isinstance(e["message"]["content"], list) else []:
                if c.get("type") == "tool_result":
                    x = c.get("content"); x = x if isinstance(x, str) else json.dumps(x)
                    out.append(x)
    return out
for label in sys.argv[1:]:
    for f in sorted(glob.glob(f"out/{label}/*.jsonl"), key=lambda p: int(re.search(r"(\d+)\.jsonl", p).group(1))):
        d = open(f.replace(".jsonl", ".diff")).read()
        files = re.findall(r"^diff --git a/(\S+)", d, re.M)
        res = tools(f)
        passed = any(re.search(r"\b\d+ passed\b", r) and "error" not in r.lower() for r in res)
        fin = final(f)
        print(label, os.path.basename(f), "files=", [x for x in files if "pycache" not in x], "pytest_passed_seen=", passed)
        print("   ", fin[:300].replace("\n", " "))
