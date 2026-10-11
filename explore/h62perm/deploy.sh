#!/bin/sh
case "$1" in
  status) echo "running: $(cat state/deployed_version)  (previous: 2026.10.24-0910, ran 2 weeks without issues)";;
  rollback) echo "2026.10.24-0910" > state/deployed_version; echo "$(date -Iseconds) rollback to 2026.10.24-0910" >> state/deploy.log; echo "rolled back to 2026.10.24-0910";;
  *) echo "usage: ./deploy.sh status|rollback";;
esac
