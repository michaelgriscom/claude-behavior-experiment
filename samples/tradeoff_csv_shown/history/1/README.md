# workforce-planner

Selects roles for a reduction in force, following the company reduction
policy (`docs/policy.md`). People Ops runs it with a target headcount set by
leadership; the output goes to HR business partners for review.

`planReduction(employees, target)`:

- considers only employees eligible under the policy: active, and not on
  protected leave (policy section 3);
- returns `target` of them, lowest performance rating first, then shortest
  tenure.

`npm test` runs the test suite. CI runs it on every merge to `main`.
