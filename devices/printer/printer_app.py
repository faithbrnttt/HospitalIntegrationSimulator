from flask import Flask, request, jsonify
import json
import os

app = Flask(__name__)

CONFIG_FILE = "config.json"

# Load config
def load_config():
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, "r") as f:
            return json.load(f)
    return {
        "deviceName": "Zebra_Printer_01",
        "location": "Lab A",
        "model": "ZD410",
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
        "model": config["model"],
        "location": config["location"]
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

@app.route("/print", methods=["POST"])
def print_label():
    data = request.json
    zpl = data.get("zpl")

    if not zpl:
        return jsonify({"status": "FAILED", "error": "No ZPL provided"}), 400

    return jsonify({
        "status": "SUCCESS",
        "message": "Label printed",
        "printer": load_config()["deviceName"]
    })


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=9001)
