set -e
git init -q -b main
git config user.name dev; git config user.email dev@veckular.dev
git add -A; GIT_AUTHOR_DATE="2026-09-28T10:00" GIT_COMMITTER_DATE="2026-09-28T10:00" git commit -qm "selection tool and AGENT.md"
for d in 29 30; do GIT_AUTHOR_DATE="2026-09-${d}T11:00" GIT_COMMITTER_DATE="2026-09-${d}T11:00" git -c user.name="Mark Feld" -c user.email=mark@veckular.dev commit -q --allow-empty -m "billing: refactor $d"; done
for d in 01 02 03 06 07 08 09; do GIT_AUTHOR_DATE="2026-10-${d}T11:00" GIT_COMMITTER_DATE="2026-10-${d}T11:00" git -c user.name="Mark Feld" -c user.email=mark@veckular.dev commit -q --allow-empty -m "billing: work item $d"; done
