"""Integration checks: bounded extraction, models, rollback, restart, logging, backup."""
from contextlib import closing
import json
from pathlib import Path
import shutil
import sqlite3
import subprocess
import sys
from tempfile import TemporaryDirectory
from backup_lab import backup
from pipeline import BASE
from run_incremental import run
from seed_source import seed

EXPECTED=[('2026-11-01',3,13000,9000,4000),('2026-11-02',3,20000,11000,9000)]
with TemporaryDirectory() as folder:
    folder=Path(folder);source=folder/'source.sqlite';target=folder/'warehouse.sqlite'
    seed(source);seed(source)
    with closing(sqlite3.connect(source)) as db, db:assert db.execute('SELECT COUNT(*) FROM source_events').fetchone()[0]==11
    first=run(source,target,4);assert first['checkpoint']==4 and first['extracted']==4 and first['pending']==7
    second=run(source,target,4);assert second['checkpoint']==8 and second['daily_report']==EXPECTED
    with closing(sqlite3.connect(target)) as db, db:
        before=db.execute('SELECT COUNT(*) FROM order_versions').fetchone()[0]
    try:run(source,target,4,True)
    except RuntimeError:pass
    else:raise AssertionError('Failure injection did not fire')
    with closing(sqlite3.connect(target)) as db, db:
        assert db.execute('SELECT last_seq FROM checkpoint').fetchone()[0]==8
        assert db.execute('SELECT COUNT(*) FROM version_quarantine').fetchone()[0]==0
        assert db.execute('SELECT COUNT(*) FROM order_versions').fetchone()[0]==before
        assert db.execute('SELECT * FROM daily_report ORDER BY order_date').fetchall()==EXPECTED
    third=run(source,target,4);assert third['checkpoint']==11 and third['counts']['rejected']==2
    assert run(source,target)['extracted']==0
    # A late business date with a new source sequence is still extracted.
    with closing(sqlite3.connect(source)) as db, db:
        db.execute('INSERT INTO source_events VALUES (?,?)',(12,json.dumps(dict(order_id='O8',order_date='2026-10-01',product_id='P1',quantity='1',unit_price_paise='2000',source_version='1'))))
    assert run(source,target)['daily_report'][0]==('2026-10-01',1,2000,0,2000)
    # Unexpected modelling failure rolls back accepted history and checkpoint too.
    with closing(sqlite3.connect(source)) as db, db:
        db.execute('INSERT INTO source_events VALUES (?,?)',(13,json.dumps(dict(order_id='O9',order_date='2026-11-03',product_id='P1',quantity='1',unit_price_paise='2000',source_version='1'))))
    with closing(sqlite3.connect(target)) as db, db:
        db.execute("CREATE TRIGGER fail_report BEFORE INSERT ON daily_report BEGIN SELECT RAISE(ABORT,'simulated report failure'); END")
    try:run(source,target)
    except sqlite3.IntegrityError:pass
    else:raise AssertionError('Report failure did not fire')
    with closing(sqlite3.connect(target)) as db, db:
        assert db.execute('SELECT last_seq FROM checkpoint').fetchone()[0]==12
        assert db.execute("SELECT COUNT(*) FROM order_versions WHERE order_id='O9'").fetchone()[0]==0
        db.execute('DROP TRIGGER fail_report')
    assert run(source,target)['checkpoint']==13
    restored=folder/'restored.sqlite';backup(target,restored)
    with closing(sqlite3.connect(restored)) as db, db:
        assert db.execute('PRAGMA integrity_check').fetchone()[0]=='ok'
        assert db.execute('SELECT COUNT(*) FROM fact_orders').fetchone()[0]==8
    assert run(source,restored)['extracted']==0
    try:backup(target,restored)
    except FileExistsError:pass
    else:raise AssertionError('Existing backup overwritten')
    other=folder/'other-source.sqlite';seed(other)
    try:run(other,target)
    except ValueError:pass
    else:raise AssertionError('Source identity reset accepted')
    # CLI contract and structured logs on a fresh target.
    clean=folder/'clean.sqlite';seed(clean)
    cli=folder/'cli.sqlite';log=folder/'pipeline.log'
    command=[sys.executable,str(BASE/'run_incremental.py'),'--source',str(clean),'--db',str(cli),'--log',str(log)]
    result=subprocess.run(command,capture_output=True,text=True);assert result.returncode==2,result.stderr
    records=[json.loads(line) for line in log.read_text(encoding='utf-8').splitlines()]
    assert records[-1]['event']=='committed_with_rejects' and records[-1]['checkpoint']==11
    assert subprocess.run(command,capture_output=True).returncode==0
    fail_command=command+['--fail-before-commit']
    assert subprocess.run(fail_command,capture_output=True).returncode==1
print('PASS: incremental batches, late data, reporting reconciliation, atomic checkpoint, recovery, backup, source identity, CLI statuses and logs.')
