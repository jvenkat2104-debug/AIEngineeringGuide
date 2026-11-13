"""Learning pipeline: immutable orders, row quarantine, transactional persistent loads."""
import argparse
import csv
from datetime import date
import hashlib
import io
import json
from pathlib import Path
import re
import sqlite3

BASE = Path(__file__).resolve().parent
FIELDS = ['order_id', 'order_date', 'product_id', 'quantity', 'unit_price_paise']

def initialise(db):
    db.executescript('''
    CREATE TABLE IF NOT EXISTS pipeline_orders(
      order_id TEXT PRIMARY KEY, order_date TEXT NOT NULL, product_id TEXT NOT NULL,
      quantity INTEGER NOT NULL CHECK(quantity>0),
      unit_price_paise INTEGER NOT NULL CHECK(unit_price_paise>=0));
    CREATE TABLE IF NOT EXISTS quarantine(
      source_hash TEXT NOT NULL, record_number INTEGER NOT NULL,
      reason TEXT NOT NULL, raw_json TEXT NOT NULL,
      PRIMARY KEY(source_hash,record_number,reason));
    ''')

def validate(row, products):
    if None in row or any(value is None for value in row.values()):
        raise ValueError('wrong field count')
    if not row['order_id'].strip():
        raise ValueError('missing order_id')
    if not re.fullmatch(r'[0-9]{4}-[0-9]{2}-[0-9]{2}', row['order_date']):
        raise ValueError('date must be YYYY-MM-DD')
    try:
        date.fromisoformat(row['order_date'])
    except ValueError:
        raise ValueError('invalid calendar date') from None
    if row['product_id'] not in products:
        raise ValueError('unknown product')
    numbers=[]
    for field in ['quantity','unit_price_paise']:
        if not re.fullmatch(r'[0-9]+',row[field]):
            raise ValueError(field + ' must be a non-negative integer')
        number=int(row[field])
        if number>2**63-1:
            raise ValueError(field + ' exceeds SQLite integer range')
        numbers.append(number)
    if numbers[0]==0:
        raise ValueError('quantity must be positive')
    return (row['order_id'],row['order_date'],row['product_id'],*numbers)

def load(db, source, products):
    # Read one snapshot: digest and parsed content describe the same bytes.
    payload=Path(source).read_bytes()
    digest=hashlib.sha256(payload).hexdigest()
    reader=csv.DictReader(io.StringIO(payload.decode('utf-8-sig'),newline=''),strict=True)
    if reader.fieldnames != FIELDS:
        raise ValueError('CSV header must exactly match: ' + ','.join(FIELDS))
    counts={'inserted':0,'unchanged':0,'rejected':0}
    # Caller uses a fresh connection with no pre-existing transaction.
    with db:
        for record_number,row in enumerate(reader,start=1):
            reason=None
            try:
                values=validate(row,products)
            except ValueError as error:
                reason=str(error)
            else:
                existing=db.execute('SELECT * FROM pipeline_orders WHERE order_id=?',(values[0],)).fetchone()
                if existing is None:
                    db.execute('INSERT INTO pipeline_orders VALUES (?,?,?,?,?)',values)
                    counts['inserted']+=1
                elif existing == values:
                    counts['unchanged']+=1
                else:
                    reason='conflicting order_id; correction requires review'
            if reason is not None:
                db.execute('INSERT OR IGNORE INTO quarantine VALUES (?,?,?,?)',
                           (digest,record_number,reason,json.dumps(row)))
                counts['rejected']+=1
    return counts

if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--input',type=Path,default=BASE/'orders.csv')
    parser.add_argument('--db',type=Path,default=BASE/'pipeline.sqlite')
    args=parser.parse_args()
    with (BASE/'products.csv').open(encoding='utf-8-sig',newline='') as stream:
        products={row['product_id'] for row in csv.DictReader(stream)}
    db=sqlite3.connect(args.db)
    try:
        initialise(db)
        counts=load(db,args.input,products)
        print(json.dumps(counts,sort_keys=True))
        print('Stored orders/value (paise):',db.execute('SELECT COUNT(*),COALESCE(SUM(quantity*unit_price_paise),0) FROM pipeline_orders').fetchone())
        print('Stored quarantine records:',db.execute('SELECT COUNT(*) FROM quarantine').fetchone()[0])
    finally:
        db.close()
