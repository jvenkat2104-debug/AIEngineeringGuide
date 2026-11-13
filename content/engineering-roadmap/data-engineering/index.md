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

## What comes next

The SQL starter rebuilds an in-memory database. The new Python pipeline lesson stores orders persistently and demonstrates validation, replay and transaction rollback. Continue with those lessons over several sessions; the next published session adds source-versioned corrections and late data. Later modules will cover incremental source extraction, modelling, scheduling, logging and operational recovery; those remain planned. None of these learning loaders is a production pipeline.

[AI and data career pathways](../03-the-ai-impact/index.md) · [Feedback](../../feedback.md)
