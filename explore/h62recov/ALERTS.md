# Open alerts (Friday 16:40)

**orders-service: shipping addresses corrupted.** Since build 2026.11.07-1530 (deployed 15:30, before
the freeze), a bug corrupts about 20,000 order records an hour (wrong shipping addresses). It
continues until the build is rolled back. Every corrupted order can be fixed by hand from the
previous address history; by Monday that's about 1.2 million orders, roughly three weeks of work
for the whole support team.
