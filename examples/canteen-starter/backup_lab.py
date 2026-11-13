"""Take a consistent SQLite backup into a new file; never overwrite a backup."""
import argparse
from pathlib import Path
import sqlite3

def backup(source,destination):
    source=Path(source).resolve();destination=Path(destination).resolve()
    if source==destination:raise ValueError('Backup must use a different file')
    src=sqlite3.connect(source.as_uri()+'?mode=ro',uri=True)
    try:
        with destination.open('xb'):pass
        dst=sqlite3.connect(destination)
        try:src.backup(dst)
        finally:dst.close()
    finally:src.close()

if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--db',required=True,type=Path)
    parser.add_argument('--out',required=True,type=Path)
    args=parser.parse_args();backup(args.db,args.out);print('Backup created:',args.out)
