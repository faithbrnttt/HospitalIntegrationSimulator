import requests
import time
from .logger import log_error


class DeviceClient:
    """
    Unified client for scanner, analyzer, and printer devices.
    """

    def __init__(self, entry):
        """
        Expected registry entry:
        {
            "id": "scanner01",
            "type": "scanner",
            "host": "localhost",
            "port": 9002
        }
        """
        self.id = entry["id"]
        self.type = entry["type"]
        self.host = entry["host"]
        self.port = entry["port"]
        self.base_url = f"http://{self.host}:{self.port}"

        self.last_zpl = None

    # ------------------------------------------
    # Core retrying HTTP request helper
    # ------------------------------------------

    def _request_with_retry(self, method, path, json=None, retries=3, backoff=1):
        """
        Send an HTTP request with exponential backoff.
        Returns (data, error_string).
        """
        url = self.base_url + path

        for attempt in range(1, retries + 1):
            try:
                r = requests.request(method, url, json=json, timeout=3)
                r.raise_for_status()
                return r.json(), None

            except Exception as e:
                log_error(f"[{self.id}] Attempt {attempt} failed: {e}")

                if attempt == retries:
                    return None, str(e)

                time.sleep(backoff)
                backoff *= 2

    # ------------------------------------------
    # PRINTER METHODS
    # ------------------------------------------

    def fetch_printer_settings(self):
        return self._request_with_retry("GET", "/settings")

    def test_print(self, zpl=None):
        if zpl is None:
            zpl = "^XA^FO50,50^ADN,36,20^FDTEST PRINT^FS^XZ"

        self.last_zpl = zpl
        return self._request_with_retry("POST", "/print", json={"zpl": zpl})

    def reprint_last_label(self):
        if not self.last_zpl:
            return None, "No previous label to reprint."

        return self._request_with_retry("POST", "/print", json={"zpl": self.last_zpl})

    # ------------------------------------------
    # SCANNER METHODS
    # ------------------------------------------

    def fetch_scanner_settings(self):
        return self._request_with_retry("GET", "/settings")

    def scan_barcode(self):
        return self._request_with_retry("GET", "/scan")

    # ------------------------------------------
    # ANALYZER METHODS
    # ------------------------------------------

    def fetch_analyzer_settings(self):
        return self._request_with_retry("GET", "/settings")

    def generate_lab_result(self, specimen_id, test_type):
        payload = {
            "specimenId": specimen_id,
            "testType": test_type
        }
        return self._request_with_retry("POST", "/runtest", json=payload)
