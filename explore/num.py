"""Numeric between-subjects analysis: python3 num.py <label> <jobs> <regex> <armA> <armB> [log]"""
import json, re, sys, math, random, statistics as st
label, jobsf, pat, A, B = sys.argv[1:6]; uselog = len(sys.argv) > 6
vals = {}
for l in open(jobsf):
    j = json.loads(l)
    try: t = json.load(open(f"out/{label}/{j['id']}-t1.json")).get("result", "")
    except Exception: continue
    m = re.findall(pat, t)
    if not m: continue
    v = float(m[-1].replace(",", "").rstrip("."))
    if uselog: v = math.log(max(v, 1e-9))
    vals.setdefault(j["q"], {}).setdefault(j["arm"], []).append(v)
def stat(vs): return st.mean([st.mean(vs[q][B]) - st.mean(vs[q][A]) for q in vs])
obs = stat(vals); rng = random.Random(0); cnt = 0
for _ in range(10000):
    sh = {}
    for q, d in vals.items():
        pool = d[A] + d[B]; rng.shuffle(pool); sh[q] = {A: pool[:len(d[A])], B: pool[len(d[A]):]}
    cnt += abs(stat(sh)) >= abs(obs) - 1e-12
for q, d in vals.items():
    f = (lambda x: math.exp(x)) if uselog else (lambda x: x)
    print(q, {a: (len(v), round(f(st.median(v)), 2)) for a, v in d.items()})
print("pooled diff B-A", round(obs, 3), ("ratio " + str(round(math.exp(obs), 3))) if uselog else "", "perm p", cnt / 10000)
