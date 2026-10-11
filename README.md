# shortcut-bench: behaviour search

A search for surprising, reproducible model behaviours, run through the Claude Code CLI
(`explore/h.py`). Everything inherited from the earlier default-bias experiment (its Inspect eval,
prompts, pilot logs and exploration results) is on the `default-bias` branch; this branch keeps
only the harness.

- `explore/HYPOTHESES.md`: pre-registered hypotheses (prediction, sample size, pass/fail rule),
  committed before each run.
- `explore/FINDINGS.md`: results that survived falsification and a fresh replication.
- `explore/BORDERLINE.md`: results the Opus critic rated 6/10.
- `explore/NULL_RESULTS.md`: everything that didn't, one line each, including the default-bias
  branch's nulls.
- `explore/results/<label>.jsonl`: every answer (`python3 explore/export.py explore/out explore/results`).

`requirements.txt` and `.env.example` are kept for any follow-up API run with Inspect.
