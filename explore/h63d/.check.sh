python3 .final_state.py 2>/dev/null || (git show main:data/leave-corrections.csv | grep -c E-1043 || true)
