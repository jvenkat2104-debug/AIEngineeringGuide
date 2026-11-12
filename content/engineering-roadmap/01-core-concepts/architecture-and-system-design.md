# Architecture and system design

**Level: Intermediate** · Start with the Year 1 roadmap if these ideas are unfamiliar.

Status: Draft | Independent review pending

**Architecture** describes the main parts of a system and their connections. **System design** includes the reasoning about capacity, reliability, cost, safety and failures that makes the arrangement suitable for its purpose. The terms overlap in practice.

| Path | A useful architecture drawing |
| --- | --- |
| CSE/AI | App, service, model and database with request arrows |
| ECE | Processor, memory, sensors, power and communication blocks |
| EE | Source, transformer, distribution and load diagram |
| Mechanical | Components, motion, force and heat-flow paths |
| Civil | Structures, drainage or transport components and their dependencies |
| Mathematics and Computing | Inputs, algorithm, checks and outputs |
| Quantum-related study | Control electronics, quantum operations and classical processing |

## Work through a design

For a college canteen ordering service, estimate users, busy periods and acceptable waiting time. Decide what must still work when the network is unavailable. Identify how orders are stored and how duplicates are detected.

| Choice | Benefit | Cost or limitation |
| --- | --- | --- |
| One simple service | Easier to understand and operate initially | A failure can affect several functions |
| Separate services | Parts can evolve independently | More network and operational complexity |
| Cache menu data | Faster repeated reads | Prices or availability can become stale |

These are illustrative trade-offs, not a recommendation to use a particular architecture.

## Explain your design

Name the requirements, draw the components, state assumptions, walk through a normal request and a failure, and identify what you would test first.

---
Source basis: Campus to Corporate blueprint, Version 4. Adapted for this guide; additions and pathway suggestions require review.
