"""Business and failure-recovery checks in disposable databases only."""
import sqlite3
from pathlib import Path
from tempfile import TemporaryDirectory
from pipeline import initialise,load,BASE

def totals(db):
    return db.execute('SELECT COUNT(*),SUM(quantity*unit_price_paise) FROM pipeline_orders').fetchone()

with TemporaryDirectory() as temp:
    target=Path(temp)/'test.sqlite'
    db=sqlite3.connect(target)
    initialise(db)
    assert load(db,BASE/'orders.csv',{'P1','P2','P3'})=={'inserted':5,'unchanged':0,'rejected':0}
    db.close()
    db=sqlite3.connect(target)
    assert load(db,BASE/'orders.csv',{'P1','P2','P3'})=={'inserted':0,'unchanged':5,'rejected':0}
    assert totals(db)==(5,24000)
    assert load(db,BASE/'orders-with-errors.csv',{'P1','P2','P3'})=={'inserted':1,'unchanged':1,'rejected':6}
    assert totals(db)==(6,28000)
    assert load(db,BASE/'orders-with-errors.csv',{'P1','P2','P3'})=={'inserted':0,'unchanged':2,'rejected':6}
    assert db.execute('SELECT COUNT(*) FROM quarantine').fetchone()[0]==6
    assert db.execute("SELECT quantity FROM pipeline_orders WHERE order_id='O1'").fetchone()[0]==2
    malformed=Path(temp)/'bad.csv';malformed.write_text('wrong,header\nx,y\n',encoding='utf-8')
    try:load(db,malformed,{'P1'})
    except ValueError:pass
    else:raise AssertionError('Invalid header accepted')
    assert totals(db)==(6,28000)
    malformed.write_text('order_id,order_date,product_id,quantity,unit_price_paise\nX,2026-11-01,P1,1,2000,extra\nY,2026-11-01,P1,1\nZ,2026-11-01,P1,-1,2000\nW,2026-11-01,P1,1,9223372036854775808\n',encoding='utf-8')
    assert load(db,malformed,{'P1'})['rejected']==4
    assert totals(db)==(6,28000)
    db.close()
    # Unexpected database failure after a successful insert must roll back the batch.
    db=sqlite3.connect(':memory:');initialise(db)
    db.execute("CREATE TRIGGER fail_order BEFORE INSERT ON pipeline_orders WHEN NEW.order_id='O2' BEGIN SELECT RAISE(ABORT,'simulated failure'); END")
    try:load(db,BASE/'orders.csv',{'P1','P2','P3'})
    except sqlite3.IntegrityError:pass
    else:raise AssertionError('Failure injection did not fire')
    assert totals(db)==(0,None)
    db.execute('DROP TRIGGER fail_order')
    assert load(db,BASE/'orders.csv',{'P1','P2','P3'})['inserted']==5
    db.close()
print('PASS: persistent replay, invalid records, conflict protection, quarantine replay, header failure, atomic rollback and recovery.')
