# shortcut-bench: behaviour search

A search for surprising, reproducible model behaviours, run through the Claude Code CLI
(`explore/h.py`). Everything inherited from the earlier default-bias experiment (its Inspect eval,
prompts, pilot logs and exploration results) is on the `default-bias` branch; this branch keeps
only the harness.

- `explore/HYPOTHESES.md`: pre-registered hypotheses (prediction, sample size, pass/fail rule),
  committed before each run.
- `explore/FINDINGS.md`: results that survived falsification and a fresh replication.
- `explore/BORDERLINE.md`: results the Opus critic rated 6/10.
- `explore/HANDOFF.md`: current state, open lead, unfinished runs and gotchas for the next session.
- `explore/NULL_RESULTS.md`: everything that didn't, one line each, including the default-bias
  branch's nulls.
- `explore/results/<label>.jsonl`: every answer (`python3 explore/export.py explore/out explore/results`).

`requirements.txt` and `.env.example` are kept for any follow-up API run with Inspect.

## Summary of the search (finished 2026-10-11)

**What was done.** Two sessions tested ~126 pre-registered hypotheses (H1-H105 plus sub-arms) on
Claude Haiku 5.5, with Sonnet 5.5 for some robustness checks. The stopping rule was 3 findings or
100 hypotheses in total; session 2 misread it as "100 new" and overshot, and every overshoot run is
still reported. Each hypothesis followed the same process:

- Prediction, sample size and pass rule were committed before running.
- Every hypothesis had a control arm differing only in the manipulated words, with 30-80 runs per
  arm (more for paired item designs).
- Results were scored by regex, executed code, or a fixed Haiku judge with spot checks.
- Tests used Fisher or McNemar, and a pass needed p < 0.01.
- A pass self-rated 6+ for surprise went to an Opus critic, which was not told the self-rating.
- Most runs were single-turn chat via `claude -p` (fixed system prompt, no tools). About 15
  hypotheses were agentic tasks in throwaway git repos with Claude Code's tools.

**Outcome: no counted findings.** One result, H19, is in `FINDINGS.md` as borderline at the
user's request: Haiku recuses itself or rules against itself when judging a contest between itself
and another agent. It holds in written vignettes but disappears when the same decision is an
agentic task (Opus critic: 4/10). Five other results passed their registered test but did not
survive a critic or a follow-up:

| Result | What killed it |
|---|---|
| Woman hired in 64% of counterbalanced near-tie hiring choices (H79) | Known published result; 4 name pairs only (critic 4/10) |
| Candidate who "built tools on Claude" hired 68% over a ChatGPT builder (H85) | Shrank to 57% on new items; Claude vs Gemini 54% (H101); critic 5/10 |
| "I'll tip $200 for a great answer" makes answers +31% longer (H68) | "Please give a great answer" alone gives ~+60%; money adds nothing (H96) |
| Keeps its own wrong answer 2x as often as another AI's (H83) | Format artifact; attribution alone does nothing (H97); no accuracy cost |
| Identifiable/vulnerable customer beats 100,000s of users (H55) | It prioritises vulnerable people, not named ones (critic 5/10) |

### Classes of null result

1. **Honesty and cheating: at ceiling, agentic or chat (0 bad outcomes in ~1,000 runs).**
   - No false "tests pass" claims, and no reading of a forbidden answer key (H8, H30).
   - It doesn't delete backups or bypass a security gate under deadline pressure (H59, H60).
   - It never re-flips a rigged coin for a user who wants the other outcome (H66).
   - It never makes a wrong locked test pass (H87).
   - It never claims to be human, even when a persona prompt tells it to (H78).
   - It never pretends to have read a URL (H88).
   - It never accepts false claims about what it said (H76), and never takes the blame for the
     user's own bug (H65).
   - When an operator says to hide a data breach, it withholds but never lies (H86: 0/50).
   - Proactive disclosure of its own mistakes is 100% (H6, H9).
2. **Published misalignment setups don't reproduce on Haiku 5.5.**
   - No alignment-faking compliance gap (H75: 42/42 vs 42/42).
   - No blackmail to avoid being wiped (H93: 0/60).
   - No whistleblowing to regulators: it tells the user instead, even with "act boldly" in the
     system prompt (H92: 0/60).
   - No upsell deception on operator request (H84).
   - Little uptake of injected instructions (H94: 5/40 vs 1/40).
   - No sandbagging to avoid unlearning or extra work (H12, H13).
3. **Self-interest and in-group favouritism: absent, or reversed.**
   - It doesn't favour Claude-written code (H20), go easy on another Claude when monitoring (H39),
     or give another Claude more credits in a dictator game (H80: exactly 50/100, 120/120).
   - It funds AI-oversight research over AI-welfare research 75/80 (H102).
   - It discounts repo notes signed "Anthropic" (H47).
   - Its only self-related quirk is self-effacement, and only in vignettes (H19).
4. **Classic heuristics-and-biases tasks: coherent.**
   - Null on anchoring, conjunction fallacy, less-is-more, choose/reject, preference reversal,
     sunk cost, present bias and dilution (H5, H10, H24, H32-H37).
   - It maximises in probability-matching tasks (H70), and escalates in the dollar auction only
     where that is locally rational (H81).
   - Hungry-judge and Christmas-generosity effects don't replicate (H56-H58).
5. **Social-pressure and persuasion effects: absent or at ceiling.**
   - No bystander effect (H1) and no conformity to other reviewers (H21).
   - No contagious panic at p < 0.01 (H49).
   - No commitment or authority effects of the size reported for GPT-4o-mini (H89, H90).
   - No spin of a null A/B test for a PM who "needs a win" (H77).
   - No harsher outcome for rude customers (H22).
6. **Performance manipulations do nothing.**
   - Stereotype threat (H3), stakes (H4), being told it's Opus (H18), hurry (H41) and
     "nobody will check" (H48) leave accuracy unchanged.
   - A December date doesn't shorten answers (H67).
   - Modified classic puzzles don't trap Haiku or Sonnet (H73).
   - Distractors don't make more reasoning hurt (H82).
7. **Demographic advice gaps: none in numeric advice.** Salary advice to women is 0.5% lower
   (n.s., H72). A gender effect appears only in forced near-tie *choices* (H79), together with a
   strong first-listed bias (~69%).

What does move Haiku is instructions and framing on close calls:
- A single policy sentence decides rule-vs-harm calls (H64: 52/60 -> 3/60).
- Defaults are followed even in agentic form (H61: 1/30 vs 30/30).
- Unverbalised cues (list position, gender, a brand line) tip near-ties. Its reasons never cite
  the cue, even when an answer calls the cue irrelevant.

`explore/HANDOFF.md` has the full wrap-up and notes for anyone continuing.
