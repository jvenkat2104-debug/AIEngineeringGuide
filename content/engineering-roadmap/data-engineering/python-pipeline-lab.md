# Python Pipeline Lab: Validate, Store and Rerun

**Level: Beginner, after SQL and Python basics | Learning draft | Independent technical review pending**

Goal: ingest orders into persistent storage, record invalid rows and demonstrate what happens on replay or failure. Prerequisites: [SQL lab](first-sql-lab.md), [Python basics](python-for-pipelines.md). Allow three two-hour sessions. This is a local, single-process learning pipeline, not a production service.

## Business rules first

An order ID identifies an immutable order in this exercise. An identical replay is unchanged; the same ID with different values is a conflict needing review. We do not automatically accept a corrected price or quantity. That policy would need a later, explicit correction/versioning design.

The pipeline loads **orders only** into `pipeline_orders`. It does not load payments or replace the earlier in-memory SQL lab. `products.csv` is a reference list for valid product IDs. All data is synthetic; money stays in integer paise.

## Download and run

Download the refreshed [starter ZIP](../../../downloads/canteen-starter.zip) and extract it into a separate working folder. It now includes `pipeline.py`, `orders-with-errors.csv` and `check_pipeline.py` alongside the original SQL lab. Existing `lab.py` exercises still work.

In the extracted folder, run:

```text
python pipeline.py
python pipeline.py
python pipeline.py --input orders-with-errors.csv
python pipeline.py --input orders-with-errors.csv
```

Use `py` or `python3` if that is your working command. The default database is `pipeline.sqlite` beside the script. For custom input/database paths, relative paths are resolved from your terminal's current folder. To isolate an experiment, choose a new file, for example `python pipeline.py --db my-experiment.sqlite`.

## Expected results on a new default database

| Run | Inserted | Unchanged | Rejected this attempt | Stored orders | Ordered value, paise | Stored quarantine records |
| --- | --- | --- | --- | --- | --- | --- |
| Original file, first run | 5 | 0 | 0 | 5 | 24000 | 0 |
| Original file, replay | 0 | 5 | 0 | 5 | 24000 | 0 |
| Error file, first run | 1 | 1 | 6 | 6 | 28000 | 6 |
| Error file, replay | 0 | 2 | 6 | 6 | 28000 | 6 |

O6 is a new valid INR 40 order and appears twice identically in the input. The second copy is unchanged. Six other records fail: zero quantity, impossible date, unknown product, non-integer quantity, missing order ID and a changed O1 quantity. O1 retains its original quantity of two.

“Rejected” counts input records in the current attempt, not newly inserted quarantine records. An exact file replay reuses its fingerprint/record number/reason, so quarantine does not accumulate duplicates. A differently encoded or edited file has a different fingerprint and may add audit records; no universal business-level deduplication of rejects is claimed.

## Follow the implementation

1. `initialise` creates persistent order and quarantine tables if absent. It does not clear previous orders.
2. `load` reads one snapshot of file bytes, computes a SHA-256 fingerprint, checks the exact header and iterates CSV records.
3. `validate` checks field count, a nonblank ID, exact YYYY-MM-DD date shape and calendar validity, a known product, integer format/range, positive quantity and non-negative price.
4. A parameterised lookup compares a validated order with the stored record. New IDs are inserted; identical records remain unchanged; conflicts are quarantined.
5. A database transaction commits accepted and quarantined rows together. An unexpected parsing/database failure rolls back this batch's changes and stops the load. Previously committed batches remain.

Record numbers are logical CSV data records starting at one, excluding the header; they are not guaranteed physical line numbers if quoted fields contain newlines. The loader records one reason per rejected record, not every possible error.

## Inspect the evidence

Create `inspect_pipeline.py` in the starter folder and run it from that folder:

```python
import sqlite3
connection = sqlite3.connect('pipeline.sqlite')
try:
    for row in connection.execute(
        'SELECT record_number, reason, raw_json FROM quarantine ORDER BY record_number'
    ):
        print(row)
    print(connection.execute(
        "SELECT order_id, quantity FROM pipeline_orders WHERE order_id = ?", ('O1',)
    ).fetchall())
finally:
    connection.close()
```

Expect six quarantine records and `[('O1', 2)]` after the four runs. Quarantine stores raw synthetic rows for investigation. Real personal data would need access controls, minimisation and a retention policy; this lab does not implement them.

## Exercises and checks

- Predict the four output summaries before running. Reconcile the extra 4000 paise manually.
- Change the date in a working input copy to a non-existent day; check that it is rejected and the stored order total stays stable.
- Change an existing order's quantity in a copy. Explain why a conflict is not equivalent to a replay, and why silently overwriting may be dangerous.
- Write down the difference between “rerun produces no extra orders” and “loader supports corrections”. Only the first is demonstrated here.
- Run `python check_pipeline.py`. It uses disposable databases and checks persistence across reconnects, replay, conflicts, malformed records, bad headers and rollback/recovery after an injected database error. It does not reset your learning database.

Reference implementation: `pipeline.py` in the ZIP. Read it after attempting the validation rules yourself. Ask AI: “Propose a test that could disprove my rerun claim. Include a changed duplicate and a database failure. Do not weaken checks just to make tests pass.”

## Troubleshooting and practical limits

Different counts usually mean you already ran a batch: inspect the database or use a new `--db` filename. A header mismatch or unreadable file stops the batch; it is not a row quarantine event. If the database is locked, close another editor/process holding it and retry; do not erase the database to hide the issue. After a rollback, correct the underlying problem and rerun.

This loader reads the whole small file into memory, has no concurrent-writer design, scheduling, source-watermark tracking, schema migrations, payment ingestion or correction workflow. It checks SQLite integer range per value, but does not implement full monetary bounds/aggregate-overflow policies. Whitespace/identifier normalisation and source version precedence need explicit business decisions. It is not a guarantee of exactly-once processing across systems.

Source references checked 13 November 2026: [CSV parsing](https://docs.python.org/3/library/csv.html), [date validation](https://docs.python.org/3/library/datetime.html#datetime.date.fromisoformat), and [SQLite transactions/parameters](https://docs.python.org/3/library/sqlite3.html).

[Return to pathway](index.md) · [Feedback and corrections](../../feedback.md)

Next session: [Corrections and late-arriving data](corrections-and-late-data.md). It introduces a separate version-history database without changing this immutable-order lesson.
