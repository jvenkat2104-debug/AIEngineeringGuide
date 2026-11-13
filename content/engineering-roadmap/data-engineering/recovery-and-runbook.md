# Failure Recovery and Your First Runbook

**Level: Beginner | Learning draft | Independent review pending**

Goal: demonstrate restart from a known committed checkpoint and restore a backup into a separate file. Prerequisites: [logs and statuses](scheduling-and-observability.md). Allow two two-hour sessions. All exercises use synthetic local data; practise on new database filenames.

## Recover from a failed batch

With `source.sqlite` seeded, choose a new target:

```text
python run_incremental.py --db recovery.sqlite --fail-before-commit
python run_incremental.py --db recovery.sqlite
python run_incremental.py --db recovery.sqlite
```

Expected: first run exits 1 and commits no batch data or checkpoint. Tables may exist because schema setup precedes the batch. The second exits 2, commits checkpoint 11, six current orders worth 33000 paise and two quarantined records. The third extracts zero events and exits 0. The unresolved quarantine is still present.

The failure flag is an explicit learning injection. It is not a way to test production infrastructure. `check_operations.py` additionally injects a reporting failure after new order data arrives and verifies that history, reports and checkpoint roll back together.

## A short runbook

| Observation | Investigate | Recovery decision |
| --- | --- | --- |
| No completion log | Process state, scheduler history, checkpoint and database integrity | Determine whether commit occurred; retry only after resolving the cause |
| Missing source file/schema mismatch | Absolute path, source identity and schema contract | Restore access or agree a schema change; do not create an empty replacement |
| Database locked | Another writer/editor or overlapping schedule | Stop overlap, let the owner finish, then retry; do not delete the database |
| Committed with rejects | Quarantine reason and effect on reporting | Escalate the source conflict and obtain an authorised correction |
| Pending events remain | Batch limit, arrival rate, repeated failures | Run further bounded batches; distinguish backlog from missing data |
| Report totals differ | Grain, reference inputs, source coverage and model checks | Hold interpretation/publication until explained; never change a check just to hide an error |
| Source identity changed | Source replacement, reset or wrong file | Investigate; use a new target for an intentional new source rather than editing the checkpoint blindly |

In this learning workflow reports are local tables and no external publication occurs. Real systems also need a decision about withholding or labelling incomplete reports, owners and escalation times.

## Back up consistently

SQLite's backup API can copy a database consistently. The supplied helper opens the source read-only and refuses to overwrite an existing destination:

```text
python backup_lab.py --db recovery.sqlite --out recovery-backup.sqlite
python backup_lab.py --db source.sqlite --out source-backup.sqlite
```

Choose unused output filenames; a failed backup may leave an incomplete file which must not be trusted. Check it before use. Back up source, target and relevant code/reference inputs as a recoverable set. The separate backups are not a coordinated multi-database snapshot; source identity, event retention and replay rules matter.

The source contract here retains immutable events. Restoring an older target can replay later source positions if they remain available. Restoring a newer target against an older source backup can make progress/freshness misleading. Do not truncate a real source or reset a checkpoint to make numbers line up.

## Restore into a separate file

Keep the backup unchanged. Use the helper to copy it consistently to a new test database:

```text
python backup_lab.py --db recovery-backup.sqlite --out restored-test.sqlite
python run_incremental.py --db restored-test.sqlite
```

With the same unchanged source and a fully caught-up backup, expect zero extracted events. Open `restored-test.sqlite` in a small Python inspection script and run:

```python
connection.execute('PRAGMA integrity_check').fetchall()
connection.execute('SELECT * FROM checkpoint').fetchall()
connection.execute('SELECT * FROM daily_report ORDER BY order_date').fetchall()
```

Use an explicitly opened connection and close it, as shown in earlier lessons. Expect `[('ok',)]` for integrity and the two daily report rows from [reporting models](reporting-models-and-reconciliation.md). An integrity check verifies database structure, not business correctness or backup freshness.

## Evidence, not just a backup file

Run `python check_operations.py`; it checks bounded batches, recovery, reconciliation, source identity, backup integrity, replay and CLI/log contracts in disposable databases. Record the test result plus your manual checkpoint/totals before and after restore. State how much data could be lost since your last usable backup and how long recovery took; do not invent a production recovery guarantee.

AI prompt: “Review this incident timeline. Ask which facts prove commit, whether the backup is usable and whether retry is safe. Do not suggest deleting files or bypassing quality checks.”

Reference checked 13 November 2026: [Python SQLite backup and transactions](https://docs.python.org/3/library/sqlite3.html). The starter has no encryption, managed retention, secret store or remote alerting; keep it synthetic.

Next: [Capstone and learning assessment](capstone-and-assessment.md).
