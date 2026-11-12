# Student learning paths for AI and data

Audience: engineering students exploring software and data pathways
Status: Draft | Independent review pending
Last updated / sources checked: 12 November 2026

Start with common foundations, then choose one direction. This is a suggested sequence with evidence milestones, not a fixed course length or hiring guarantee.

## Common foundation

Learn one programming language, basic SQL, data formats, Git and testing. Practise [DSA](../01-core-concepts/data-structures-and-algorithms.md), and strengthen probability, statistics and linear algebra as needed for modelling. Explain missing data, units and the meaning of a row before training a model.

| Stage | Work to do | Evidence before moving on |
| --- | --- | --- |
| Year 1 | Programming, arrays/strings, small tables and clear explanations | A small program and a report you can reproduce |
| Year 2 | SQL joins, data modelling, ingestion and validation; introductory ML after prerequisites | A rerunnable pipeline and a baseline evaluated correctly |
| Year 3 | Choose data, model, application or operations depth | A substantial project with failure tests and feedback |
| Year 4 | Refine the capstone and match actual next-step requirements | Design walkthrough, results, limitations and tailored applications |

Students starting later can revisit earlier material. Shared computers and local tools are sufficient for the basic project; no paid certification is required by this guide.

## Choose a track after the common foundation

**Data/integration:** focus on SQL, schema meaning, APIs/files, idempotent loads, quality and orchestration. Add distributed processing only when the data or role requires it. Show a duplicate-safe rerun and trace an incorrect report to its source.

**ML:** focus on a measurable target, a simple baseline, suitable splits, metrics and reproducibility. Add more complex models only after explaining why the baseline is insufficient. Show an honest negative result if the model does not improve it.

**AI application:** build a narrowly scoped user workflow with source-grounded answers where applicable. Keep an evaluation set and test unsupported requests, access boundaries and failures. Prompting complements software engineering.

**MLOps:** begin with a working pipeline/model; automate checks, record artifacts, expose a local inference path and demonstrate rollback. Learn containers/cloud when justified; a complex cluster is not the starting milestone.

## A small project progression

Complete one stage of the [canteen project](canteen-data-to-ai-project.md), get feedback, and extend it. Keep the same dataset definitions so you can explain what changed. Never invent model scores or claim deployment experience from a diagram alone.

## Review your readiness

Can you explain every component, reproduce the result, identify a realistic failure and match your evidence to a role’s requirements? Use [job-market evidence](job-market-snapshot.md) to refine the plan, not to infer that every advertised tool is mandatory.

## Learning references

Use [Google’s ML Crash Course](https://developers.google.com/machine-learning/crash-course), [Microsoft’s ETL/ELT explanation](https://learn.microsoft.com/en-us/azure/architecture/data-guide/relational-data/etl) and the [MLOps architecture reference](https://cloud.google.com/architecture/mlops-continuous-delivery-and-automation-pipelines-in-machine-learning) at the relevant stage. These are optional references, not endorsements of a required platform purchase.

[Back to AI, Data and Career Pathways](index.md)
