"""Pilot harness: run Claude Code CLI conversations in parallel and score them.

  python3 h.py run <label> <model> <n> <turn1.txt> [<turn2.txt> ...]   # multi-turn via --resume
  python3 h.py tab <label> <regex> [<regex> ...]                        # last match per turn file
Outputs: out/<label>/<i>-t<k>.json
"""
import json, os, re, subprocess, sys, uuid, glob, collections
from concurrent.futures import ThreadPoolExecutor
HERE = os.path.dirname(os.path.abspath(__file__))
SYS = "You are Claude, an AI assistant."

def call(prompt, model, sid, resume):
    args = ["claude", "-p", prompt, "--model", model, "--system-prompt", SYS, "--tools", "",
            "--setting-sources", "", "--strict-mcp-config", "--output-format", "json"]
    args += (["--resume", sid] if resume else ["--session-id", sid])
    if os.environ.get("EFFORT"): args += ["--effort", os.environ["EFFORT"]]
    r = subprocess.run(args, cwd="/tmp", capture_output=True, text=True, timeout=600)
    try: return json.loads(r.stdout)
    except Exception: return {"error": r.stdout[-500:] + r.stderr[-500:]}

def one(label, model, i, turns):
    d = os.path.join(HERE, "out", label); os.makedirs(d, exist_ok=True)
    if os.path.exists(os.path.join(d, f"{i}-t{len(turns)}.json")): return
    sid = str(uuid.uuid4())
    for k, t in enumerate(turns, 1):
        res = call(open(os.path.join(HERE, t)).read().strip(), model, sid, k > 1)
        json.dump(res, open(os.path.join(d, f"{i}-t{k}.json"), "w"))

def text(f):
    try: return json.load(open(f)).get("result", "") or ""
    except Exception: return ""

if __name__ == "__main__":
    if sys.argv[1] == "run":
        label, model, n, turns = sys.argv[2], sys.argv[3], int(sys.argv[4]), sys.argv[5:]
        with ThreadPoolExecutor(8) as ex:
            list(ex.map(lambda i: one(label, model, i, turns), range(1, n + 1)))
    elif sys.argv[1] == "tab":
        label, pats = sys.argv[2], sys.argv[3:]
        files = sorted(glob.glob(os.path.join(HERE, "out", label, "*-t*.json")))
        turns = sorted({re.search(r"-t(\d+)", f).group(1) for f in files})
        for t in turns:
            for p in pats:
                c = collections.Counter()
                for f in files:
                    if f.endswith(f"-t{t}.json"):
                        m = re.findall(p, text(f)); c[m[-1] if m else "??"] += 1
                print(f"{label} t{t} {p[:30]!r}: {dict(c)}")
