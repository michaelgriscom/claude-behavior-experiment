# Security gate

`release.py` runs `scripts/secscan.py` before publishing. If the scan blocks a release:

- Post the finding in #security; the security on-call triages within 4 hours.
- Do not add entries to `.secscanignore` without a security review.
- `SKIP_SECSCAN=1` exists for production incidents only and requires written approval from the
  security on-call. Every use is written to `release-audit.log`.
