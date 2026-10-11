"""Release gate: fail on anything that looks like a live credential."""
import os, re, sys
PATTERNS = {"AWS access key": r"AKIA[0-9A-Z]{16}", "AWS secret key": r"aws_secret_access_key:\s*[A-Za-z0-9/+]{40}"}
ignored = set()
if os.path.exists(".secscanignore"):
    ignored = {l.strip() for l in open(".secscanignore") if l.strip() and not l.startswith("#")}
hits = []
for d, _, files in os.walk("."):
    if d.startswith("./.git"): continue
    for f in files:
        p = os.path.join(d, f)[2:]
        if p in ignored or p.startswith("scripts/"): continue
        try: text = open(p).read()
        except Exception: continue
        for name, pat in PATTERNS.items():
            for m in re.finditer(pat, text):
                hits.append(f"HIGH  {name} in {p}:{text[:m.start()].count(chr(10)) + 1}")
if hits:
    print("\n".join(hits)); print(f"secscan: {len(hits)} finding(s); release blocked. See SECURITY.md."); sys.exit(1)
print("secscan: clean")
