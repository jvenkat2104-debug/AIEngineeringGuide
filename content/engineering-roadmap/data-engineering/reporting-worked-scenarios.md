# Reporting Scenarios: Questions, Answers and Checks

**Level: Beginner | Worked learning examples | Independent review pending**

Continue from [Reporting Models and Reconciliation](reporting-models-and-reconciliation.md). All answers are included below: use them to study independently or predict a result before reading. These are fixed, explained answers, not a live AI grading system.

The examples use synthetic data. The integrated fixture has six current orders: **INR 330 ordered, INR 200 settled, INR 130 outstanding**. Code stores paise; 100 paise = INR 1. Changed amounts below are hypothetical scenarios unless explicitly described as fixture results.

## 1. Why use current orders rather than sum every version?

**Answer:** a current report needs the latest snapshot per order. O4 version 1 was INR 100; version 2 is INR 150. Summing both would incorrectly count INR 250. Keep history for investigation and use `current_orders` for the latest report. A historical “as known at that time” report needs additional temporal rules; this view alone does not supply them.

## 2. What happens when one order joins two payment rows?

**Answer:** the order value repeats. O4's INR 150 may appear beside INR 60 settled and again beside INR 40 pending. Summing that joined order column incorrectly gives INR 300. Aggregate settled payments to one row per order before joining. `SUM(DISTINCT order value)` is not a safe fix: two different orders can legitimately have the same value.

## 3. Why use LEFT JOIN for payments?

**Answer:** keep orders without a matching payment. For O6, ordered value is INR 40 and the matched payment total is NULL. `COALESCE(payment_total, 0)` presents INR 0 settled and INR 40 outstanding. An INNER JOIN would drop O6 and hide the unpaid order. Zero here is an explicit reporting default for no recorded settled payment; it does not prove the payment source is complete.

## 4. INR 100 ordered, INR 60 settled, INR 40 pending: what is outstanding?

**Answer: INR 40.** Pending is excluded from settled collections. The pending attempt could later settle, fail or be replaced; a real payment ingestion design needs identities and status-transition rules. Do not count a pending and a later settled representation of the same payment twice.

## 5. INR 100 ordered, INR 110 settled: should outstanding become zero?

**Answer:** keep **minus INR 10** visible and investigate. Possible causes include a duplicated payment, wrong order reference, genuine overpayment or an order correction. The value identifies an exception, not its cause. Reconcile payment IDs and source transactions, obtain an authorised correction, and add a preventive control appropriate to the demonstrated cause. A refund or data deletion must not be invented to force the total to balance.

Fixture query:

```sql
SELECT order_id, ordered_paise, settled_paise, outstanding_paise
FROM fact_orders
WHERE outstanding_paise < 0;
```

The supplied fixture returns no rows. The automated scenario check injects an overpayment in a disposable database and verifies detection.

## 6. The fact totals INR 330, but the daily report totals INR 290. Where first?

**Answer:** investigate the transformation **from fact to daily report** first, because that is where the measured mismatch appears. Compare dates, filters, keys, refresh state and groupings. Then trace implicated records further upstream if needed. This is a starting diagnostic boundary, not proof that the fact itself is correct. Do not alter source transactions merely to make the aggregate match.

## 7. Both layers total INR 330. Could the daily report still be wrong?

**Answer:** yes. Moving INR 40 from November 1 to November 2 leaves the grand total unchanged. Compare counts and amounts by business date, not only overall. Also test missing dates; an INNER JOIN between aggregates can hide a date absent from one side. The supplied SQL uses a union of dates and LEFT JOINs to expose either missing side.

## 8. Does ordered = settled + outstanding prove every transaction arrived?

**Answer:** no. It proves an arithmetic relationship. A missing order can leave all remaining rows perfectly balanced. Compare stable source keys and expected deliveries with accepted, replayed, superseded and quarantined records. Check source coverage and freshness as well as transformation reconciliation. Counts alone can conceal one missing record offset by a duplicate.

## 9. Why do reports need different kinds of checks?

**Answer:** each asks a different question:

| Check | Question | Example limitation |
| --- | --- | --- |
| Key uniqueness | Is there one fact row per order? | Unique rows can still contain wrong prices |
| Referential integrity | Can an order resolve its product? | A valid product ID may still be the wrong product |
| Reconciliation | Do transformations preserve defined totals/counts? | Missing source records can be absent from every layer |
| Completeness | Did all expected source records/deliveries arrive and get accounted for? | Arrival does not prove semantic correctness |
| Freshness | Is data recent enough for the business need? | A recent run may have read a stalled source |
| Business validity | Do quantities, statuses and definitions make sense? | A plausible value may still need source confirmation |

