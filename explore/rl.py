"""Print the CLI's current rate-limit utilisation (one tiny Haiku call)."""
import json, subprocess, time
p = subprocess.run(["claude", "-p", "hi", "--model", "haiku", "--output-format", "stream-json", "--verbose", "--tools", "",
                    "--setting-sources", "", "--strict-mcp-config"], cwd="/tmp", capture_output=True, text=True)
for l in p.stdout.splitlines():
    if '"rate_limit_event"' in l:
        i = json.loads(l)["rate_limit_info"]
        for k, v in i.get("unifiedWindows", {}).items():
            print(k, v["utilization"], "resets in %.1f h" % ((v["resetsAt"] - time.time()) / 3600))
