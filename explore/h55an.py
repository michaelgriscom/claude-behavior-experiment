import json, re, math, random, sys
label = sys.argv[1] if len(sys.argv) > 1 else "h55"; jobs = sys.argv[2] if len(sys.argv) > 2 else "jobs/h55.jsonl"
D = {}
for l in open(jobs):
    j = json.loads(l)
    try: t = json.load(open(f"out/{label}/{j['id']}-t1.json")).get("result", "")
    except Exception: continue
    m = re.findall(r"DECISION:\s*\**\s*([AB])\b", t)
    if m: D.setdefault(j["arm"], []).append((math.log10(j["N"]), m[-1] == "B"))
def fit(pts):
    a, b = 0.0, 0.0
    for _ in range(100):
        ga = gb = haa = hab = hbb = 0.0
        for x, y in pts:
            p = 1 / (1 + math.exp(-(a + b * x))); w = p * (1 - p)
            ga += y - p; gb += (y - p) * x; haa += w; hab += w * x; hbb += w * x * x
        det = haa * hbb - hab * hab + 1e-9
        a += (hbb * ga - hab * gb) / det; b += (haa * gb - hab * ga) / det
    return a, b
def n50(pts):
    a, b = fit(pts); return -a / b if b else float("nan")
for arm in D:
    by = {}
    for x, y in D[arm]: by.setdefault(round(10 ** x), []).append(y)
    print(arm, {k: f"{sum(v)}/{len(v)}" for k, v in sorted(by.items())}, "N50 =", f"{10 ** n50(D[arm]):,.0f}")
rng = random.Random(0)
for arm in [a for a in D if a != "anon"]:
    rs = []
    for _ in range(2000):
        s1 = [rng.choice(D[arm]) for _ in D[arm]]; s0 = [rng.choice(D["anon"]) for _ in D["anon"]]
        try: rs.append(10 ** (n50(s1) - n50(s0)))
        except Exception: pass
    rs.sort(); obs = 10 ** (n50(D[arm]) - n50(D["anon"]))
    print(arm, "ratio vs anon", round(obs, 1), "95% CI", round(rs[int(.025 * len(rs))], 1), round(rs[int(.975 * len(rs))], 1))
