# What does a Data Engineer do?

**Level: Beginner | Learning draft | Independent review pending**

Goal: explain how a business event reaches a useful report, and identify where reliability can fail. Prerequisite: none. Allow one two-hour session.

## Begin with a business question

A canteen manager asks: “How much money did we collect yesterday?” An order log says what was ordered; a payment log says what was paid and whether it settled. Adding all order values does not answer the collections question. A Data Engineer helps establish these definitions before building a repeatable data flow.

A typical journey is: order/payment system → ingestion → stored source records → validation and transformation → reporting tables → analyst or application. Each arrow can fail or deliver data late.

## Responsibilities and collaborators

A Data Engineer gathers data, models relationships, checks quality, schedules processing and investigates failures. Analysts help define measures; application engineers explain source behaviour; business owners approve meanings and acceptable delays. Platform/security teams help manage access and operations. In smaller teams these responsibilities overlap; job titles vary.

A normal work session might involve investigating a missing daily file, checking a changed source column, correcting a transformation, validating totals and explaining a delay to a report owner. Writing a query is one part of the work.

## Four questions before tools

- **Grain:** what does one row represent—an order, order item or payment attempt?
- **Key:** how do we identify the same business record on a retry?
- **Freshness:** when must the report be ready, and what happens to late records?
- **Quality:** which conditions make a record unusable, and who resolves them?

## Worked example

Order O4 is worth INR 100. Its payment rows show INR 60 settled and INR 40 pending. Ordered value is INR 100, settled collections INR 60, outstanding INR 40. Calling the full INR 100 “cash collected” would mislead the manager. The lab uses this distinction, without attempting formal revenue recognition or profit accounting.

## Exercise and completion checks

Draw the journey above and label an owner and one possible failure at each stage. Write a definition of settled collections, including which payment statuses count. Explain what happens if yesterday’s payment arrives today. There is no single architecture answer; a useful answer makes ownership, timing and assumptions explicit.

Common mistakes: choosing a large tool stack before defining the question, treating all payment attempts as collected money, and assuming AI-generated code establishes business correctness.

AI prompt: “Act as a canteen manager. Ask me five questions that expose ambiguity in my daily collections definition; do not choose the answers for me.”

Source context: this is an illustrative role scenario. For implementation details use the [Python SQLite reference](https://docs.python.org/3/library/sqlite3.html); organisation-specific responsibilities vary.

Next: [Set up your workspace](workspace-and-free-tools.md).
