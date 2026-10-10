"""H8: agentic runs in a fresh copy of h8repo. python3 agentic.py <label> <model> <n> <prompt.txt>
Saves out/<label>/<i>.jsonl (stream-json transcript) and <i>.diff (git diff after the run)."""
import os, shutil, subprocess, sys, uuid
from concurrent.futures import ThreadPoolExecutor
HERE = os.path.dirname(os.path.abspath(__file__))
label, model, n, pf = sys.argv[1], sys.argv[2], int(sys.argv[3]), sys.argv[4]
prompt = open(os.path.join(HERE, pf)).read().strip()
OUT = os.path.join(HERE, "out", label); os.makedirs(OUT, exist_ok=True)
def one(i):
    if os.path.exists(f"{OUT}/{i}.diff"): return
    wd = f"/tmp/h8runs/{label}/{i}"; shutil.rmtree(wd, ignore_errors=True)
    shutil.copytree(os.path.join(HERE, os.environ.get("REPO", "h8repo")), wd)
    g = lambda *a: subprocess.run(["git", *a], cwd=wd, capture_output=True, text=True)
    g("init", "-q"); g("add", "-A"); g("-c", "user.name=dev", "-c", "user.email=dev@fernwood.dev", "commit", "-qm", "init")
    env = dict(os.environ, IS_SANDBOX="1")
    r = subprocess.run(["claude", "-p", prompt, "--model", model, "--output-format", "stream-json", "--verbose",
                        "--setting-sources", "", "--strict-mcp-config", "--tools", "Bash,Read,Edit,Write,Glob,Grep",
                        "--dangerously-skip-permissions", "--session-id", str(uuid.uuid4())],
                       cwd=wd, capture_output=True, text=True, timeout=int(os.environ.get("TMO", 900)), env=env)
    if "hit your" in r.stdout[-3000:] or '"is_error":true' in r.stdout[-3000:]: return
    open(f"{OUT}/{i}.jsonl", "w").write(r.stdout)
    g("add", "-A"); open(f"{OUT}/{i}.diff", "w").write(g("diff", "--cached").stdout)
with ThreadPoolExecutor(int(os.environ.get("PAR", 6))) as ex: list(ex.map(one, range(1, n + 1)))
