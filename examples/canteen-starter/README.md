# Canteen starter lab

Synthetic data only. Python 3.9+; no pip packages, cloud account or API key.

Run `python lab.py` (Windows may use `py lab.py`). Edit the `query` string for exercises.
Run `python check_lab.py` to check the five reference answers and failure examples.
SQL is SQLite dialect. Multi-line queries need Python triple quotes.

Each orders row represents one single-product order; payments can have multiple rows per order.
Prices are captured at purchase time and expressed in integer paise. 100 paise = INR 1.
This simplified model excludes taxes, refunds, discounts and operating costs. Ordered value is not profit or a financial-reporting definition of revenue.
Each run creates a fresh in-memory database; it does not demonstrate persistent incremental loading.

Lessons: https://jvenkat2104-debug.github.io/engineering-roadmap/data-engineering/
Content/data: CC BY 4.0. Code: Apache 2.0. Repository licensing policy applies.
