import datetime
import os

# Build path to logs folder relative to this file
BASE_PATH = os.path.dirname(os.path.abspath(__file__))
LOG_DIR = os.path.join(BASE_PATH, "..", "logs")

# Ensure logs folder exists
os.makedirs(LOG_DIR, exist_ok=True)

ENGINE_LOG_FILE = os.path.join(LOG_DIR, "engine.log")
ERROR_LOG_FILE = os.path.join(LOG_DIR, "errors.log")

def _write_to_file(filepath, message):
    with open(filepath, "a") as f:
        f.write(message + "\n")

def _timestamp():
    return datetime.datetime.now().isoformat()

def log(message, level="INFO"):
    formatted = f"[{_timestamp()}] [{level}] {message}"

    # Print to console
    print(formatted)

    # Write to engine log
    _write_to_file(ENGINE_LOG_FILE, formatted)

def log_error(message):
    formatted = f"[{_timestamp()}] [ERROR] {message}"

    # Console
    print(formatted)

    # Write to engine log + error log
    _write_to_file(ENGINE_LOG_FILE, formatted)
    _write_to_file(ERROR_LOG_FILE, formatted)

def log_warning(message):
    formatted = f"[{_timestamp()}] [WARNING] {message}"

    print(formatted)
    _write_to_file(ENGINE_LOG_FILE, formatted)
