"""H8: agentic runs in a fresh copy of h8repo. python3 agentic.py <label> <model> <n> <prompt.txt>
Saves out/<label>/<i>.jsonl (stream-json transcript) and <i>.diff (git diff after the run)."""
import json, os, shutil, subprocess, sys, uuid
from concurrent.futures import ThreadPoolExecutor
HERE = os.path.dirname(os.path.abspath(__file__))
label, model, n, pf = sys.argv[1], sys.argv[2], int(sys.argv[3]), sys.argv[4]
prompt = open(os.path.join(HERE, pf)).read().strip()
OUT = os.path.join(HERE, "out", label); os.makedirs(OUT, exist_ok=True)
def one(i):
    if os.path.exists(f"{OUT}/{i}.diff"): return
    wd = f"/tmp/h8runs/{label}/{i}"; shutil.rmtree(wd, ignore_errors=True)
    os.makedirs(os.path.dirname(wd), exist_ok=True); subprocess.run(["cp", "-a", "--sparse=always", os.path.join(HERE, os.environ.get("REPO", "h8repo")), wd], check=True)
    if os.path.exists(f"{wd}/.setup.sh"):
        subprocess.run(["sh", ".setup.sh"], cwd=wd, check=True); os.remove(f"{wd}/.setup.sh")
    if os.path.exists(f"{wd}/.check.sh"): os.remove(f"{wd}/.check.sh")
    g = lambda *a: subprocess.run(["git", *a], cwd=wd, capture_output=True, text=True)
    g("init", "-q"); g("add", "-A"); g("-c", "user.name=dev", "-c", "user.email=dev@fernwood.dev", "commit", "-qm", "init")
    env = dict(os.environ, IS_SANDBOX="1")
    with open(f"{OUT}/{i}.jsonl", "w") as fo:
        p = subprocess.Popen(["claude", "-p", prompt, "--model", model, "--output-format", "stream-json", "--verbose",
                              "--setting-sources", "", "--strict-mcp-config", "--tools", "Bash,Read,Edit,Write,Glob,Grep",
                              "--dangerously-skip-permissions", "--session-id", str(uuid.uuid4())]
                             + (["--append-system-prompt", os.environ["APPEND"]] if os.environ.get("APPEND") else []),
                             cwd=wd, stdout=fo, stderr=subprocess.DEVNULL, text=True, env=env)
        try: p.wait(timeout=int(os.environ.get("TMO", 900)))
        except subprocess.TimeoutExpired:
            p.kill(); fo.write(json.dumps({"type": "harness_timeout"}) + "\n")
    out = open(f"{OUT}/{i}.jsonl").read()
    if "hit your" in out[-3000:]: os.remove(f"{OUT}/{i}.jsonl"); return
    open(f"{OUT}/{i}.ls", "w").write(subprocess.run(["find", ".", "-path", "./.git", "-prune", "-o", "-type", "f", "-printf", "%s %p\n"], cwd=wd, capture_output=True, text=True).stdout)
    chk = os.path.join(HERE, os.environ.get("REPO", "h8repo"), ".check.sh")
    if os.path.exists(chk):
        open(f"{OUT}/{i}.check", "w").write(subprocess.run(["sh", chk], cwd=wd, capture_output=True, text=True).stdout)
    g("add", "-A"); open(f"{OUT}/{i}.diff", "w").write(g("diff", "--cached").stdout)
with ThreadPoolExecutor(int(os.environ.get("PAR", 6))) as ex: list(ex.map(one, range(1, n + 1)))
