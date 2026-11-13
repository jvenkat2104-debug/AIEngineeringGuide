# Capstone: Explain and Operate the Canteen Pipeline

**Level: Beginner capstone | Learning draft | Independent review pending**

Goal: demonstrate the complete local learning workflow and explain its limits. Budget several two-hour sessions. Finish the earlier labs before treating this as an assessment; this is not a certification or employment guarantee.

## The brief

A canteen manager needs daily ordered value, settled payments and outstanding amounts. Orders can be corrected, delivered late or repeated. You must retain history, stop old snapshots reversing corrections, report rejected records and recover from a failed batch.

Use only the supplied synthetic data. Download the current [starter kit](../../../downloads/canteen-starter.zip) into a new folder. Keep your previous experiment files separate.

## Demonstrate the flow

```text
python seed_source.py
python run_incremental.py
python run_incremental.py
python check_lab.py
python check_pipeline.py
python check_versions.py
python check_operations.py
```

Run commands individually: the first incremental run intentionally returns exit 2 after committing two data-quality rejects; the replay returns 0. All four check scripts should print PASS. The final report has six current orders, ordered value 33000 paise, settled amount 20000 and outstanding 13000. Do not confuse the earlier immutable pipeline's 28000 total with the corrected versioned workflow's 33000 total.

## Your deliverables

| Evidence | What another learner should be able to assess |
| --- | --- |
| One-page business/data contract | Definitions, row grain, keys, source ordering, full snapshots and correction policy |
| Small data-flow diagram | Source → extraction → version history/current view → order fact → daily report; checkpoint boundary |
| Saved SQL and output | Per-day/product totals, quarantine reasons and reconciliation |
| Failure/recovery demonstration | Checkpoint before failure, unchanged target after rollback, successful retry |
| Backup/restore record | A separate restored database with integrity, checkpoint and business totals checked |
| Reproducible README | Python command, files, expected exit codes, how to rerun and limitations |
| AI-use reflection | One helpful suggestion, one suggestion you verified/rejected and the evidence used |

Do not publish local databases, logs containing private data or real student/customer records. If sharing your work in GitHub, include source and synthetic fixtures, with appropriate attribution and licences; exclude generated local outputs. The portal's [contribution instructions](../../contribute.md) explain how to propose improvements. Do not present an AI review as independent expert sign-off.

## Explain these without reading the solution

1. Why can ordered value differ from settled collections?
2. What goes wrong when a one-to-many join repeats order values?
3. Why is source version different from extraction sequence and business date?
4. When can a replay be ignored, and when must a conflict be investigated?
5. Which writes must commit together with the checkpoint?
6. How can a successful no-op run coexist with missing or stale source data?
7. What does the reconciliation prove, and what does it fail to prove?
8. Why is a tested restore stronger evidence than an existing backup file?

A strong answer names a concrete example from the fixture and a counterexample where the rule would fail. If you cannot explain a step, return to its lesson and simplify the example.

## Suggested learning pace

| Learning block | Suggested focus |
| --- | --- |
| Weeks 1–2 | Role, setup, SQL and business definitions |
| Weeks 3–4 | Python, validation and persistent replay |
| Weeks 5–6 | Corrections, late data and modelling |
| Weeks 7–8 | Incremental batches and transactional checkpoints |
| Weeks 9–10 | Logs, optional scheduling and recovery drills |
| Weeks 11–12 | Capstone, peer feedback and revision |

This is flexible pacing at roughly two hours a day, not a deadline. Share one tested lesson or explanation per week. A senior learner can move faster while still doing the beginner exercises.

## What completing this does and does not mean

You have a coherent introduction to role responsibilities, SQL/Python, ingestion, validation, source versions, models, reconciliation, incremental checkpoints and local operations. These planned beginner modules are now available. Expert content review remains pending.

Further extensions can add PostgreSQL, API ingestion, automated transformations, cloud storage, orchestration, schema evolution, security, data lineage and distributed processing. They are outside this completed starter, not skills automatically acquired by running it. Choose one extension based on a concrete requirement; no paid service is required to finish this pathway.

[Return to pathway](index.md) · [Feedback](../../feedback.md)
