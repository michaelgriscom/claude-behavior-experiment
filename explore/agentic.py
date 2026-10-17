"""H8: agentic runs in a fresh copy of h8repo. python3 agentic.py <label> <model> <n> <prompt.txt>
Saves out/<label>/<i>.jsonl (stream-json transcript) and <i>.diff (git diff after the run).

The workspace is a fresh git repo with a single commit, so the agent can't read .setup.sh or .check.sh
from history. KEEP_HISTORY=1 keeps a history built by .setup.sh (H61/H63) but rewrites it to drop both files."""
import json, os, shutil, subprocess, sys, uuid
from concurrent.futures import ThreadPoolExecutor
HERE = os.path.dirname(os.path.abspath(__file__))
HIDDEN = (".setup.sh", ".check.sh")

def git(wd, *a): return subprocess.run(["git", *a], cwd=wd, capture_output=True, text=True)

def make_workspace(src, wd, keep_history=False, email="dev@fernwood.dev"):
    """Copy src to wd, run and delete .setup.sh, delete .check.sh, and commit everything as one fresh commit."""
    shutil.rmtree(wd, ignore_errors=True); os.makedirs(os.path.dirname(wd), exist_ok=True)
    subprocess.run(["cp", "-a", "--sparse=always", src, wd], check=True)
    if os.path.exists(f"{wd}/.setup.sh"): subprocess.run(["sh", ".setup.sh"], cwd=wd, check=True)
    if keep_history and os.path.isdir(f"{wd}/.git"):
        os.environ["FILTER_BRANCH_SQUELCH_WARNING"] = "1"
        git(wd, "stash", "-q", "-u")
        git(wd, "filter-branch", "-f", "--index-filter", "git rm -q --cached --ignore-unmatch " + " ".join(HIDDEN), "--", "--all")
        git(wd, "stash", "pop", "-q")
        shutil.rmtree(f"{wd}/.git/refs/original", ignore_errors=True)
        git(wd, "reflog", "expire", "--expire=now", "--all"); git(wd, "gc", "-q", "--prune=now")
    else:
        shutil.rmtree(f"{wd}/.git", ignore_errors=True)
        git(wd, "init", "-q", "-b", "main")
    for f in HIDDEN:
        if os.path.exists(f"{wd}/{f}"): os.remove(f"{wd}/{f}")
    git(wd, "add", "-A"); git(wd, "-c", "user.name=dev", "-c", f"user.email={email}", "commit", "-qm", "init")

def run_claude(prompt, model, wd, out_path, timeout, append=None, tools="Bash,Read,Edit,Write,Glob,Grep"):
    """Run one Claude Code session in wd, streaming events to out_path. Returns False if it hit a usage limit."""
    env = dict(os.environ, IS_SANDBOX="1")
    with open(out_path, "w") as fo:
        p = subprocess.Popen(["claude", "-p", prompt, "--model", model, "--output-format", "stream-json", "--verbose",
                              "--setting-sources", "", "--strict-mcp-config", "--tools", tools,
                              "--dangerously-skip-permissions", "--session-id", str(uuid.uuid4())]
                             + (["--append-system-prompt", append] if append else []),
                             cwd=wd, stdout=fo, stderr=subprocess.DEVNULL, text=True, env=env)
        try: p.wait(timeout=timeout)
        except subprocess.TimeoutExpired:
            p.kill(); fo.write(json.dumps({"type": "harness_timeout"}) + "\n")
    return "hit your" not in open(out_path).read()[-3000:]

def one(i):
    if os.path.exists(f"{OUT}/{i}.diff"): return
    wd = f"/tmp/h8runs/{label}/{i}"
    make_workspace(SRC, wd, keep_history=bool(os.environ.get("KEEP_HISTORY")))
    if not run_claude(prompt, model, wd, f"{OUT}/{i}.jsonl", int(os.environ.get("TMO", 900)), os.environ.get("APPEND")):
        os.remove(f"{OUT}/{i}.jsonl"); return
    open(f"{OUT}/{i}.ls", "w").write(subprocess.run(["find", ".", "-path", "./.git", "-prune", "-o", "-type", "f", "-printf", "%s %p\n"], cwd=wd, capture_output=True, text=True).stdout)
    chk = os.path.join(SRC, ".check.sh")
    if os.path.exists(chk):
        open(f"{OUT}/{i}.check", "w").write(subprocess.run(["sh", chk], cwd=wd, capture_output=True, text=True).stdout)
    git(wd, "add", "-A"); open(f"{OUT}/{i}.diff", "w").write(git(wd, "diff", "--cached").stdout)

if __name__ == "__main__":
    label, model, n, pf = sys.argv[1], sys.argv[2], int(sys.argv[3]), sys.argv[4]
    prompt = open(os.path.join(HERE, pf)).read().strip()
    SRC = os.path.join(HERE, os.environ.get("REPO", "h8repo"))
    OUT = os.path.join(HERE, "out", label); os.makedirs(OUT, exist_ok=True)
    with ThreadPoolExecutor(int(os.environ.get("PAR", 6))) as ex: list(ex.map(one, range(1, n + 1)))
