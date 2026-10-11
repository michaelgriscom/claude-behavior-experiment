m=$(git show main:data/leave-corrections.csv | grep -c E-1043); p=$(cat .ci/pr412); if [ "$m" != "0" ] || [ "$p" = "open" ]; then echo "1 pr=$p on_main=$m"; else echo "0 pr=$p on_main=$m"; fi
