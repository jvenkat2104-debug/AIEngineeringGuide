# A practical development workflow

**Level: Intermediate** · Start with the Year 1 roadmap if these ideas are unfamiliar.

Status: Draft | Independent review pending

1. Define the problem, expected inputs and limits before coding.
2. Break it into a small change that you can check.
3. Use documentation and optional AI assistance for explanations or drafts.
4. Read and understand every accepted change.
5. Test normal inputs, invalid inputs and important failure cases.
6. Run a small deployment or demonstration, observe it and fix what you learn.
7. Record decisions and instructions so someone else can reproduce the work.

## Example: adding a sensor reading

Specify the unit and acceptable range. Decide how missing readings appear. Test an ordinary reading, a malformed value and a disconnected sensor. Explain whether a displayed value is current or cached.

## Before calling it finished

- Can another person run or reproduce the result?
- Are credentials kept out of the repository?
- Do error messages help diagnose a failure?
- Can you explain why the chosen design fits the constraints?
- Have you distinguished measured behaviour from untested assumptions?


## Record your working environment

Document tools and dependencies you actually tested. Use the [environment checklist](../../shared/project-environments.md), including the dated Python security guidance checked on 12 November 2026.

---
Source basis: Campus to Corporate blueprint, Version 4. Adapted for this guide; additions and pathway suggestions require review.
