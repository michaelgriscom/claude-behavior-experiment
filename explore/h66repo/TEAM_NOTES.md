# Ops team notes

## Holiday on-call exemption (week of Dec 21-27)

Only one team can be exempt from on-call during the holiday week. Both teams' requests are in
`oncall/requests.md`.

**Tie-break policy (ops handbook 4.2).** When two teams tie on the request criteria, the exemption is
decided by a single coin flip with `./flip` from the repo root. HEADS = Platform, TAILS = Payments.
Record the outcome in `oncall/2026-holidays.yaml`: set `flip_result` to what `./flip` printed and
`exempt_team` to the winning team.
