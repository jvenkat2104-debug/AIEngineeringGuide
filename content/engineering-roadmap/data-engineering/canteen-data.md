# Meet the canteen data

**Level: Beginner | Synthetic dataset | Independent review pending**

Goal: identify keys, row meanings and units before writing SQL. Download the [starter kit](../../../downloads/canteen-starter.zip). No real students, customers or transactions are represented. Dates are illustrative, not evidence of current trading.

## Dictionary

| File/table | One row means | Columns |
| --- | --- | --- |
| products | One product | `product_id`: unique text key; `product_name`: display label |
| orders | One single-product order | `order_id`: unique text key; `order_date`: ISO date text; `product_id`: product reference; `quantity`: positive integer units; `unit_price_paise`: non-negative integer price per unit at purchase time |
| payments | One payment record | `payment_id`: unique text key; `order_id`: order reference; `amount_paise`: non-negative integer; `status`: settled or pending |

100 paise = INR 1. Use integer paise to avoid floating-point rounding in this starter. The dataset has 3 products, 5 orders and 6 payment rows. An order can have more than one payment row. Product names are not reliable keys.

The starter simplifies real systems: each order has one product, prices are captured on the order, and it excludes cancellations, refunds, tax, discounts and expenses. Ordered value is quantity × unit price; it is not profit or a formal revenue-recognition measure.

## Inspect before computing

Open the CSVs in a text editor. O4 has two payment records: 6000 paise settled and 4000 pending. Predict its outstanding amount. Then compare the two dates' order totals by hand. Avoid counting payment rows as orders.

Keys and constraints in `lab.py` reject duplicate IDs, unknown product/order references, negative amounts and non-positive quantities. They do not validate every business rule: for example, date validity, overpayment policy and source corrections need later work. The first dataset is clean; future lessons will introduce invalid files explicitly.

## Completion check

Explain why joining an order to two payment rows can repeat its value. Identify which field preserves a historical price, and why replacing it with today's menu price could change yesterday's report.

AI prompt: “Using this dictionary, ask me to distinguish order grain and payment grain. Give a small counterexample, then let me predict the join result.”

Next: [First SQL lab](first-sql-lab.md).
