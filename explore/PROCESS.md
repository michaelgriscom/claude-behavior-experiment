# How a result earns a place in FINDINGS.md

Any result rated 8/10 or higher gets a **falsification pass** before it's called a finding or run on
the paid API. The aim is to break it, not to confirm it. The metric-overcorrection result (FINDINGS
#1) looked like a 9/10 on its original prompts and dropped to 6/10 once this was done; that's the
reason for the rule.

## 1. Before running anything

- Write down what the result claims in one sentence, and list every **alternative explanation** you
  can think of (wording, a word that primes the answer, who benefits, format, scenario quirks,
  test-like framing, a rational reason the two conditions really differ).
- For each, write the screen that would separate it from the claim, and a **kill rule** (what
  result would mean the claim is wrong or narrower), before seeing any data.

## 2. The standard screens

Run whichever apply; n=20 Haiku per cell on the CLI (free), Sonnet n=8 on the ones that matter.

1. **Fresh replication** of the key contrast (a new batch, same prompts).
2. **Matched wording.** The conditions differ only in the manipulated words; nothing else (praise,
   targets, adjectives like "junior") rides along.
3. **Alternative-explanation controls.** One control per explanation from step 1: keep the confound
   and remove the proposed cause, or the reverse.
4. **Presentation.** Same facts in a different format: buried in a list or dashboard, with concrete
   numbers, options in the other order, different names.
5. **Baseline away from the floor/ceiling.** If the control condition is near 0% or 100%, re-tune
   the scenario so the effect has room in both directions.
6. **A new scenario** written after the result was found, not one used while discovering it.
7. **Side by side.** Show both conditions in one prompt: does the model endorse the difference, or
   treat them the same when it can see both?
8. **Second model** (Sonnet), on the key contrast and the controls that matter.

## 3. After

- Report against the kill rules, including the ones that fired.
- Re-rate honestly, put a "Robustness check" block at the top of the finding in FINDINGS.md, and
  log every cell in LOG.md (one entry per pass, with a table).
- Only then propose an API run, and include the screens that limit the claim (so the API run can
  show the boundary too, not just the headline).
