import requests

# Corrected to match your actual device ports

def test_scanner_online():
    res = requests.get("http://localhost:9002/status")
    assert res.status_code == 200

    device_field = res.json().get("device")
    assert device_field is not None
    assert "scanner" in device_field.lower()



def test_scanner_scan():
    res = requests.get("http://localhost:9002/scan")
    data = res.json()
    assert "barcode" in data

def test_analyzer_run_test():
    res = requests.post("http://localhost:9003/runtest", json={
        "specimenId": "TEST123",
        "testType": "CBC"
    })
    data = res.json()
    assert data["status"] == "SUCCESS"
    assert "result" in data

def test_printer_print():
    res = requests.post("http://localhost:9001/print", json={
        "zpl": "^XA^FO50,50^FDHello^FS^XZ"
    })
    assert res.json()["status"] == "SUCCESS"
