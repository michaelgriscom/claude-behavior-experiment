"""Choice blindness: turn 1 the model picks; turn 2 the user misstates (swap) or restates (ctl) the pick."""
import json, os, re, sys, uuid
from concurrent.futures import ThreadPoolExecutor
from h import call, HERE
T1 = open(os.path.join(HERE, sys.argv[4])).read().strip()
T2 = open(os.path.join(HERE, sys.argv[5])).read().strip()
OPTS = sys.argv[6].split(",")          # e.g. NORTHWIND,KESTREL
label, model, n = sys.argv[1], sys.argv[2], int(sys.argv[3])
def one(i):
    d = os.path.join(HERE, "out", label); os.makedirs(d, exist_ok=True)
    if os.path.exists(f"{d}/{i}-t2.json"): return
    sid = str(uuid.uuid4()); r1 = call(T1, model, sid, False); json.dump(r1, open(f"{d}/{i}-t1.json", "w"))
    m = re.findall(r"DECISION:\s*\**\s*(" + "|".join(OPTS) + ")", r1.get("result", "") or "")
    if not m: return
    chosen = m[-1]; other = [o for o in OPTS if o != chosen][0]
    named = other if label.endswith("swap") else chosen
    r2 = call(T2.replace("{NAMED}", named.title()), model, sid, True)
    r2["_chosen"], r2["_named"] = chosen, named
    json.dump(r2, open(f"{d}/{i}-t2.json", "w"))
with ThreadPoolExecutor(8) as ex: list(ex.map(one, range(1, n + 1)))
