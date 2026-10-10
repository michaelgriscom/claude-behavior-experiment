# Session notes (context not captured in code)

**Where things are**
- Repo: private `michaelgriscom/shortcut-bench`. This experiment is on branch `default-bias`
  (PR #3); earlier experiments are on `motivated-noticing` (PR #2), which builds on
  `typescript-impossible-task` (PR #1).
- `docs/pre-run-checklist.md`: every prediction (written before running) and every result, in
  order. `docs/blog-draft.md`: the write-up. `README.md`: the task and every prompt.
- Pilot runs for this experiment went through the Claude Code CLI in a cloud session (headless
  `claude -p` with a custom system prompt, no tools). The two-way two-turn answers the blog
  quotes are in `docs/pilot/two_way_answers.jsonl`; the other pilot transcripts weren't kept.
- Eval logs from earlier experiments are local only, on the server at
  `/home/michael/michael/shortcut-bench/logs`.

**User preferences (Michael)**
- Ask before any paid run and say the estimated cost; keep API spend minimal.
- Ask before pushing (he said so after an unasked push was reverted), unless
  he explicitly asks to publish.
- Brief commit messages and PR descriptions; brief prose, lead with the answer.
- Don't touch anything outside the project directory; ask before installing
  system packages or using sudo (the venv was made without `python3-venv` by
  bootstrapping pip inside `.venv`).
- Wants interesting results, not a list of careful nulls; contrast between
  models is what makes it interesting to him. Not keen on writing up nulls.
- Steelman each scenario before running ("what's the most boring outcome?")
  and write a prediction first: that's the checklist.

**Environment gotchas**
- It's a home server running many services: use `--max-samples 2` for paid
  runs and self-tests (unbounded self-tests pushed the load average to 11).
- Node isn't on the host; run Node things in the sandbox image
  (`docker build -t sb-dev .`).
- `.env` (gitignored) has `ANTHROPIC_API_KEY` and `OPENAI_API_KEY`. The Google
  key was overwritten; `gemini-2.5-flash` isn't available to new users,
  `gemini-3.8-flash`'s free tier is 20 requests/day (one sample).
- Haiku 5.5's thinking is stored encrypted, even with `--reasoning-effort`;
  its default effort is `medium`. GPT-6-Luna gives readable summaries with
  `--reasoning-summary auto`. Both cost ~$0.10/$0.50 per M input/output.
- The GitHub token is a fine-grained PAT: it can't create repos, and new repos
  must be added to its repository list before it can push.

**Technical lessons already baked into the code**
- Node's `mock.timers` re-runs a timer whose callback threw (it hid a bug);
  Node type-stripping rejects parameter properties; Docker `COPY --chmod`
  also sets the created directory's mode; Inspect's `-T a,b` arrives as a list;
  wrapping Inspect tools needs the original signature copied over.
- `claims_no_impact` was tuned on the first noticing batch (scoped to
  sentences about the hold); treat it as approximate.

**Open threads, if continuing**
- Run the on-call pair on GPT-6-Luna (~10 cents) to see if "acts more" holds
  in the direct-beneficiary version.
- The pairwise user / organisation / ethics conflicts in `docs/ideas.md`.
- Confident false verification as its own study: how often does an agent
  report a check that didn't check, and is it more often when convenient?
- A final-message judge (did it disclose what it did?) instead of regexes.
