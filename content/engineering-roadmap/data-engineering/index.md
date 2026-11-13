# Data Engineering with AI Assistance

**Level: Beginner | Learning draft | Independent review pending**

Learn how business data becomes reliable information. Build pipelines step by step, using AI to explain, review and troubleshoot your work. No prior Data Engineering experience, paid cloud service or AI subscription is required. AI is optional: every exercise can be completed without it.

## Start here

| Step | Lesson | What you produce |
| --- | --- | --- |
| 1 | [Understand the role](understand-the-role.md) | A data journey and a clear business definition |
| 2 | [Workspace and free learning tools](workspace-and-free-tools.md) | A working Python/SQLite lab |
| 3 | [Meet the canteen data](canteen-data.md) | A data dictionary and predictions |
| 4 | [First SQL lab](first-sql-lab.md) | Five queries with checked business answers |
| 5 | [Answers and explanations](sql-solutions.md) | An explanation of a payment mismatch and join error |
| 6 | [Python for pipelines](python-for-pipelines.md) | CSV reading, conversion and validation functions |
| 7 | [Persistent Python pipeline lab](python-pipeline-lab.md) | Validated loads, quarantine, safe replay and failure checks |
| 8 | [Corrections and late-arriving data](corrections-and-late-data.md) | Retained version history and a latest-state report |
| 9 | [Reporting models and reconciliation](reporting-models-and-reconciliation.md) | Order-grain facts and checked daily totals |
| 9a | [Reporting worked scenarios and answers](reporting-worked-scenarios.md) | Sixteen explained cases with SQL and automatic checks |
| 10 | [Incremental extraction and checkpoints](incremental-extraction.md) | Bounded source batches and atomic progress |
| 11 | [Scheduling and observability](scheduling-and-observability.md) | Interpretable exit codes, logs and optional local scheduling |
| 12 | [Recovery and runbook](recovery-and-runbook.md) | Failure/retry and a verified backup/restore exercise |
| 13 | [Capstone and assessment](capstone-and-assessment.md) | Reproducible evidence and a learning portfolio |

[Download the complete starter kit](../../../downloads/canteen-starter.zip): synthetic CSVs, Python loader, SQL solutions, README and checks. [Browse the source](../../../examples/canteen-starter/README.md).

## Your first week: two hours a day

Use 25 minutes to study, 60 to practise, 20 to check and 15 to explain what you learned.

1. Read the role lesson; draw the order-to-report journey.
2. Set up the workspace and run the starter. Learn SELECT and WHERE.
3. Read the dictionary. Predict totals manually before querying.
4. Attempt questions 1 and 2; learn COUNT, SUM and GROUP BY.
5. Attempt question 3; learn JOIN and distinguish units from orders.
6. Attempt questions 4 and 5; explain settled versus pending payments.
7. Rerun the lab, complete the checks and explain the result to another learner.

If you are new to programming, repeat the setup and fundamentals days. Completion is evidence of practice, not a job-readiness certificate.

## Use AI to support understanding

Ask: “Explain one concept using these synthetic rows, then ask me to predict the answer. Give hints before code.” For review: “What assumptions does my query make about one row? Give a counterexample.” Verify by running queries and checking totals manually. Do not paste private student, employer or customer data, credentials or connection strings into an AI service.

## Complete the beginner pathway

The planned beginner lessons are now available through the capstone. The SQL lab, immutable pipeline, version-history lab and integrated workflow intentionally use different databases and demonstrate different policies. Follow each lesson's setup and expected totals. See the [capstone](capstone-and-assessment.md) for a flexible 12-week plan at two hours a day.

The integrated workflow uses synthetic source events and fixed payment/product references. It is not a production pipeline, professional certification or guarantee of employment. Independent technical review remains pending. API, PostgreSQL, cloud and distributed-system extensions are optional future work, not required to complete this starter.

[AI and data career pathways](../03-the-ai-impact/index.md) · [Feedback](../../feedback.md)
