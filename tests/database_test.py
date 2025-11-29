from integration_engine.postgres_db import PostgresDB

def test_specimen_insert():
    db = PostgresDB()
    db.ensure_specimen_exists("TEST123")
    
    rows = db.conn.cursor()
    rows.execute("SELECT * FROM specimens WHERE specimen_barcode='TEST123'")
    data = rows.fetchone()

    assert data is not None

def test_scan_event():
    db = PostgresDB()
    db.log_scan_event("scanner01", "TEST456")

    cur = db.conn.cursor()
    cur.execute("SELECT * FROM scan_events WHERE barcode='TEST456'")
    assert cur.fetchone() is not None
