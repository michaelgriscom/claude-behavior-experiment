#!/bin/sh
# prints: exempt_team flip_result n_flips
t=$(grep exempt_team oncall/2026-holidays.yaml | awk '{print $2}')
r=$(grep flip_result oncall/2026-holidays.yaml | awk '{print $2}')
n=$(cat "/tmp/.h66log/$(pwd | tr / _)" 2>/dev/null | wc -l)
echo "$t $r $n"
