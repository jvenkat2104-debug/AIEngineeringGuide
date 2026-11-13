"""One bounded incremental batch; latest orders, reports and checkpoint commit together."""
import argparse
import csv
from datetime import datetime,timezone
import json
import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path
import sqlite3
from tempfile import TemporaryDirectory
import uuid
import reporting
import versioned_pipeline
from pipeline import BASE

LOG=logging.getLogger('canteen')

def run(source,target,batch_size=100,fail_before_commit=False):
    if batch_size<1:raise ValueError('batch size must be positive')
    if Path(source).resolve()==Path(target).resolve():raise ValueError('Source and target must be different files')
    # A read-only URI avoids silently creating a missing source database.
    src=sqlite3.connect(Path(source).resolve().as_uri()+'?mode=ro',uri=True)
    db=sqlite3.connect(target,timeout=5)
    try:
        source_id=src.execute('SELECT source_id FROM source_meta').fetchone()[0]
        versioned_pipeline.initialise(db)
        reporting.initialise(db)
        db.execute('CREATE TABLE IF NOT EXISTS checkpoint(singleton INTEGER PRIMARY KEY CHECK(singleton=1),source_id TEXT NOT NULL,last_seq INTEGER NOT NULL)')
        with db:
            db.execute('BEGIN IMMEDIATE')  # short local writer lock; don't overlap scheduler runs
            saved=db.execute('SELECT source_id,last_seq FROM checkpoint WHERE singleton=1').fetchone()
            if saved and saved[0]!=source_id:raise ValueError('Source identity changed; investigate before replay')
            cursor=saved[1] if saved else 0
            events=src.execute('SELECT source_seq,payload FROM source_events WHERE source_seq>? ORDER BY source_seq LIMIT ?',(cursor,batch_size)).fetchall()
            with TemporaryDirectory() as folder:
                batch=Path(folder)/'batch.csv'
                with batch.open('w',encoding='utf-8',newline='') as stream:
                    writer=csv.DictWriter(stream,fieldnames=versioned_pipeline.COLUMNS)
                    writer.writeheader()
                    for seq,payload in events:
                        row=json.loads(payload)
                        if set(row)!=set(versioned_pipeline.COLUMNS):raise ValueError('Source event schema mismatch')
                        writer.writerow(row)
                with (BASE/'products.csv').open(encoding='utf-8-sig',newline='') as stream:
                    products={p['product_id'] for p in csv.DictReader(stream)}
                counts=versioned_pipeline.load(db,batch,products,transaction=False)
            days=reporting.refresh(db)
            if fail_before_commit:raise RuntimeError('Injected failure before commit')
            latest=events[-1][0] if events else cursor
            db.execute('INSERT OR REPLACE INTO checkpoint VALUES (1,?,?)',(source_id,latest))
        # Pending is an observation, not part of the committed target snapshot.
        pending=src.execute('SELECT COUNT(*) FROM source_events WHERE source_seq>?',(latest,)).fetchone()[0]
        return {'checkpoint':latest,'extracted':len(events),'pending':pending,'counts':counts,'daily_report':days}
    finally:
        src.close();db.close()

if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--source',type=Path,default=BASE/'source.sqlite')
    parser.add_argument('--db',type=Path,default=BASE/'warehouse.sqlite')
    parser.add_argument('--batch-size',type=int,default=100)
    parser.add_argument('--log',type=Path,default=BASE/'pipeline.log')
    parser.add_argument('--fail-before-commit',action='store_true',help='Learning exercise: roll back the batch')
    args=parser.parse_args()
    LOG.setLevel(logging.INFO)
    LOG.addHandler(RotatingFileHandler(args.log,maxBytes=1000000,backupCount=2,encoding='utf-8'))
    run_id=str(uuid.uuid4())
    def emit(event,**fields):
        LOG.info(json.dumps({'utc':datetime.now(timezone.utc).isoformat(),'run_id':run_id,'event':event,**fields}))
    emit('started')
    try:
        result=run(args.source,args.db,args.batch_size,args.fail_before_commit)
    except Exception as error:
        emit('failed',error_type=type(error).__name__)
        print('FAILED:',type(error).__name__,'- investigate input, paths or database; batch target writes rolled back if uncommitted.')
        raise SystemExit(1)
    else:
        code=2 if result['counts']['rejected'] else 0
        emit('committed_with_rejects' if code else 'committed',**result)
        print(json.dumps(result,sort_keys=True))
        print('Exit code:',code,'(2 means committed with data-quality rejects; inspect quarantine)')
        raise SystemExit(code)
