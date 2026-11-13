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

## Persistent pipeline lab

`python pipeline.py` loads orders into `pipeline.sqlite` beside the script. Repeat it, then run `python pipeline.py --input orders-with-errors.csv` twice. Expected stored totals: 5 orders/24000 paise before the error batch; 6/28000 after it, with 6 quarantine records. Existing IDs with changed values are quarantined; they are not overwritten. `python check_pipeline.py` verifies replay and rollback behaviour in disposable databases. See the portal's Python pipeline lesson for full instructions and limitations. Payments remain in the original SQL lab only. Use a new `--db` filename for a separate experiment.

## Corrections and late data

Run `python versioned_pipeline.py` twice using a new default `versions.sqlite`. First load: 7 advanced, 2 unchanged, 2 rejected; replay: 0 advanced, 9 unchanged, 2 rejected. Both finish with 6 current orders worth 33000 paise, 7 history versions and 2 quarantine records. Run `python check_versions.py` for disposable checks. This lab uses full snapshots and source-assigned per-order versions; it does not implement deletions, source extraction or payments. See the portal corrections lesson for assumptions and limits.
