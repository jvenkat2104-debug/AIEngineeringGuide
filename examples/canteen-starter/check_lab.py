"""Verify business answers and demonstrate duplicate/grain failures."""
import sqlite3
from lab import build_database
with build_database() as db:
    statements=[x.strip() for x in open(__file__.replace('check_lab.py','solutions.sql'),encoding='utf-8-sig').read().split(';') if x.strip()]
    expected=[[(5,24000)],[('2026-11-01',9000),('2026-11-02',15000)],[('Idli',3),('Meal',3),('Tea and snack',1)],[(20000,)],[('O4',10000,6000,4000)]]
    for query,answer in zip(statements,expected):
        assert db.execute(query).fetchall()==answer,query
    assert len(statements)==5
    # A naive one-to-many join repeats O4 and inflates ordered value.
    assert db.execute('SELECT SUM(o.quantity*o.unit_price_paise) FROM orders o JOIN payments p ON p.order_id=o.order_id').fetchone()[0]==34000
    try:
        db.execute("INSERT INTO orders SELECT * FROM orders WHERE order_id='O1'")
    except sqlite3.IntegrityError:
        pass
    else:
        raise AssertionError('Duplicate order accepted')
print('PASS: five business answers, join fan-out, duplicate rejection.')
