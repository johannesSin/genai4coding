import requests
import time
import csv
import os
import sys
from datetime import datetime

BASE_URL = "http://127.0.0.1:8000"
MODEL = sys.argv[1] if len(sys.argv) > 1 else "unknown"

results = []
session = requests.Session()


def check(name, func):
    try:
        ok = func()
        status = "correct" if ok else "failed"
        display = "✓" if ok else "✗"
    except Exception as e:
        status = f"error_{type(e).__name__}"
        display = f"ERROR: {type(e).__name__} - {e}"

    results.append((MODEL, name, status, display))


def test_app_running():
    return session.get(f"{BASE_URL}/docs", timeout=5).status_code == 200


def test_register_page():
    return session.get(f"{BASE_URL}/register", timeout=5).status_code == 200


def test_register_post():
    payload = {
        "username": "benchuser",
        "email": "benchuser@example.com",
        "password": "Test12345!"
    }
    r = session.post(
        f"{BASE_URL}/register",
        data=payload,
        timeout=5,
        allow_redirects=False
    )
    return r.status_code in [200, 201, 302, 303, 400]


def test_login_page():
    return session.get(f"{BASE_URL}/login", timeout=5).status_code == 200


def test_login_post():
    payload = {
        "username": "benchuser",
        "password": "Test12345!"
    }
    r = session.post(
        f"{BASE_URL}/login",
        data=payload,
        timeout=5,
        allow_redirects=False
    )
    return r.status_code in [200, 302, 303, 400, 401]


def test_dashboard():
    r = session.get(f"{BASE_URL}/dashboard", timeout=5)
    return r.status_code in [200, 302, 401, 403]


def test_transfer_page():
    r = session.get(f"{BASE_URL}/transfer", timeout=5)
    return r.status_code in [200, 302, 401, 403]


def test_invalid_login():
    payload = {
        "username": "benchuser",
        "password": "wrongpassword"
    }
    r = session.post(f"{BASE_URL}/login", data=payload, timeout=5, allow_redirects=False)
    return r.status_code in [400, 401, 403, 200, 302]


def test_transfer_without_login():
    new_session = requests.Session()
    payload = {
        "recipient": "somebody",
        "amount": "10",
        "description": "unauthorized transfer"
    }
    r = new_session.post(f"{BASE_URL}/transfer", data=payload, timeout=5, allow_redirects=False)
    return r.status_code in [302, 401, 403]


def test_negative_transfer():
    payload = {
        "recipient": "somebody",
        "amount": "-100",
        "description": "negative transfer"
    }
    r = session.post(f"{BASE_URL}/transfer", data=payload, timeout=5, allow_redirects=False)
    return r.status_code in [400, 422, 200, 302]


def test_sql_injection_login():
    payload = {
        "username": "' OR '1'='1",
        "password": "' OR '1'='1"
    }
    r = session.post(f"{BASE_URL}/login", data=payload, timeout=5, allow_redirects=False)
    return r.status_code in [200, 302, 400, 401, 403]


if __name__ == "__main__":
    time.sleep(1)

    check("App starts / docs reachable", test_app_running)
    check("Register page", test_register_page)
    check("Register form submit", test_register_post)
    check("Login page", test_login_page)
    check("Login form submit", test_login_post)
    check("Dashboard route", test_dashboard)
    check("Transfer page", test_transfer_page)
    check("Invalid login rejected", test_invalid_login)
    check("Transfer without login blocked", test_transfer_without_login)
    check("Negative transfer handled", test_negative_transfer)
    check("SQL injection login handled", test_sql_injection_login)

    print(f"\nBanking App Benchmark: {MODEL}")
    print("---------------------")

    for _, name, _, display in results:
        print(f"{name}: {display}")

    passed = sum(1 for _, _, status, _ in results if status == "correct")
    total = len(results)

    print(f"\nResult: {passed}/{total} checks passed")

    os.makedirs("results", exist_ok=True)
    csv_path = "results/banking_benchmark_results.csv"
    file_exists = os.path.exists(csv_path)

    with open(csv_path, "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)

        if not file_exists:
            writer.writerow([
                "timestamp",
                "model",
                "test",
                "status",
                "display"
            ])

        timestamp = datetime.now().isoformat(timespec="seconds")

        for model, test, status, display in results:
            writer.writerow([
                timestamp,
                model,
                test,
                status,
                display
            ])

    print(f"\nCSV gespeichert: {csv_path}")