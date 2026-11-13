"""Learning lab: source-versioned full order snapshots, retained history and latest view."""
import argparse
import csv
import hashlib
import io
import json
from pathlib import Path
import re
import sqlite3
from pipeline import BASE,FIELDS,validate

COLUMNS=FIELDS+['source_version']

def initialise(db):
    db.executescript('''
    CREATE TABLE IF NOT EXISTS order_versions(
      order_id TEXT NOT NULL, order_date TEXT NOT NULL, product_id TEXT NOT NULL,
      quantity INTEGER NOT NULL CHECK(quantity>0),
      unit_price_paise INTEGER NOT NULL CHECK(unit_price_paise>=0),
      source_version INTEGER NOT NULL CHECK(source_version>0),
      PRIMARY KEY(order_id,source_version));
    CREATE VIEW IF NOT EXISTS current_orders AS
      SELECT v.* FROM order_versions v WHERE v.source_version=(
        SELECT MAX(h.source_version) FROM order_versions h WHERE h.order_id=v.order_id);
    CREATE TABLE IF NOT EXISTS version_quarantine(
      source_hash TEXT NOT NULL, record_number INTEGER NOT NULL,
      reason TEXT NOT NULL, raw_json TEXT NOT NULL,
      PRIMARY KEY(source_hash,record_number,reason));
    ''')

def load(db,source,products):
    payload=Path(source).read_bytes()
    digest=hashlib.sha256(payload).hexdigest()
    reader=csv.DictReader(io.StringIO(payload.decode('utf-8-sig'),newline=''),strict=True)
    if reader.fieldnames!=COLUMNS:
        raise ValueError('CSV header must exactly match: '+','.join(COLUMNS))
    counts={'advanced':0,'late_history':0,'unchanged':0,'rejected':0}
    with db:
        for number,raw in enumerate(reader,start=1):
            reason=None
            try:
                row=dict(raw)
                text=row.pop('source_version')
                if not isinstance(text,str) or not re.fullmatch(r'[0-9]+',text):
                    raise ValueError('source_version must be a positive integer')
                version=int(text)
                if not 1<=version<=2**63-1:
                    raise ValueError('source_version out of range')
                values=validate(row,products)
            except ValueError as error:
                reason=str(error)
            else:
                old=db.execute('SELECT order_date,product_id,quantity,unit_price_paise FROM order_versions WHERE order_id=? AND source_version=?',(values[0],version)).fetchone()
                if old is not None:
                    if old==values[1:]:counts['unchanged']+=1
                    else:reason='conflicting payload for existing order/version'
                else:
                    latest=db.execute('SELECT MAX(source_version) FROM order_versions WHERE order_id=?',(values[0],)).fetchone()[0]
                    db.execute('INSERT INTO order_versions VALUES (?,?,?,?,?,?)',(*values,version))
                    counts['advanced' if latest is None or version>latest else 'late_history']+=1
            if reason is not None:
                db.execute('INSERT OR IGNORE INTO version_quarantine VALUES (?,?,?,?)',(digest,number,reason,json.dumps(raw)))
                counts['rejected']+=1
    return counts

if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--input',type=Path,default=BASE/'order-changes.csv')
    parser.add_argument('--db',type=Path,default=BASE/'versions.sqlite')
    args=parser.parse_args()
    with (BASE/'products.csv').open(encoding='utf-8-sig',newline='') as stream:
        products={row['product_id'] for row in csv.DictReader(stream)}
    db=sqlite3.connect(args.db)
    try:
        initialise(db)
        print(json.dumps(load(db,args.input,products),sort_keys=True))
        print('Current orders/value (paise):',db.execute('SELECT COUNT(*),SUM(quantity*unit_price_paise) FROM current_orders').fetchone())
        print('History/quarantine:',db.execute('SELECT (SELECT COUNT(*) FROM order_versions),(SELECT COUNT(*) FROM version_quarantine)').fetchone())
    finally:db.close()
