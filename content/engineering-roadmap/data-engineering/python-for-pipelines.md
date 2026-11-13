# Python for Your First Pipeline

**Level: Beginner | Learning draft | Independent technical review pending**

Goal: read a small CSV, convert values deliberately and distinguish a data problem from a program failure. Prerequisite: complete the [SQL lab](first-sql-lab.md) and [workspace setup](workspace-and-free-tools.md). Allow two or more two-hour sessions. No extra packages or paid tools are needed.

## Five ideas, one business example

| Python idea | Meaning | Canteen use |
| --- | --- | --- |
| Variable | A name referring to a value | `quantity = 2` |
| Dictionary | Values addressed by field names | `row['quantity']` |
| Loop | Repeat an action | Inspect each incoming order |
| Function | A named operation with inputs and a result | Validate one record |
| Exception | A signal that an operation could not complete normally | Invalid number, unreadable file or failed database write |

Create `practice.py` in your extracted starter folder. Run it using `python practice.py` (or `py` / `python3` as appropriate):

```python
quantity_text = '2'
quantity = int(quantity_text)
unit_price_paise = 2000
print(quantity * unit_price_paise)
```

Expected: `4000`. A CSV value begins as text. The text `'2'` and integer `2` are different types; inspect them with `type(...)`. Change `'2'` to `'two'` and observe the conversion error, then restore it.

## Read rows by column name

```python
import csv
from pathlib import Path

source = Path(__file__).resolve().parent / 'orders.csv'
with source.open(encoding='utf-8-sig', newline='') as stream:
    for row in csv.DictReader(stream):
        quantity = int(row['quantity'])
        value_paise = quantity * int(row['unit_price_paise'])
        print(row['order_id'], value_paise)
```

Expected O1–O5 values: 4000, 5000, 2000, 10000 and 3000. `with` closes the input file after use. `DictReader` uses the header as field names; it does not establish that those fields are valid business data. The pipeline lesson will add those checks. In a notebook, `__file__` is not defined: run a saved script, or use the actual uploaded file path instead.

## Validate a rule with a function

```python
def positive_quantity(text):
    value = int(text)
    if value <= 0:
        raise ValueError('quantity must be positive')
    return value

for text in ['2', '0', 'two']:
    try:
        print(positive_quantity(text))
    except ValueError as error:
        print('Rejected:', error)
```

Expected: one accepted value (`2`) and two rejected cases. This small function only demonstrates conversion and positivity; the full pipeline also requires a specific integer-text format. Avoid a broad `except Exception: pass`: hiding failures can make a broken pipeline look successful.

## Parameters keep values separate from SQL

```python
connection.execute(
    'SELECT * FROM pipeline_orders WHERE order_id = ?',
    ('O1',)
).fetchall()
```

Run this only after opening the persistent database from the [next lab](python-pipeline-lab.md). The `?` is a parameter placeholder; the tuple supplies its value. The comma in `('O1',)` makes a one-item tuple. Do not build SQL by concatenating incoming values.

## Practise before opening the complete solution

1. Modify the CSV reader to calculate a grand total: start at zero, add each value and print after the loop. Expect 24000 paise.
2. Write a function that rejects a negative price but accepts zero. Decide whether zero-priced orders are valid under your business rules.
3. Explain which errors can be isolated to one record and which should stop a load. An invalid quantity can be quarantined; an unavailable database should not be treated as a bad customer order.

AI prompt: “Review my function and suggest boundary cases. Give hints, not a replacement implementation. Ask me to explain each exception.” Run your cases yourself.

Completion: explain text conversion, dictionaries, iteration, function return values and an exception path. If any are unclear, use the [free Python learning resources](workspace-and-free-tools.md) and repeat this exercise.

Source references checked 13 November 2026: [Python CSV](https://docs.python.org/3/library/csv.html), [Python tutorial](https://docs.python.org/3/tutorial/), [SQLite interface](https://docs.python.org/3/library/sqlite3.html).

Next: [Build a persistent, validated pipeline](python-pipeline-lab.md).
