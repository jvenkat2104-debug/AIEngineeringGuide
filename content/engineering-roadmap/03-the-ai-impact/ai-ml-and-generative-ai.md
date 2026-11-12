# AI, ML and generative AI: what is the difference?

Audience: engineering students exploring software and data pathways
Status: Draft | Independent review pending
Last updated / sources checked: 12 November 2026

## Start with the problem

The canteen wants to reduce shortages and waste. Several approaches could help: a stock rule, a summary report, a demand prediction or a document-search assistant. They solve different problems.

| Idea | Plain-language meaning | Canteen example | What to check |
| --- | --- | --- | --- |
| Rule-based software | Humans specify the decision logic | Flag stock below a fixed threshold | Whether the rule matches the situation |
| Artificial intelligence | A broad field concerned with capabilities such as reasoning, perception and language | A system interpreting a question or recognising an item | Which capability it actually provides |
| Machine learning | Models learn patterns from examples | Estimate tomorrow’s demand from historical records | Performance on unseen, relevant data |
| Generative AI | Models produce content such as text or images | Draft a menu description | Accuracy, appropriateness and permissions |
| Retrieval | Find stored information relevant to a query | Locate an approved refund-policy paragraph | Relevance, freshness and access rights |
| Retrieval-augmented generation (RAG) | Supply retrieved material as context to a generator | Answer a policy question using approved canteen documents | Grounding, citations and unsupported answers |

AI and ML overlap; not every AI approach is ML, and using an existing model is different from training one.

## Training, inference and prompting

**Training** adjusts learned parameters using data. **Inference** uses the resulting model on an input. **Prompting** supplies instructions or context to an existing model. **Fine-tuning** further trains a model; it is not the same as adding documents to a retrieval index.

A prompt asking “How many meals tomorrow?” does not turn a general chatbot into a validated demand forecaster. Choose a measurable target and compare a simple baseline first.

## Prediction needs evaluation

A feature is an input, such as day of week. A label or target is the outcome being predicted, such as meals sold. Use only information available at prediction time. Tomorrow’s final sales cannot be an input to tomorrow morning’s forecast.

Separate training and evaluation data. For a time-dependent forecast, use earlier periods to develop the model and later periods to evaluate it. Keep a final test period out of model-selection decisions. Small synthetic datasets teach mechanics; they do not prove real-world performance.

## Try it

Classify these requests as rules, reporting, prediction or generation: “What sold yesterday?”, “Warn when rice is low”, “Estimate tomorrow’s demand”, “Write a menu summary”. Explain a failure mode for each. Describe which task needs a model at all.

## Sources and further study

[Google Machine Learning Crash Course](https://developers.google.com/machine-learning/crash-course) is a starting source for prediction, data preparation and model evaluation; check its prerequisites. This chapter’s canteen scenarios are editorial examples.

[Back to AI, Data and Career Pathways](index.md)
