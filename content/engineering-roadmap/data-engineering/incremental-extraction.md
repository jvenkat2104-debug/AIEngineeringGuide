# Incremental Extraction and Checkpoints

**Level: Beginner, after reporting models | Learning draft | Independent review pending**

Goal: read new source events in bounded batches and advance a checkpoint only with committed target changes. Allow two two-hour sessions. The example simulates an append-only source in SQLite; it is not a commercial database CDC connector.

## Two sequences with different meanings

`source_seq` is a unique, increasing position in one append-only source event stream. `source_version` orders full snapshots of one business order. `order_date` is the date used in a business report. None of these is interchangeable.

A new event with sequence 12 can describe an order from October. Filtering on the latest business date would miss it; reading source sequence greater than the saved checkpoint includes it. This depends on the source contract: committed events must become visible in increasing sequence order, and old events must not be edited, deleted or inserted below the consumed position. Real sources may need timestamps plus tie-breakers, overlap windows, log offsets or a specialised connector instead.

## How this local example works

`seed_source.py` creates `source.sqlite` with a source identity and 11 synthetic events from `order-changes.csv`. Rerunning the seed does not append duplicate events. It is a fixture creator, not a continuously changing business system.

`run_incremental.py` reads the next bounded batch, validates snapshots, rebuilds the small reporting models and saves the highest consumed source sequence. History, quarantine, reports and checkpoint commit in one target transaction. On a failure before commit, all those batch changes roll back. Source identity is saved with the checkpoint; replacing the source with a different identity stops the runner rather than silently skipping data.

## Exercise: process three batches

Use a new target filename for this exercise; do not reuse your previous warehouse and expect first-run counts:

```text
python seed_source.py
python run_incremental.py --db batches.sqlite --batch-size 4
python run_incremental.py --db batches.sqlite --batch-size 4
python run_incremental.py --db batches.sqlite --batch-size 4
python run_incremental.py --db batches.sqlite --batch-size 4
```

| Run | Extracted | Saved checkpoint | Remaining source events | Expected outcome |
| --- | --- | --- | --- | --- |
| 1 | 4 | 4 | 7 | Partial current data; exit 0 |
| 2 | 4 | 8 | 3 | Corrections and late O6 applied; report reaches 33000 paise; exit 0 |
| 3 | 3 | 11 | 0 | Two rejects, one replay; exit 2, committed |
| 4 | 0 | 11 | 0 | No new orders; report refreshed; exit 0 |

No new events is not evidence that the business had no activity. The source could be stalled. `pending` is an observation after target commit and may change if the source changes afterwards. A successful run with checkpoint 8 can still produce an incomplete report because more events remain.

## Rejected rows and progress

This exercise commits the quarantine decision and advances past rejected events. That prevents a known bad row from blocking all later work. It also creates a responsibility: someone must review unresolved quarantine and obtain corrected source events with appropriate versions and new sequence positions. Do not simply move the checkpoint backwards to “fix” a business conflict.

The quarantine key uses generated batch-file bytes and record position, inherited from the prior lab. Replaying exactly the same batch is stable, but changing batch boundaries or re-extracting different batches may create additional audit rows. This is not a complete event-receipt ledger. A production design should use stable source event IDs for audit deduplication.

## Exercises and completion

1. Explain why neither `MAX(order_date)` nor source version is the extraction checkpoint.
2. Read the `checkpoint` row and compare it with remaining source events.
3. Predict what must happen if the report rebuild fails after version history was inserted.
4. Run `python check_operations.py`. It appends an older-business-date order at a new source sequence in a disposable fixture and verifies that it is extracted.

AI prompt: “Challenge my assumption that a source sequence is safe. What if transactions become visible out of sequence, the source resets, or records are deleted?” Write which assumptions this synthetic source guarantees and which a real source must prove.

The runner reads one batch into memory and holds a short local writer lock. It is not a distributed exactly-once guarantee, snapshot-consistent multi-source ingestion or a schema migration framework. Standard-library mechanics: [Python SQLite transactions and parameters](https://docs.python.org/3/library/sqlite3.html), checked 13 November 2026.

Next: [Scheduling and observability](scheduling-and-observability.md).
