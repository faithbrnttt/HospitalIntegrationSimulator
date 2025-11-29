from flask import Flask, request, jsonify
import json
import os
import random
import string

app = Flask(__name__)

CONFIG_FILE = "config.json"

# Load config
def load_config():
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, "r") as f:
            return json.load(f)
    return {
        "deviceName": "Barcode_Scanner_01",
        "location": "Lab A",
        "model": "SCN-2000",
        "status": "ONLINE"
    }

# Save config
def save_config(config):
    with open(CONFIG_FILE, "w") as f:
        json.dump(config, f, indent=4)

# Endpoint setup

@app.route("/status", methods=["GET"])
def status():
    config = load_config()
    return jsonify({
        "device": config["deviceName"],
        "status": config["status"],
        "location": config["location"],
        "model": config["model"]
    })

@app.route("/settings", methods=["GET"])
def settings():
    config = load_config()
    return jsonify(config)

@app.route("/setname", methods=["POST"])
def set_name():
    data = request.json
    new_name = data.get("deviceName")

    config = load_config()
    config["deviceName"] = new_name
    save_config(config)

    return jsonify({"message": "Device name updated", "newName": new_name})

@app.route("/scan", methods=["GET"])
def scan():
    """Simulate scanning a barcode."""
    # Generate a mock barcode: LAB + 10-digit code
    barcode = "LAB" + ''.join(random.choices(string.digits, k=10))

    return jsonify({
        "barcode": barcode,
        "scanStatus": "SUCCESS",
        "device": load_config()["deviceName"]
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=9002)
