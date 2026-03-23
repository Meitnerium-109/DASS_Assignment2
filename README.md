# DASS Assignment 2

## GitHub Repository
**Git Repository Link:** [INSERT YOUR REPO LINK HERE]

This directory contains the deliverables for Assignment 2, organized by the three testing strategies.

## Running the Tests & Code

You will need `pytest` and `requests` installed across the suite (`pip install pytest pytest-cov requests`).

### Part 1: White Box Testing (MoneyPoly)
* **Run Code:** Standard Python execution from the root of the project:
  ```bash
  python3 -m moneypoly.main
  ```
* **Run Tests:** Go to `whitebox/tests/` and run `pytest`:
  ```bash
  cd whitebox/tests
  PYTHONPATH=../code/moneypoly pytest -v test_moneypoly.py
  ```

### Part 2: Integration Testing (StreetRace Manager)
* **Run Tests:** Go to `integration/tests/` and run `pytest`:
  ```bash
  cd integration/tests
  PYTHONPATH=../code pytest -v test_streetrace_integration.py
  ```

### Part 3: Black Box API Testing (QuickCart)
* **Run API Server (Docker required):**
  ```bash
  cd blackbox
  docker load -i quickcart_image_x86.tar
  docker run -d -p 8080:8080 quickcart
  ```
* **Run Tests:** Go to `blackbox/tests/` and run `pytest`:
  ```bash
  cd blackbox/tests
  pytest -v test_quickcart.py
  ```

---

## Deliverable Structure

* `whitebox/`: Pylint refactored codebase (`code/`), whitebox paths (`tests/`), node flow paths (`diagrams/`), and bugs (`report.pdf`).
* `integration/`: StreetRace Manager implementation (`code/`), component checks (`tests/`), method invocations (`diagrams/`), and integration specs (`report.pdf`).
* `blackbox/`: Automations against the Docker API (`tests/`), and JSON validation failures captured in `report.pdf`.
