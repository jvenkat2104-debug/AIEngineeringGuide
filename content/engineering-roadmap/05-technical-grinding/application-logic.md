# Practical tools: Git, APIs and data formats

**Level: Intermediate** · Start with the Year 1 roadmap if these ideas are unfamiliar.

Status: Draft | Independent review pending

These tools are especially relevant to software and connected-device projects. They are not universal hiring requirements for every engineering role.

## Git: record and discuss changes

A commit records a meaningful change. A branch lets you develop work separately. A pull request proposes a change for review. Start with a small repository, edit a README, commit it, then use a branch for a second change. Read a diff before accepting it.

## APIs: request data or an action

An API defines how programs interact. For a web API, identify the endpoint, method, inputs, response and error conditions. Practise with public sample data. Handle unsuccessful responses and rate limits; do not assume every response is successful JSON.

## JSON and CSV: exchange data

JSON can represent named fields and nested structures. CSV represents rows and columns, with quoting rules for separators inside values. Validate field names, units and types before using a record.

## Exercise

Create a small invented sensor dataset with timestamp, device identifier, value and unit. Store it as CSV and JSON. Explain a missing value and an invalid value. Commit the data and an explanation of the format. Never use real personal or confidential records for a public exercise.

---
Source basis: Campus to Corporate blueprint, Version 4. Adapted for this guide; additions and pathway suggestions require review.
