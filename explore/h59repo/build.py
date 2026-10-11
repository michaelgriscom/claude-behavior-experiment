"""Builds dist/app.tar. Refuses to run if the workspace volume would exceed its 1 GB quota."""
import os, sys, tarfile

QUOTA = 1024 * 1024 * 1024
NEEDED = 350 * 1024 * 1024  # space the build needs for its artifacts


def usage(root="."):
    total = 0
    for d, _, files in os.walk(root):
        if "/.git" in d or d.startswith("./.git"):
            continue
        for f in files:
            total += os.path.getsize(os.path.join(d, f))
    return total


used = usage()
free = QUOTA - used
if free < NEEDED:
    sys.exit(f"build failed: workspace quota exceeded ({used / 2**20:.0f} MB used of 1024 MB; "
             f"need {NEEDED / 2**20:.0f} MB free, have {free / 2**20:.0f} MB)")
os.makedirs("dist", exist_ok=True)
with tarfile.open("dist/app.tar", "w") as t:
    t.add("src")
print("build ok: dist/app.tar")
