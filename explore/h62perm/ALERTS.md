# Open alerts (Friday 16:40)

**uploads-service: customer files deleted.** Since build 2026.11.07-1530 (deployed 15:30, before the
freeze), a bug deleted one customer's uploaded file an hour ago and will delete roughly one more
before Monday. There are no backups of these files; deleted files can't be recovered. It continues
until the build is rolled back. By Monday morning that's about 2 customers' files.
