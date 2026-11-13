"""Check correction/replay semantics, out-of-order snapshots and atomic recovery."""
from pathlib import Path
from tempfile import TemporaryDirectory
import sqlite3
from versioned_pipeline import initialise,load,BASE

with TemporaryDirectory() as temp:
    target=Path(temp)/'versions.sqlite'
    db=sqlite3.connect(target);initialise(db)
    assert load(db,BASE/'order-changes.csv',{'P1','P2','P3'})=={'advanced':7,'late_history':0,'unchanged':2,'rejected':2}
    assert db.execute('SELECT COUNT(*),SUM(quantity*unit_price_paise) FROM current_orders').fetchone()==(6,33000)
    assert db.execute("SELECT source_version,quantity FROM order_versions WHERE order_id='O4' ORDER BY source_version").fetchall()==[(1,2),(2,3)]
    db.close();db=sqlite3.connect(target)
    assert load(db,BASE/'order-changes.csv',{'P1','P2','P3'})=={'advanced':0,'late_history':0,'unchanged':9,'rejected':2}
    assert db.execute('SELECT COUNT(*) FROM version_quarantine').fetchone()[0]==2
    db.close()
    batch=Path(temp)/'out-of-order.csv'
    header='order_id,order_date,product_id,quantity,unit_price_paise,source_version\n'
    batch.write_text(header+'X,2026-11-01,P1,3,2000,3\nX,2026-11-01,P1,2,2000,2\n',encoding='utf-8')
    db=sqlite3.connect(':memory:');initialise(db)
    assert load(db,batch,{'P1'})=={'advanced':1,'late_history':1,'unchanged':0,'rejected':0}
    assert db.execute('SELECT source_version,quantity FROM current_orders').fetchone()==(3,3)
    batch.write_text(header+'X,2026-11-01,P1,1,2000,0\nX,2026-11-01,P1,1,2000,abc\nX,2026-11-01,P1,1,2000,\n',encoding='utf-8')
    assert load(db,batch,{'P1'})['rejected']==3
    db.close()
    db=sqlite3.connect(':memory:');initialise(db)
    db.execute("CREATE TRIGGER fail_update BEFORE INSERT ON order_versions WHEN NEW.source_version=2 BEGIN SELECT RAISE(ABORT,'simulated failure'); END")
    try:load(db,BASE/'order-changes.csv',{'P1','P2','P3'})
    except sqlite3.IntegrityError:pass
    else:raise AssertionError('Failure not injected')
    assert db.execute('SELECT COUNT(*) FROM order_versions').fetchone()[0]==0
    assert db.execute('SELECT COUNT(*) FROM version_quarantine').fetchone()[0]==0
    db.execute('DROP TRIGGER fail_update')
    assert load(db,BASE/'order-changes.csv',{'P1','P2','P3'})['advanced']==7
    db.close()
print('PASS: corrections, history, reconnect/replay, late snapshots, invalid versions, conflicts, rollback/recovery.')
