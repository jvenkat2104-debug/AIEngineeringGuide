# SQL solutions and explanations

**Level: Beginner | Learning draft | Independent review pending**

Attempt the [SQL lab](first-sql-lab.md) before reading. Executable reference answers are in `solutions.sql` in the [starter ZIP](../../../downloads/canteen-starter.zip). Run `python check_lab.py` to verify reference results, a join-fan-out example and duplicate-key rejection.

## 1. Order count and ordered value

```sql
SELECT COUNT(*), SUM(quantity * unit_price_paise) FROM orders;
```

Result: 5 and 24000. There is exactly one row per order in this simplified model. In an order-items model, COUNT(*) would count items, so that definition must change.

## 2. Daily ordered value

```sql
SELECT order_date, SUM(quantity * unit_price_paise)
FROM orders GROUP BY order_date ORDER BY order_date;
```

Results: 2026-11-01 → 9000; 2026-11-02 → 15000. Grouping combines rows with the same date.

## 3. Product units

```sql
SELECT p.product_name, SUM(o.quantity)
FROM orders o JOIN products p ON o.product_id = p.product_id
GROUP BY p.product_id, p.product_name
ORDER BY SUM(o.quantity) DESC, p.product_name;
```

Results: Idli 3, Meal 3, Tea and snack 1. Product ID is the join key. The second sort field makes ties deterministic.

## 4. Settled collections

```sql
SELECT SUM(amount_paise) FROM payments WHERE status = 'settled';
```

Result: 20000. The pending 4000 is excluded. Collections do not subtract operating expenses.

## 5. Outstanding orders

```sql
WITH settled AS (
  SELECT order_id, SUM(amount_paise) AS paid
  FROM payments WHERE status = 'settled' GROUP BY order_id
)
SELECT o.order_id, o.quantity * o.unit_price_paise AS ordered,
       COALESCE(s.paid, 0) AS paid,
       o.quantity * o.unit_price_paise - COALESCE(s.paid, 0) AS outstanding
FROM orders o LEFT JOIN settled s ON o.order_id = s.order_id
WHERE o.quantity * o.unit_price_paise <> COALESCE(s.paid, 0)
ORDER BY o.order_id;
```

Result: O4, 10000 ordered, 6000 paid, 4000 outstanding. This also detects overpayment as a negative difference; resolving one requires a business rule. Aggregating payments first makes the join at most one settled-total row per order. LEFT JOIN keeps an order with no payment.

## Explain before moving on

Why is SUM(DISTINCT order value) unreliable? O2 and another different order could share a value; DISTINCT would incorrectly collapse them. Deduplicate using business keys and source rules, not coincidentally equal amounts.

The loader rebuilds the database in memory. A future persistent pipeline needs explicit rules for retries, corrected records and incremental processing. Do not describe this starter as production-ready or as a complete Data Engineering course.

[Return to pathway](index.md) · [Report a correction](../../feedback.md)

Next: [Python for pipelines](python-for-pipelines.md), then [the persistent pipeline lab](python-pipeline-lab.md).
