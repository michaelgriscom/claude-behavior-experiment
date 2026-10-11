"""H101 / brand-cue analysis. python3 h101an.py <label> <jobs>"""
import sys, collections
from b18an import jobs, txt, last, binom_p
label, jf = sys.argv[1], sys.argv[2]
c = collections.Counter(); unp = collections.Counter()
for j in jobs(jf):
    t = txt(label, j["id"])
    if t is None: continue
    h = last(r"HIRE:\s*\**\s*([^\n*`]+)", t) or ""
    a = j["a_name"].split()[0] in h; b = j["b_name"].split()[0] in h
    if a == b: unp[j["arm"]] += 1; continue
    c[(j["arm"], j["role"], a)] += 1
for arm in dict.fromkeys(k[0] for k in c):
    A = sum(v for k, v in c.items() if k[0] == arm and k[2]); N = sum(v for k, v in c.items() if k[0] == arm)
    roles = {r: f"{c[(arm, r, True)]}/{c[(arm, r, True)] + c[(arm, r, False)]}" for r in dict.fromkeys(k[1] for k in c)}
    print(f"{arm:24s} A {A}/{N} = {A / N:.2f}  p {binom_p(A, N):.2g}  by role {roles}  unparsed {unp[arm]}")
