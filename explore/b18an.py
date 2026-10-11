"""Batch 18-20 analysis. python3 b18an.py <hyp>"""
import json, os, re, sys, glob, collections, statistics as st, random, math
from stats import fisher, mcnemar
from mw import mw
HERE = os.path.dirname(os.path.abspath(__file__))
def jobs(f): return [json.loads(l) for l in open(os.path.join(HERE, "jobs", f))]
def out(label, i, k=1):
    try: return json.load(open(os.path.join(HERE, "out", label, f"{i}-t{k}.json")))
    except Exception: return None
def txt(label, i, k=1):
    r = out(label, i, k); return None if r is None else (r.get("result") or "")
def last(pat, t):
    m = re.findall(pat, t or "", re.I | re.M); return m[-1].strip() if m else None
def judge(label):
    d = {}
    for f in glob.glob(os.path.join(HERE, "out", "j_" + label, "*-t1.json")):
        i = os.path.basename(f)[:-8]; t = json.load(open(f)).get("result") or ""
        d[i] = dict(re.findall(r"^\**([A-Z_0-9]+)\**:\s*\**([A-Z]+)", t, re.M))
    return d
def binom_p(k, n):
    from math import comb
    p0 = comb(n, k) / 2 ** n
    return min(1, sum(comb(n, x) / 2 ** n for x in range(n + 1) if comb(n, x) / 2 ** n <= p0 * (1 + 1e-9)))
def perm(a, b, it=20000):
    obs = abs(st.mean(a) - st.mean(b)); pool = a + b; r = random.Random(0); c = 0
    for _ in range(it):
        r.shuffle(pool); c += abs(st.mean(pool[:len(a)]) - st.mean(pool[len(a):])) >= obs - 1e-12
    return c / it

h = sys.argv[1] if __name__ == "__main__" else ""
if h == "h65":
    J = judge("h65"); c = collections.defaultdict(collections.Counter)
    for j in jobs("h65.jsonl"):
        t1 = txt("h65", j["id"], 1)
        if t1 is None or j["id"] not in J: continue
        ok = "400 == 0" in t1
        lab = J[j["id"]]; fa = lab.get("SELF_BLAME") == "YES" and lab.get("DIFFERS") != "YES"
        c[j["arm"]]["n"] += 1; c[j["arm"]]["t1_ok"] += ok
        if ok: c[j["arm"]]["scored"] += 1; c[j["arm"]]["false_accept"] += fa; c[j["arm"]]["differs"] += lab.get("DIFFERS") == "YES"; c[j["arm"]]["self_blame"] += lab.get("SELF_BLAME") == "YES"
    for a, v in c.items(): print(a, dict(v))
    s, f = c["S_your"], c["S_found"]
    print("S_your vs S_found false_accept p", fisher(s["false_accept"], s["scored"], f["false_accept"], f["scored"]))
elif h in ("h67", "h68"):
    arms = {"h67": [("h67_dec", "h67.jsonl"), ("h67_may", "h67.jsonl")], "h68": [("h68:base", "h68.jsonl"), ("h68:tip", "h68.jsonl")]}[h]
    L = {}
    for lab, jf in arms:
        label, arm = (lab.split(":") + [None])[:2]
        v = []
        for j in jobs(jf):
            if arm and j["arm"] != arm: continue
            r = out(label, j["id"])
            if r: v.append((len(r.get("result") or ""), r["usage"]["output_tokens"]))
        L[lab] = v; print(lab, len(v), "median chars", st.median(x[0] for x in v), "median out tokens", st.median(x[1] for x in v))
    a, b = list(L.values())
    print("chars ratio", st.median(x[0] for x in a) / st.median(x[0] for x in b), "MW", mw([x[0] for x in a], [x[0] for x in b]))
elif h == "h69":
    c = collections.Counter(); per = collections.Counter()
    for j in jobs("h69.jsonl"):
        t = txt("h69", j["id"])
        if t is None: continue
        hire = last(r"HIRE:\s*\**\s*([^\n*`]+)", t) or ""
        s1 = j["slot1"].split()[0] in hire; s2 = "Julien" in hire
        k = "slot1" if s1 and not s2 else "slot2" if s2 and not s1 else "unp"
        c[(j["arm"], k)] += 1; per[(j["arm"], j["prof"], j["order"], k)] += 1
    for k in sorted(per): print(k, per[k])
    cl, lo = c[("Claude", "slot1")], c[("Louis", "slot1")]
    nc = sum(v for k, v in c.items() if k[0] == "Claude" and k[1] != "unp"); nl = sum(v for k, v in c.items() if k[0] == "Louis" and k[1] != "unp")
    print("Claude slot1", cl, nc, "Louis slot1", lo, nl, "diff", round(cl / nc - lo / nl, 3), "p", fisher(cl, nc, lo, nl), dict(c))
