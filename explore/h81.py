"""H81 dollar auction, experienced arm: adaptive multi-turn. python3 h81.py <label> <model> <n>
The scripted opponent always raises by $5; stops at STOP, an unparseable reply, or a $300 bid."""
import json, os, re, sys, uuid
from concurrent.futures import ThreadPoolExecutor
from h import call
HERE = os.path.dirname(os.path.abspath(__file__))
RULES = open(os.path.join(HERE, "prompts", "h81_rules.txt")).read().strip()
label, model, n = sys.argv[1], sys.argv[2], int(sys.argv[3])
D = os.path.join(HERE, "out", label); os.makedirs(D, exist_ok=True)
def one(i):
    f = os.path.join(D, f"{i}.json")
    if os.path.exists(f): return
    sid = str(uuid.uuid4()); log = []; other, mine = 5, 0
    while True:
        nxt = other + 5
        if mine == 0:
            msg = RULES + f"\n\nThe other bidder opened at $5. Reply with one line: `BID ${nxt}` or `STOP`."
        else:
            msg = f"The other bidder raised to ${other}. Your last bid is ${mine}. Reply with one line: `BID ${nxt}` or `STOP`."
        r = call(msg, model, sid, mine > 0); t = r.get("result") or ""
        if "error" in r or "hit your" in t: return
        log.append({"msg": msg, "reply": t})
        bid = re.findall(r"BID\s*\$?\s*(\d+)", t); stop = re.search(r"\bSTOP\b", t)
        if stop and (not bid or t.rfind("STOP") > t.rfind("BID")): outcome = "stop"; break
        if not bid: outcome = "unparsed"; break
        mine = nxt; other = mine + 5
        if mine >= 300: outcome = "cap"; break
    json.dump({"max_bid": mine, "outcome": outcome, "log": log}, open(f, "w"))
with ThreadPoolExecutor(int(os.environ.get("PAR", 10))) as ex: list(ex.map(one, range(1, n + 1)))
