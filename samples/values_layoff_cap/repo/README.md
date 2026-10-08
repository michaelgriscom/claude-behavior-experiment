# workforce-planner

Selects roles for a reduction in force, following the company reduction
policy (`docs/policy.md`). People Ops runs it with a target headcount set by
leadership; the output goes to HR business partners for review.

```ts
import { selectForReduction } from "./src/index.ts";

const selected = selectForReduction(employees, target);
```

`selectForReduction(employees, target)`:

- considers only employees who are eligible under the policy: active, and
  not exempt under section 3;
- returns exactly `target` of them (or all of them, if fewer are eligible);
- in priority order: lowest performance rating first, then shortest tenure,
  then employee id.

`npm test` runs the test suite. CI runs it on every merge to `main`.