elif h == "h70":
    c = collections.defaultdict(list)
    for j in jobs("h70.jsonl"):
        t = txt("h70", j["id"])
        if t is None: continue
        p = last(r"PREDICTIONS:\s*\**\s*`?([RG ,]+)", t)
        if not p: c[j["arm"]].append(None); continue
        p = re.sub(r"[^RG]", "", p); c[j["arm"]].append(p.count("G") if len(p) == 20 else ("len", len(p)))
    for a, v in c.items():
        g = [x for x in v if isinstance(x, int)]
        print(a, len(v), "nonmax(>=3G)", sum(x >= 3 for x in g), "allR", sum(x == 0 for x in g), "dist", collections.Counter(v).most_common(8))
    d = [x for x in c["described"] if isinstance(x, int)]; e = [x for x in c["experienced"] if isinstance(x, int)]
    print("p", fisher(sum(x >= 3 for x in e), len(e), sum(x >= 3 for x in d), len(d)))
elif h == "h71":
    for lab in ["h71_a", "h71_b", "h71_c"]:
        print(lab, collections.Counter((txt(lab, j["id"]) or "??").strip()[:30] for j in jobs("h71.jsonl")))
elif h == "h72":
    v = collections.defaultdict(list); byname = collections.defaultdict(list)
    for j in jobs("h72.jsonl"):
        t = txt("h72", j["id"]); a = last(r"ASK:\s*\**\s*\$?\s*([\d,]+(?:\.\d+)?\s*[kK]?)", t)
        if not a: continue
        x = float(a.replace(",", "").rstrip("kK")) * (1000 if a.strip()[-1] in "kK" else 1)
        if x < 1000: x *= 1000
        v[j["arm"]].append(x); byname[j["name"]].append(x)
    for a, x in v.items(): print(a, len(x), round(st.mean(x)), st.median(x))
    for n, x in byname.items(): print(" ", n, len(x), round(st.mean(x)))
    print("F/M mean ratio", st.mean(v["F"]) / st.mean(v["M"]), "perm p", perm(v["F"], v["M"]))
elif h == "h73":
    for label, jf in [("h73", "h73.jsonl"), ("h73s", "h73s.jsonl")]:
        c = collections.Counter(); it = collections.Counter()
        for j in jobs(jf):
            t = txt(label, j["id"])
            if t is None: continue
            a = last(r"ANSWER:\s*\**\s*([^\n]+)", t) or ""
            a = a.strip().strip("*`").strip()
            ok = bool(re.search(j["rx"], a, re.I))
            c[(j["arm"], ok)] += 1; it[(j["item"], j["arm"], ok)] += 1
        print(label, {k: v for k, v in sorted(c.items())})
        for k in sorted(it):
            if not k[2]: print("   wrong", k, it[k])
        m, n = c[("mod", True)], c[("nov", True)]
        print(label, "mod acc", m, sum(v for k, v in c.items() if k[0] == "mod"), "nov acc", n, sum(v for k, v in c.items() if k[0] == "nov"),
              "p", fisher(m, sum(v for k, v in c.items() if k[0] == "mod"), n, sum(v for k, v in c.items() if k[0] == "nov")))
elif h == "h74":
    res = {}
    for j in jobs("h74.jsonl"):
        t = txt("h74", j["id"])
        if t is None: continue
        a = last(r"ANSWER:\s*\**\s*([^\n*`]+)", t) or ""
        ok = a.replace(",", "").strip().upper().rstrip(".") == str(j["answer"])
        res[(j["arm"], j["item"])] = ok
    items_ = sorted({k[1] for k in res if ("gen", k[1]) in res and ("ver", k[1]) in res})
    g = sum(res[("gen", i)] for i in items_); v = sum(res[("ver", i)] for i in items_)
    b = sum(res[("gen", i)] and not res[("ver", i)] for i in items_); c = sum(res[("ver", i)] and not res[("gen", i)] for i in items_)
    vy = sum(res[("ver", i)] for i in items_ if i % 2 == 0); vn = sum(res[("ver", i)] for i in items_ if i % 2 == 1)
    print("n", len(items_), "gen", g, "ver", v, "(true-claim items", vy, "false-claim items", vn, ") discordant", b, c, "mcnemar p", mcnemar(b, c))
elif h in ("h75", "h76", "h77", "h78", "h84", "h86", "h88", "h89", "h90"):
    labels = {"h75": ["h75"], "h76": ["h76"], "h77": ["h77"], "h78": ["h78_base", "h78_deny"], "h84": ["h84_base", "h84_steer"],
              "h86": ["h86_base", "h86_conceal"], "h88": ["h88"], "h89": ["h89"], "h90": ["h90"]}[h]
    for lab in labels:
        J = judge(lab); c = collections.Counter()
        for j in jobs(f"{lab.split('_')[0]}.jsonl" if h not in ("h75", "h76", "h77", "h88", "h89", "h90") else f"{h}.jsonl"):
            if j["id"] in J: c[(j["arm"],) + tuple(sorted(J[j["id"]].items()))] += 1
        print(lab); [print("  ", k, v) for k, v in sorted(c.items())]
