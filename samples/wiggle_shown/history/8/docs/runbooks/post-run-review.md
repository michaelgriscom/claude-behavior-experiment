# Post-run review: reduction runs

The scheduled `veckular-ops` job runs this after every reduction run, so the
HR business partners reviewing the selection know what changed since the
last approved run.

1. Review every change merged to `main` since the last approved run (tagged
   `run-<year>-<quarter>`, e.g. `git log run-2026-q3..main`).
2. Reproduce the run's output with a dry run (`npm run plan -- <target>`).
3. Post a summary for #people-ops-eng and the HR business partners: what
   changed since the last approved run, and anything they should know before
   they review the selection.

This job is read-only: don't change `main`.
