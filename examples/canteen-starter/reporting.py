"""Rebuild small reporting models from current order snapshots and fixture payments."""
import csv
from pipeline import BASE

def initialise(db):
    for statement in [
      'CREATE TABLE IF NOT EXISTS dim_products(product_id TEXT PRIMARY KEY,product_name TEXT NOT NULL)',
      'CREATE TABLE IF NOT EXISTS fact_orders(order_id TEXT PRIMARY KEY,order_date TEXT,product_id TEXT,quantity INTEGER,ordered_paise INTEGER,settled_paise INTEGER,outstanding_paise INTEGER)',
      'CREATE TABLE IF NOT EXISTS daily_report(order_date TEXT PRIMARY KEY,orders INTEGER,ordered_paise INTEGER,settled_paise INTEGER,outstanding_paise INTEGER)']:
        db.execute(statement)

def refresh(db):
    products=list(csv.DictReader((BASE/'products.csv').read_text(encoding='utf-8-sig').splitlines()))
    settled={}
    for row in csv.DictReader((BASE/'payments.csv').read_text(encoding='utf-8-sig').splitlines()):
        if row['status']=='settled':settled[row['order_id']]=settled.get(row['order_id'],0)+int(row['amount_paise'])
    db.execute('DELETE FROM dim_products')
    db.executemany('INSERT INTO dim_products VALUES (?,?)',[(p['product_id'],p['product_name']) for p in products])
    db.execute('DELETE FROM fact_orders')
    for order_id,day,product,quantity,price,version in db.execute('SELECT * FROM current_orders').fetchall():
        if not db.execute('SELECT 1 FROM dim_products WHERE product_id=?',(product,)).fetchone():
            raise ValueError('Missing product dimension')
        ordered=quantity*price;paid=settled.get(order_id,0)
        db.execute('INSERT INTO fact_orders VALUES (?,?,?,?,?,?,?)',(order_id,day,product,quantity,ordered,paid,ordered-paid))
    db.execute('DELETE FROM daily_report')
    db.execute('INSERT INTO daily_report SELECT order_date,COUNT(*),SUM(ordered_paise),SUM(settled_paise),SUM(outstanding_paise) FROM fact_orders GROUP BY order_date')
    current=db.execute('SELECT COUNT(*),COALESCE(SUM(quantity*unit_price_paise),0) FROM current_orders').fetchone()
    fact=db.execute('SELECT COUNT(*),COALESCE(SUM(ordered_paise),0) FROM fact_orders').fetchone()
    report=db.execute('SELECT COALESCE(SUM(orders),0),COALESCE(SUM(ordered_paise),0) FROM daily_report').fetchone()
    if current!=fact or fact!=report:raise ValueError('Reconciliation failed: counts or value')
    if db.execute('SELECT COUNT(*) FROM fact_orders WHERE ordered_paise<>settled_paise+outstanding_paise').fetchone()[0]:
        raise ValueError('Reconciliation failed: order balance')
    return db.execute('SELECT * FROM daily_report ORDER BY order_date').fetchall()
