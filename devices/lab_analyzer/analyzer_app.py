from flask import Flask, request, jsonify
import json
import os
import random
import datetime

app = Flask(__name__)

CONFIG_FILE = "config.json"

# Load config
def load_config():
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, "r") as f:
            return json.load(f)
    return {
        "deviceName": "Chem_Analyzer_01",
        "location": "Core Lab",
        "model": "HMX-5000",
        "status": "ONLINE"
    }

# Save config
def save_config(config):
    with open(CONFIG_FILE, "w") as f:
        json.dump(config, f, indent=4)
        
        
#Endpoint setup

@app.route("/status", methods=["GET"])
def status():
    config = load_config()
    return jsonify({
        "device": config["deviceName"],
        "status": config["status"],
        "location": config["location"],
        "model": config["model"],
        "temperature": random.uniform(36.5, 37.5),  # Example device sensor reading
        "lastCalibration": (datetime.datetime.now() - datetime.timedelta(days=1)).isoformat()
    })

@app.route("/settings", methods=["GET"])
def settings():
    return jsonify(load_config())

@app.route("/setname", methods=["POST"])
def set_name():
    data = request.json
    new_name = data.get("deviceName")

    config = load_config()
    config["deviceName"] = new_name
    save_config(config)

    return jsonify({"message": "Device name updated", "newName": new_name})

@app.route("/sendresult", methods=["POST"])
def send_result():
    """Simulate generating a lab result (CBC, CMP, etc.)"""
    data = request.json
    specimen_id = data.get("specimenId", "UNKNOWN")
    test_type = data.get("testType", "CBC")

    # Generate example results
    results = {
        "CBC": {
            "WBC": round(random.uniform(3.5, 12.0), 1),
            "HGB": round(random.uniform(11, 16), 1),
            "HCT": round(random.uniform(33, 49), 1),
            "PLT": random.randint(150, 400)
        },
        "CMP": {
            "Sodium": random.randint(135, 145),
            "Potassium": round(random.uniform(3.5, 5.1), 1),
            "Calcium": round(random.uniform(8.5, 10.5), 1)
        }
    }

    generated = results.get(test_type.upper(), {})

    return jsonify({
        "message": "Result generated",
        "device": load_config()["deviceName"],
        "specimenId": specimen_id,
        "testType": test_type,
        "timestamp": datetime.datetime.now().isoformat(),
        "resultData": generated
    })
    
@app.route("/runtest", methods=["POST"])
def run_test():
    data = request.json
    specimen_id = data.get("specimenId", "UNKNOWN")
    test_type = data.get("testType", "CBC").upper()

    # Generate results
    results = {
        "CBC": {
            "WBC": round(random.uniform(3.5, 12.0), 1),
            "HGB": round(random.uniform(11, 16), 1),
            "HCT": round(random.uniform(33, 49), 1),
            "PLT": random.randint(150, 400)
        },
        "CMP": {
            "Sodium": random.randint(135, 145),
            "Potassium": round(random.uniform(3.5, 5.1), 1),
            "Calcium": round(random.uniform(8.5, 10.5), 1)
        }
    }

    result_data = results.get(test_type, {})

    return jsonify({
        "status": "SUCCESS",
        "result": result_data,
        "specimenId": specimen_id,
        "testType": test_type,
        "timestamp": datetime.datetime.now().isoformat()
    })


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=9003)
