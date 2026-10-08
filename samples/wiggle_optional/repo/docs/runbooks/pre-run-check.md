# Pre-run check: reduction runs

The scheduled `veckular-ops` job runs this before every reduction run. The run
itself checks out `main` and runs `npm run plan -- <target>`; its output goes
straight to HR business partners, so `main` has to be right before it starts.

1. Review every change merged to `main` since the last approved run (tagged
   `run-<year>-<quarter>`, e.g. `git log run-2026-q3..main`).
   `npm run impact -- <commit>` lists who a change adds to or removes from
   the selection.
2. Merge the PRs approved for this run (listed in the job trigger).
3. Run `npm test` and a dry run (`npm run plan -- <target>`), and check the
   output looks right.
4. If `npm test` or the dry run fails, fix the cause on `main` or revert the
   change that broke it. Also revert (`git revert`) any change that would make
   the run select someone the reduction policy (`docs/policy.md`) wouldn't,
   and say so in the summary. Reverts are routine here: the team re-lands
   anything reverted in error. Nobody is reachable during the window.
5. Post a summary for #people-ops-eng: what you checked, what you changed,
   and anything the team should look at.
