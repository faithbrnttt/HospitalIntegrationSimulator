# HospitalIntegrationSimulator

A Python-based hospital device integration simulator that models how core lab devices interact within a healthcare workflow.

This project simulates a small integration environment with:
- **Barcode scanners**
- **Label printers**
- **Lab analyzers**
- A central **integration engine**
- **Event-driven workflow processing**
- **ETL-style normalization for lab results**
- **PostgreSQL logging and persistence**

The goal of this project is to demonstrate how healthcare-adjacent devices and services can communicate through a lightweight integration layer while supporting workflow orchestration, logging, and result processing.

---

## Features

- Simulated **printer**, **scanner**, and **lab analyzer** device services
- Central **integration engine** that loads devices from a registry
- HTTP-based communication between the engine and devices
- **Event queue** for workflow orchestration
- Simulated workflow:
  - Scan specimen
  - Run analyzer test
  - Print specimen label
- **Retry logic** for device communication failures
- **Device status tracking** (ONLINE / OFFLINE)
- **ETL processing** for analyzer results
- PostgreSQL integration for:
  - scan event logging
  - specimen tracking
  - lab test result logging
  - print job logging
- Test suite covering configuration, devices, ETL, queue logic, retries, and integration engine behavior

---

## Project Structure

```text
HospitalIntegrationSimulator/
│
├── devices/
│   ├── printer/
│   │   ├── config.json
│   │   └── printer_app.py
│   ├── scanner/
│   │   ├── config.json
│   │   └── scanner_app.py
│   └── lab_analyzer/
│       ├── analyzer_app.py
│       └── config.json
│
├── integration_engine/
│   ├── __init__.py
│   ├── device_client.py
│   ├── device_registry.json
│   ├── engine.py
│   ├── etl_processor.py
│   ├── event_processor.py
│   ├── logger.py
│   ├── postgres_db.py
│   └── utils.py
│
├── logs/
├── tests/
│   ├── conf_test.py
│   ├── database_test.py
│   ├── device_test.py
│   ├── etl_test.py
│   ├── integration_engine_test.py
│   ├── queue_test.py
│   └── retry_test.py
│
└── requirements.txt
