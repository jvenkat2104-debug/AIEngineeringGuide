# MLOps: operating a model beyond the notebook

Audience: engineering students exploring software and data pathways
Status: Draft | Independent review pending
Last updated / sources checked: 12 November 2026

**MLOps** applies engineering and operational practices to the model lifecycle: developing, validating, releasing, observing and updating models and the surrounding system. It is a set of responsibilities, not a single certification or deployment tool.

A canteen notebook that predicts one number is different from a service staff depend on daily. The operational system needs predictable data, a versioned model, checks and a recovery plan.

## What changes after the first demonstration?

| Responsibility | A useful student implementation |
| --- | --- |
| Reproducibility | Record data, transformation, model and environment versions |
| Evaluation | Compare with a baseline on a later held-out period |
| Release gate | Accept a candidate only if defined checks pass |
| Deployment | Load a known model version in a batch job or service |
| Monitoring | Observe data freshness, errors, latency and output quality |
| Recovery | Retain the previous working version and a tested fallback |
| Ownership | State who investigates a failure and how decisions are recorded |

**CI** means integrating changes with automated checks. **CD** concerns preparing or delivering changes to a running system. Model retraining is another activity: it should not automatically publish a model merely because training completed.

The [Google Cloud MLOps overview](https://cloud.google.com/architecture/mlops-continuous-delivery-and-automation-pipelines-in-machine-learning) explains how automation extends across data and model pipelines. Read its architecture as an advanced reference, not a requirement to buy cloud services.

## Monitor the right thing

A service can return a response successfully while predictions worsen. Input **drift** means input distributions changed; it is a signal to investigate, not proof the model is wrong. Measuring prediction error requires actual outcomes, which may arrive later.

In the canteen example, distinguish a missing sales file, a new menu pattern, a software timeout and increased forecast error. Their remedies differ. Keep a simple fallback and label its age and limitations rather than silently presenting stale output as current.

## MLOps, DevOps and LLMOps

DevOps practices connect software development and operations. MLOps adds model/data lifecycle concerns. “LLMOps” is used for operational work around language-model applications, including prompt/model versions, retrieval changes, evaluations, access rules and costs. Boundaries vary across teams.

An API wrapper alone is not an operationally reliable AI product. Do not begin by collecting infrastructure tools; start by reproducing one result and recovering from one failure.

## Exercise

Design a release record with dataset version, model version, evaluation period, metrics, approval and fallback. Describe what you would do if the new model fails a check or yesterday’s data never arrives. This is a design exercise; it does not claim any model has been trained or deployed.

[Back to AI, Data and Career Pathways](index.md)
