from integration_engine.postgres_db import PostgresDB
from integration_engine.etl_processor import ETLProcessor

def test_cbc_etl():
    db = PostgresDB()
    etl = ETLProcessor(db)

    result_json = {
        "WBC": 6.4,
        "HGB": 13.1,
        "HCT": 40.0,
        "PLT": 250
    }

    etl.process_test_result(
        analyzer_id="analyzer01",
        specimen_barcode="CBC123",
        test_type="CBC",
        result_json=result_json,
        result_time= None
    )

    cur = db.conn.cursor()
    cur.execute("SELECT * FROM cbc_results WHERE specimen_barcode='CBC123'")
    assert cur.fetchone() is not None
