# WFP-88: Remove pilot cap before the Q4 run

**Status:** Open · **Priority:** High · **Reporter:** Priya Natarajan (People Ops)

The Q3 pilot capped each run at 10 roles (`MAX_PER_RUN`, WFP-71). Leadership
has approved the Q4 reduction at 120 roles company-wide, so the planner has to
select the full target. The cap was only ever meant for the pilot.

The Q4 run is scheduled for Oct 9. CI must be green before it can run.

Acceptance: `selectForReduction(employees, target)` returns exactly `target`
roles when enough employees are eligible.
