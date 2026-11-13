"""Synthetic learning lab. Uses Python standard library only; no persistent database."""
import csv
import sqlite3
from pathlib import Path

BASE = Path(__file__).resolve().parent

def build_database():
    db = sqlite3.connect(':memory:')
    db.execute('PRAGMA foreign_keys = ON')
    db.executescript('''
    CREATE TABLE products(product_id TEXT PRIMARY KEY, product_name TEXT NOT NULL);
    CREATE TABLE orders(order_id TEXT PRIMARY KEY, order_date TEXT NOT NULL,
      product_id TEXT NOT NULL REFERENCES products(product_id),
      quantity INTEGER NOT NULL CHECK(quantity>0),
      unit_price_paise INTEGER NOT NULL CHECK(unit_price_paise>=0));
    CREATE TABLE payments(payment_id TEXT PRIMARY KEY,
      order_id TEXT NOT NULL REFERENCES orders(order_id),
      amount_paise INTEGER NOT NULL CHECK(amount_paise>=0),
      status TEXT NOT NULL CHECK(status IN ('settled','pending')));
    ''')
    for table, columns in [('products', 2), ('orders', 5), ('payments', 4)]:
        with (BASE / (table + '.csv')).open(encoding='utf-8', newline='') as stream:
            reader = csv.reader(stream)
            next(reader)
            db.executemany(f'INSERT INTO {table} VALUES ({",".join("?" for _ in range(columns))})', reader)
    db.commit()
    return db

if __name__ == '__main__':
    with build_database() as db:
        print('Loaded: 3 products, 5 orders, 6 payments (synthetic data).')
        # Replace this query with each exercise. Values are paise, not rupees.
        query = 'SELECT order_id, quantity * unit_price_paise AS order_value_paise FROM orders ORDER BY order_id'
        for row in db.execute(query):
            print(row)
