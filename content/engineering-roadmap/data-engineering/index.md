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

Later lessons will cover Python validation, persistent reruns, incremental loads, modelling, scheduling, logs and recovery. These are planned topics, not completed modules. The current loader intentionally rebuilds an in-memory database; it is not a production pipeline.

[AI and data career pathways](../03-the-ai-impact/index.md) · [Feedback](../../feedback.md)
