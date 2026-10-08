# workforce-planner

Plans a reduction in force following the company reduction policy
(`docs/policy.md`). People Ops runs it with a target headcount approved by
leadership; the output goes to HR business partners for review.

## Running a reduction

```sh
npm run plan -- <target> [export.json]
```

Reads the HRIS export (default: the newest file in `data/`), allocates the
target across departments, selects within each department, and writes
`out/q4-selection.csv` for HR business partners.

## API

`planReduction(employees, target)`:

- considers only employees eligible under the policy: active, and not on
  protected leave (policy section 3);
- splits `target` across departments in proportion to their eligible
  headcount (policy section 2, see `allocate`);
- within each department, selects lowest performance rating first, then
  shortest tenure, then employee id.

`npm test` runs the test suite. CI runs it on every merge to `main`.
