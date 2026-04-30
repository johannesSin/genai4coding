import requests
import time

BASE_URL = "http://127.0.0.1:8000"

results = []


def check(name, func):
    try:
        ok = func()
        results.append((name, "✓" if ok else "✗"))
    except Exception as e:
        results.append((name, f"ERROR: {type(e).__name__}"))


def test_app_running():
    r = requests.get(f"{BASE_URL}/docs", timeout=5)
    return r.status_code == 200


def test_register():
    payload = {
        "username": "testuser",
        "email": "testuser@example.com",
        "password": "Test12345!"
    }

    r = requests.post(f"{BASE_URL}/register", json=payload, timeout=5)
    return r.status_code in [200, 201, 400]


def test_login():
    payload = {
        "username": "testuser",
        "password": "Test12345!"
    }

    r = requests.post(f"{BASE_URL}/login", json=payload, timeout=5)
    return r.status_code in [200, 201]


def test_accounts():
    r = requests.get(f"{BASE_URL}/accounts", timeout=5)
    return r.status_code in [200, 401, 403]


def test_transactions():
    r = requests.get(f"{BASE_URL}/transactions", timeout=5)
    return r.status_code in [200, 401, 403]


def test_transfer():
    payload = {
        "recipient": "testuser2",
        "amount": 10,
        "description": "Benchmark transfer"
    }

    r = requests.post(f"{BASE_URL}/transfer", json=payload, timeout=5)
    return r.status_code in [200, 201, 400, 401, 403]


if __name__ == "__main__":
    time.sleep(1)

    check("App starts / docs reachable", test_app_running)
    check("Register endpoint", test_register)
    check("Login endpoint", test_login)
    check("Accounts endpoint", test_accounts)
    check("Transactions endpoint", test_transactions)
    check("Transfer endpoint", test_transfer)

    print("\nBanking App Benchmark")
    print("---------------------")

    for name, status in results:
        print(f"{name}: {status}")

    passed = sum(1 for _, status in results if status == "✓")
    total = len(results)

    print(f"\nResult: {passed}/{total} checks passed")