"""Create an append-only synthetic source, without duplicating events on rerun."""
import argparse
import csv
import json
from pathlib import Path
import sqlite3
import uuid
from pipeline import BASE

def seed(path):
    db=sqlite3.connect(path)
    try:
        db.execute('CREATE TABLE IF NOT EXISTS source_meta(source_id TEXT PRIMARY KEY)')
        db.execute('CREATE TABLE IF NOT EXISTS source_events(source_seq INTEGER PRIMARY KEY,payload TEXT NOT NULL)')
        with db:
            if not db.execute('SELECT 1 FROM source_meta').fetchone():
                db.execute('INSERT INTO source_meta VALUES (?)',(str(uuid.uuid4()),))
                with (BASE/'order-changes.csv').open(encoding='utf-8-sig',newline='') as stream:
                    for seq,row in enumerate(csv.DictReader(stream),start=1):
                        db.execute('INSERT INTO source_events VALUES (?,?)',(seq,json.dumps(row)))
    finally:db.close()

if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--db',type=Path,default=BASE/'source.sqlite')
    args=parser.parse_args();seed(args.db);print('Synthetic source ready:',args.db)
