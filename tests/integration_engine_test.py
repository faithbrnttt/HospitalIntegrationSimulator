from integration_engine.engine import IntegrationEngine

def test_engine_scanner():
    engine = IntegrationEngine()
    result = engine.test_scan_all_scanners()
    for key, data in result.items():
        assert data["status"] == "SUCCESS"

def test_engine_analyzer():
    engine = IntegrationEngine()
    result = engine.run_test_on_all_analyzers("X123", "CBC")
    for key, data in result.items():
        assert data["status"] == "SUCCESS"

def test_engine_printer():
    engine = IntegrationEngine()
    result = engine.send_custom_label_to_printers("^XA^FO20,20^FDTest^FS^XZ")
    for key, data in result.items():
        assert data["status"] == "SUCCESS"
