# First SQL lab: orders and collections

**Level: Beginner | Learning draft | Independent review pending**

Goal: answer five business questions and explain why ordered value differs from collected money. Prerequisites: [workspace](workspace-and-free-tools.md), [dictionary](canteen-data.md), and basic SELECT. Allow two to three sessions; take SQLBolt's filtering, joins and aggregate lessons if needed.

## First query, explained

Run `python lab.py`. The starter query is:

```sql
SELECT order_id, quantity * unit_price_paise AS order_value_paise
FROM orders
ORDER BY order_id;
```

SELECT chooses output expressions, FROM chooses the table, AS names a calculated field and ORDER BY gives a predictable display order. O1 returns 4000 paise: 2 × 2000. Predict each row before running it.

## Your five tasks

Replace the query string in `lab.py`, save and rerun. Use SQLite SQL. Keep values in paise until presentation.

| Question | Hint | Check your result |
| --- | --- | --- |
| 1. How many orders and how much ordered value? | COUNT and SUM, no payment join | 5 orders; 24000 paise (INR 240) |
| 2. What is ordered value per date? | GROUP BY order_date | Nov 1: 9000; Nov 2: 15000 paise |
| 3. How many units of each product were ordered? | JOIN products; SUM quantity, not COUNT rows | Idli 3; Meal 3; Tea and snack 1 |
| 4. How much payment has settled? | Filter status before summing | 20000 paise (INR 200) |
| 5. Which orders are not fully settled? | Sum settled payments per order first; LEFT JOIN; COALESCE missing sums to zero | O4: ordered 10000, paid 6000, outstanding 4000 paise |

For question 5, a CTE (`WITH`) gives a name to a query result. Aggregate payments there before joining orders. Otherwise the many-side can multiply rows. COALESCE turns a missing payment total into zero so arithmetic does not become NULL.

## Investigate a convincing wrong answer

```sql
SELECT SUM(o.quantity * o.unit_price_paise)
FROM orders o JOIN payments p ON o.order_id = p.order_id;
```

This returns 34000 paise. Do not “fix” it with SUM(DISTINCT order value): different orders can have the same value. Explain which order is counted twice and how table grain causes it.

## Use AI for hints, then prove the result

“Here is my query and the dictionary. Do not solve it immediately. Identify its assumed row grain and give one hint about overcounting.” After revising, run the query and reconcile to the expected totals. AI agreement alone is not a check.

## Completion checklist

- Save all five queries and explain each in plain language.
- Show why 24000 ordered and 20000 settled are both correct under different definitions.
- Explain why an unmatched order needs a LEFT JOIN and zero default.
- Run `python check_lab.py`; expect PASS. This verifies supplied reference queries, not your edited query—compare your own answers too.
- Re-run `python lab.py`; explain why the fresh in-memory database avoids accumulation but does not demonstrate persistent safe reruns.

Try a stretch task: temporarily omit O5's payment in a working copy of the CSV. Question 5 should then include O5 outstanding 3000 as well as O4. Restore the original file afterwards; reference checks assume the supplied data.

After attempting: [Solutions and explanations](sql-solutions.md).
