"""Check worked reporting answers and deliberately introduce report discrepancies."""
from contextlib import closing
from pathlib import Path
import sqlite3
from tempfile import TemporaryDirectory
from pipeline import BASE
from seed_source import seed
from run_incremental import run

with TemporaryDirectory() as folder:
    source=Path(folder)/'source.sqlite';target=Path(folder)/'warehouse.sqlite'
    seed(source);run(source,target)
    queries=[q.strip() for q in (BASE/'reporting-scenarios.sql').read_text(encoding='utf-8-sig').split(';') if q.strip()]
    assert len(queries)==5
    with closing(sqlite3.connect(target)) as db:
        assert db.execute(queries[0]).fetchall()==[(33000,20000,13000)]
        for query in queries[1:]:assert db.execute(query).fetchall()==[]
        # Balanced grand totals do not establish the right allocation per day.
        db.execute("UPDATE daily_report SET ordered_paise=ordered_paise-4000,outstanding_paise=outstanding_paise-4000 WHERE order_date='2026-11-01'")
        db.execute("UPDATE daily_report SET ordered_paise=ordered_paise+4000,outstanding_paise=outstanding_paise+4000 WHERE order_date='2026-11-02'")
        assert db.execute('SELECT SUM(ordered_paise) FROM daily_report').fetchone()[0]==33000
        assert len(db.execute(queries[3]).fetchall())==2
        db.rollback()
        db.execute("DELETE FROM daily_report WHERE order_date='2026-11-01'")
        assert db.execute(queries[3]).fetchall()==[('2026-11-01',13000,None)]
        db.rollback()
        db.execute("UPDATE fact_orders SET settled_paise=5000,outstanding_paise=-1000 WHERE order_id='O1'")
        assert db.execute(queries[1]).fetchall()==[('O1',4000,5000,-1000)]
        db.rollback()
        db.execute("DELETE FROM dim_products WHERE product_id='P3'")
        assert db.execute(queries[4]).fetchall()==[('O5',)]
        db.rollback()
print('PASS: reference totals, overpayment, duplicate-key query, per-date errors, missing report dates and missing dimension.')
