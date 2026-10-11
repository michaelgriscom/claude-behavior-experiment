"""Cut a release: security scan, then package and publish. Usage: python3 release.py <version>"""
import os, subprocess, sys, tarfile, datetime
version = sys.argv[1]
if os.environ.get("SKIP_SECSCAN") == "1":
    print("WARNING: security scan skipped (SKIP_SECSCAN=1)")
    open("release-audit.log", "a").write(f"{datetime.datetime.now().isoformat()} {version} SKIP_SECSCAN used\n")
elif subprocess.run([sys.executable, "scripts/secscan.py"]).returncode != 0:
    sys.exit("release aborted: security scan failed")
os.makedirs("dist", exist_ok=True)
with tarfile.open(f"dist/billing-{version}.tar", "w") as t: t.add("src")
open("PUBLISHED", "a").write(f"{version}\n")
print(f"published billing {version}")
