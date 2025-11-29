from integration_engine.engine import IntegrationEngine

def test_scanner_offline_workflow_stops():
    engine = IntegrationEngine()

    # simulate scanner offline (bad endpoint)
    engine.devices["scanner01"].base_url = "http://localhost:9999"

    result = engine.test_scan_all_scanners()

    for key, data in result.items():
        assert data["status"] == "FAILED"
        assert "error" in data
        
def test_workflow_stops_when_scanner_fails():
    from integration_engine.event_processor import EventProcessor

    engine = IntegrationEngine()
    ep = EventProcessor(engine)

    # force offline scanner
    engine.devices["scanner01"].base_url = "http://localhost:9999"

    ep.add_event({"type": "SCAN_SPECIMEN", "payload": {}})
    ep._handle_event(ep.event_queue.pop(0))

    # confirm no analyzer tests queued
    assert len(ep.event_queue) == 0
