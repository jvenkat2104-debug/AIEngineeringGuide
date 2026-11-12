# Data Engineering and data integration

**Level: Intermediate** · Start with the Year 1 roadmap if these ideas are unfamiliar.

Audience: engineering students exploring software and data pathways
Status: Draft | Independent review pending
Last updated / sources checked: 12 November 2026

**Data integration** brings information from different sources into a usable relationship. **Data Engineering** builds and operates the pipelines, storage and quality controls that make that information dependable. A pipeline is a sequence of processing steps, not necessarily one specific product.

## Follow the canteen records

The till exports sales CSV files, the menu service returns JSON, and a calendar records closure days. Their identifiers and meanings must agree before a report or model can use them.

| Concept | Meaning | Canteen decision |
| --- | --- | --- |
| Ingestion | Bring records into the system | Import yesterday’s till file |
| Schema | Expected fields, types and constraints | Quantity is an integer; currency is explicit |
| Mapping | Match source fields to target meanings | Map `item_code` to `menu_item_id` using an approved table |
| ETL | Extract, transform, then load | Clean records before loading curated tables |
| ELT | Extract, load, then transform in the destination | Store permitted source data, then build cleaned tables |
| Batch | Process a collection at intervals | Produce a daily summary |
| Streaming | Process an ongoing flow | Update an operational view as events arrive |
| Orchestration | Coordinate steps and dependencies | Summarise only after imports and checks finish |
| Lineage | Record where data came from and how it changed | Trace a forecast input to source files and transformations |

Neither ETL nor ELT is universally better. Privacy, destination capabilities, costs and required transformations influence the choice. The [Microsoft ETL/ELT explanation](https://learn.microsoft.com/en-us/azure/architecture/data-guide/relational-data/etl) provides background.

## Define meaning before joining tables

Write each table’s **grain**: what one row represents. A sale line is not the same as one customer or one day. Joining it to a duplicated menu record can multiply quantities even if the query runs successfully.

Decide how to represent refunds, closures, late files and absent records. No file is not evidence of zero sales. Preserve source data only where authorised, and keep customer identifiers out of this student exercise.

## Reliability checks

- Validate required fields, units and identifier mappings.
- Detect duplicate business keys and unknown menu items.
- Reconcile input, accepted and rejected record counts.
- Make reruns **idempotent**: processing the same source again should not duplicate its effects.
- Quarantine invalid records with a reason; do not silently discard them.
- Record freshness, source version and pipeline failures.

## Try it

Create two tiny sales files with a repeated record, a missing identifier and different date formats. Write the expected cleaned rows before implementing anything. Explain what happens when the same file is imported twice and when a corrected version arrives.

A model consuming incorrect joins or stale records can produce convincing but misleading output. Data reliability remains necessary whether or not the downstream system uses AI.

[Back to AI, Data and Career Pathways](index.md)
