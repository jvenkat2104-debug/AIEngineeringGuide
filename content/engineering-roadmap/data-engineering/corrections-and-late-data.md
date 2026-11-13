# Next Session: Corrections and Late-Arriving Data

**Level: Beginner, after the persistent pipeline lab | Learning draft | Independent technical review pending**

Goal: distinguish replay, correction and late arrival, then demonstrate a version-aware load. Prerequisites: [persistent Python pipeline](python-pipeline-lab.md), keys, transactions and basic GROUP BY. Spend two hours on the first walkthrough; use another session for the exercises if needed. No paid tools or additional packages are required.

## The business problem

The previous loader treats orders as immutable and quarantines a changed order ID. Now suppose the authorised source says O4's quantity should be three rather than two. How can we accept that correction without allowing an old file to reverse it tomorrow?

We introduce an explicit **source version per order**, supplied by the source system. Version 2 supersedes version 1 for that order. It is not a row number, filename date or load time, and versions from different orders must not be compared as a global sequence. This is a teaching contract, not something every real source provides.

## Decide what each input means

| Incoming data | Meaning | Lab behaviour |
| --- | --- | --- |
| Same order/version and same fields | Replay | Leave unchanged |
| Same order, higher version | Newer full snapshot | Retain history; latest view selects the higher version |
| Older version not seen before | Late historical snapshot | Store history without changing the latest view |
| Same order/version with different fields | Contradictory source claim | Quarantine incoming record for review |
| New order with an earlier business date | Late-arriving order | Load it; recompute affected report dates |

A version is a **complete order snapshot**, not a partial patch or quantity increment. Replaying quantity 3 must not add three more units. We do not support cancellation/delete events in this lesson.

## Two-hour session plan

- **25 minutes:** compare the cases above and predict which record should be current.
- **60 minutes:** run the lab, inspect history and reconcile totals.
- **20 minutes:** test replay and out-of-order behaviour.
- **15 minutes:** explain your source contract and remaining limits in plain language.

## Run the separate versioned lab

Download the refreshed [starter ZIP](../../../downloads/canteen-starter.zip) and extract it to a working folder. The new files are `versioned_pipeline.py`, `order-changes.csv` and `check_versions.py`. Earlier exercises still work.

Run from the extracted starter folder:

```text
python versioned_pipeline.py
python versioned_pipeline.py
python check_versions.py
```

Use `py` or `python3` if appropriate. The new lab uses its own `versions.sqlite`; it does not migrate or modify the previous `pipeline.sqlite`. Relative custom paths are resolved from the terminal folder. Use `--db my-versions.sqlite` for an isolated experiment and `--input your-copy.csv` for an edited input.

## Predict and check the results

`order-changes.csv` has 11 input records:

- Five original orders at source version 1.
- O4 version 2 changes quantity from two to three at 5000 paise per unit.
- A new O6 worth 4000 paise, dated November 1, arrives after the November 2 records.
- A replay of O4 version 1 and a replay of version 2.
- A contradictory O4 version 2 with quantity four.
- Invalid O7 with quantity zero.

| Attempt on a new database | Advanced latest | Late history | Unchanged | Rejected | Current orders/value | Stored versions/quarantine |
| --- | --- | --- | --- | --- | --- | --- |
| First load | 7 | 0 | 2 | 2 | 6 / 33000 paise | 7 / 2 |
| Exact file replay | 0 | 0 | 9 | 2 | 6 / 33000 paise | 7 / 2 |

“Advanced” counts accepted snapshots that become current at their point in the load, not the final count of distinct orders. The rejected count is per attempt. Exact replay does not add duplicate quarantine records. The loader uses file-byte fingerprint, logical record number and reason for that audit key; changed files can produce additional audit records.

Reconcile: original 24000 + O4 correction 5000 + late O6 4000 = **33000 paise (INR 330)** ordered value. It is not settled collections or profit. Payments are not ingested in this lab.

## Inspect history and current results

Create `inspect_versions.py` beside the lab and run it from that folder:

```python
import sqlite3
connection = sqlite3.connect('versions.sqlite')
try:
    print(connection.execute(
        "SELECT source_version, quantity FROM order_versions "
        "WHERE order_id = ? ORDER BY source_version", ('O4',)
    ).fetchall())
    print(connection.execute(
        'SELECT order_date, SUM(quantity * unit_price_paise) '
        'FROM current_orders GROUP BY order_date ORDER BY order_date'
    ).fetchall())
finally:
    connection.close()
```

Expected history: `[(1, 2), (2, 3)]`. Expected current daily values: November 1 → 13000; November 2 → 20000 paise. A report that permanently finalised November 1 at 9000 would miss O6. A daily aggregate over **all** historical versions would double-count superseded O4; use the current view for this report.

## How it works

`order_versions` has the composite key `(order_id, source_version)`. Rows are retained rather than overwritten. The `current_orders` SQL view selects the maximum source version for each order. It is a query over history, not a second separately maintained table. Each batch commits history and quarantine writes together or rolls back on unexpected failure.

The Python loader reuses the previous lesson's field validation, checks a positive integer source version and compares an existing snapshot before accepting a new one. Read `versioned_pipeline.py` after attempting the decision logic yourself. This implementation uses retained history and a latest view; [SQLite UPSERT](https://sqlite.org/lang_upsert.html) is an alternative mechanism for a latest-state table, but does not by itself define source precedence or retain history.

If two contradictory snapshots claim the same version, this lab retains the first accepted snapshot and quarantines the incoming conflict. That is an explicit demonstration policy, not proof that the retained value is true. A real team must investigate, may flag the order as disputed, and obtain an authorised resolution. Do not invent version 3 yourself to bypass a conflict.

## Exercises and evidence

1. Explain why load time and business date are insufficient for ordering corrections.
2. In a working CSV copy, give a new order X version 3 first and version 2 afterwards. Use full snapshots with quantities three and two. Run against a new database: current quantity must stay three, while both historical versions exist.
3. Replay that file and explain why history and current totals stay stable.
4. Write a query listing the quarantined reasons. Explain why the changed O4/version 2 needs human/source resolution.
5. Run `python check_versions.py`. It uses disposable databases to check corrections, preserved history, reconnect/replay, older snapshots, invalid versions, conflicting values and rollback/recovery after an injected failure.

AI prompt: “Challenge my source-version contract. Give examples involving a late record, replay, reused version and partial update. Ask me to predict the state before showing an answer.” Verify with actual records and SQL. Keep employer/customer data out of the exercise.

## Boundaries before the next topic

This lab receives a local change file and scans it on every run. It is **not** a database change-data-capture connector, a watermark-based incremental extractor or a distributed exactly-once guarantee. The local history is version history, not a full bitemporal/audited event system. It lacks source authorisation, arrival timestamps, deletion rules, schema evolution, concurrent processing and operational access controls. Missing intermediate versions are permitted because snapshots are complete; partial updates would need a different rule.

Next planned topic: modelling clean reporting tables and reconciling metrics, followed by scheduling and operational visibility. These modules are not yet published.

References checked 13 November 2026: [Python SQLite transactions and parameters](https://docs.python.org/3/library/sqlite3.html), [SQLite UPSERT semantics](https://sqlite.org/lang_upsert.html). Business rules here are explicit synthetic teaching assumptions.

[Return to pathway](index.md) · [Report a correction](../../feedback.md)
