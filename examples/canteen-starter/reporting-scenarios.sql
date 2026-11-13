-- 1. Report totals, in paise. Expected: 33000, 20000, 13000.
SELECT SUM(ordered_paise),SUM(settled_paise),SUM(outstanding_paise) FROM fact_orders;
-- 2. Overpaid orders. Expected: no rows in the supplied fixture.
SELECT order_id,ordered_paise,settled_paise,outstanding_paise FROM fact_orders WHERE outstanding_paise<0 ORDER BY order_id;
-- 3. Duplicate reporting keys. Expected: no rows.
SELECT order_id,COUNT(*) FROM fact_orders GROUP BY order_id HAVING COUNT(*)>1;
-- 4. Per-date fact/report mismatches, including a date missing on either side.
WITH facts AS (
 SELECT order_date,COUNT(*) AS orders,SUM(ordered_paise) AS ordered,
 SUM(settled_paise) AS settled,SUM(outstanding_paise) AS outstanding
 FROM fact_orders GROUP BY order_date
), dates AS (
 SELECT order_date FROM facts UNION SELECT order_date FROM daily_report
)
SELECT d.order_date,f.ordered AS fact_ordered,r.ordered_paise AS report_ordered
FROM dates d LEFT JOIN facts f ON f.order_date=d.order_date
LEFT JOIN daily_report r ON r.order_date=d.order_date
WHERE f.order_date IS NULL OR r.order_date IS NULL
 OR f.orders<>r.orders OR f.ordered<>r.ordered_paise
 OR f.settled<>r.settled_paise OR f.outstanding<>r.outstanding_paise
ORDER BY d.order_date;
-- 5. Orders missing a product dimension. Expected: no rows.
SELECT f.order_id FROM fact_orders f LEFT JOIN dim_products p ON p.product_id=f.product_id WHERE p.product_id IS NULL ORDER BY f.order_id;