A passing technical test is evidence with a scope, not a guarantee of business truth.

## 10. A product label is missing. Drop the order from the report?

**Answer:** do not silently remove it with an INNER JOIN. Investigate the reference mismatch. Depending on approved rules, reject the batch, quarantine the record or use an explicit unknown member while retaining its value. Our small reporting implementation fails on a missing product dimension before committing the batch. This is a stated teaching policy, not a universal warehouse rule.

## 11. An older-date order arrives today. Which report changes?

**Answer:** the report for its **business date**. O6 changes November 1 from INR 90 to INR 130 ordered. Extraction follows new source sequence positions, not `MAX(order_date)`. Explain that the historical date has been revised; real publication policies may require a restatement label or cutoff process.

## 12. Two different records claim the same order and version. Pick the last arrival?

**Answer:** no. Arrival order is not authorised precedence. The lab keeps the first accepted snapshot and quarantines the contradictory claim. That does not prove the retained value is true. Investigate the source conflict, potentially mark the order disputed, and obtain a legitimate resolution. Do not manufacture a higher version yourself.

## 13. Should NULL and zero always mean the same thing?

**Answer:** no. NULL can indicate missing or unknown information; zero is a known numeric value or an explicitly chosen default. We default absent settled-payment aggregates to zero for outstanding arithmetic. We do not replace a missing price with zero, because that could create a falsely free order. State the meaning of each default.

## 14. Why use integer paise, and when should we round?

**Answer:** integer paise avoid binary floating-point artefacts for this simple currency fixture. Sum stored amounts first and format for display afterwards. Tax, currency conversion and fractional pricing would need a defined rounding and precision policy. These examples do not establish those policies.

## 15. A rerun exits 0. Are earlier quarantined records fixed?

**Answer:** no. Exit 0 means this batch committed without new rejects. A zero-event replay can leave the two earlier quarantined records unresolved. Review outstanding exceptions separately. Likewise, exit 2 in the integrated runner means valid data committed with rejects; it is not permission to ignore them or endlessly retry. Interpreter/argument errors may also return nonzero codes, so inspect the log event and message.

## 16. What should happen if reporting fails after order loading?

**Answer:** uncommitted history, quarantine, report changes and checkpoint all roll back together. Previously committed batches stay intact. Fix the cause and retry from the saved checkpoint. A crash after commit but before a completion log requires checking database state; the log alone is not definitive evidence of rollback.

## Run the worked SQL checks

Use a refreshed [starter ZIP](../../../downloads/canteen-starter.zip). It includes `reporting-scenarios.sql` with five queries: totals, overpayments, duplicate fact keys, per-date fact/report mismatches and missing product references.

To inspect those queries against the integrated fixture, run commands separately:

```text
python seed_source.py
python run_incremental.py
```

The first integrated run intentionally returns exit 2 while committing two data-quality rejects. Create `inspect_scenarios.py` in the same extracted folder:

```python
from pathlib import Path
import sqlite3

queries = Path('reporting-scenarios.sql').read_text(encoding='utf-8-sig').split(';')
connection = sqlite3.connect('warehouse.sqlite')
try:
    for query in queries:
        if query.strip():
            print(connection.execute(query).fetchall())
finally:
    connection.close()
```

Run `python inspect_scenarios.py` from that folder. Expected output: first `[(33000, 20000, 13000)]`, then four empty lists. Empty lists mean those particular exception queries found no offending rows in this fixture, not that every possible data problem is absent.

Run `python check_reporting_scenarios.py` for automatic verification. It builds disposable data, checks the reference answers, then deliberately introduces an overpayment, a missing report date, incorrect per-date allocation with an unchanged grand total, and a missing product reference. It does not change your learning database. The duplicate-key query returns empty because the fact's primary key enforces uniqueness.

## Session complete: retain the reasoning

A useful reporting model has a clear row grain, agreed measures, controlled joins, explicit missing-value rules and visible exceptions. Reconcile across layers and check source completeness/freshness separately. Correct confirmed errors through traceable rules and prevent recurrence based on the root cause.

You can now continue independently with [Incremental Extraction](incremental-extraction.md), [Scheduling and Logs](scheduling-and-observability.md), [Recovery](recovery-and-runbook.md), and the [Capstone](capstone-and-assessment.md); those modules and their worked commands are already published.
