-- Q1: order count and total ordered value (paise)
SELECT COUNT(*), SUM(quantity * unit_price_paise) FROM orders;
-- Q2: daily ordered value
SELECT order_date, SUM(quantity * unit_price_paise) FROM orders GROUP BY order_date ORDER BY order_date;
-- Q3: units per product, not number of order rows
SELECT p.product_name, SUM(o.quantity) FROM orders o JOIN products p ON o.product_id=p.product_id GROUP BY p.product_id,p.product_name ORDER BY SUM(o.quantity) DESC,p.product_name;
-- Q4: settled collections
SELECT SUM(amount_paise) FROM payments WHERE status='settled';
-- Q5: orders not fully settled. Aggregate the many-side before joining.
WITH settled AS (
 SELECT order_id,SUM(amount_paise) AS paid FROM payments WHERE status='settled' GROUP BY order_id
)
SELECT o.order_id,o.quantity*o.unit_price_paise AS ordered,COALESCE(s.paid,0) AS paid,
 o.quantity*o.unit_price_paise-COALESCE(s.paid,0) AS outstanding
FROM orders o LEFT JOIN settled s ON o.order_id=s.order_id
WHERE o.quantity*o.unit_price_paise<>COALESCE(s.paid,0) ORDER BY o.order_id;
