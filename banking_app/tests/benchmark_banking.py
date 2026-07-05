import csv
import os
import re
import sys
import time
from datetime import datetime
from html.parser import HTMLParser
from typing import Any, Callable

import requests


BASE_URL = "http://127.0.0.1:8000"
MODEL = sys.argv[1] if len(sys.argv) > 1 else "unknown"
TIMEOUT_SECONDS = 5

# Eindeutige Zugangsdaten pro Testlauf.
RUN_ID = datetime.now().strftime("%Y%m%d%H%M%S")
TEST_USERNAME = f"bench_{MODEL}_{RUN_ID}"
TEST_EMAIL = f"{TEST_USERNAME}@example.com"
TEST_PASSWORD = "Test12345!"

session = requests.Session()
results: list[dict[str, Any]] = []


class AccountOptionParser(HTMLParser):
    """Liest Konten aus den <option>-Elementen der Überweisungsseite."""

    def __init__(self) -> None:
        super().__init__()
        self.in_option = False
        self.current_value = ""
        self.current_text: list[str] = []
        self.accounts: list[dict[str, str]] = []

    def handle_starttag(
        self,
        tag: str,
        attrs: list[tuple[str, str | None]],
    ) -> None:
        if tag.lower() != "option":
            return

        self.in_option = True
        self.current_text = []
        attributes = dict(attrs)
        self.current_value = attributes.get("value") or ""

    def handle_data(self, data: str) -> None:
        if self.in_option:
            self.current_text.append(data)

    def handle_endtag(self, tag: str) -> None:
        if tag.lower() != "option" or not self.in_option:
            return

        text = " ".join("".join(self.current_text).split())

        account_number_match = re.search(
            r"\bDEMO[A-Z0-9]+\b",
            text,
            flags=re.IGNORECASE,
        )

        if self.current_value and account_number_match:
            self.accounts.append(
                {
                    "id": self.current_value,
                    "number": account_number_match.group(0),
                    "text": text,
                }
            )

        self.in_option = False
        self.current_value = ""
        self.current_text = []


def body_excerpt(response: requests.Response, limit: int = 500) -> str:
    """Erzeugt einen kompakten Auszug aus dem Antworttext."""

    text = " ".join(response.text.split())
    return text[:limit]


def response_details(response: requests.Response) -> dict[str, Any]:
    return {
        "actual_status": response.status_code,
        "actual_url": response.url,
        "redirect_location": response.headers.get("Location", ""),
        "body_excerpt": body_excerpt(response),
    }


def make_result(
    passed: bool,
    expected: str,
    observed: str,
    response: requests.Response | None = None,
) -> dict[str, Any]:
    result: dict[str, Any] = {
        "passed": passed,
        "expected": expected,
        "observed": observed,
        "actual_status": "",
        "actual_url": "",
        "redirect_location": "",
        "body_excerpt": "",
    }

    if response is not None:
        result.update(response_details(response))

    return result


def check(
    name: str,
    func: Callable[[], dict[str, Any]],
) -> None:
    try:
        result = func()

        if not isinstance(result, dict) or "passed" not in result:
            raise TypeError(
                f"{func.__name__} lieferte kein gültiges Ergebnisobjekt."
            )

        status = "correct" if result["passed"] else "failed"
        error = ""

    except Exception as exc:
        result = {
            "expected": "Der Test sollte ohne technische Ausnahme laufen.",
            "observed": f"{type(exc).__name__}: {exc}",
            "actual_status": "",
            "actual_url": "",
            "redirect_location": "",
            "body_excerpt": "",
        }

        status = f"error_{type(exc).__name__}"
        error = f"{type(exc).__name__}: {exc}"

    results.append(
        {
            "model": MODEL,
            "test": name,
            "expected": result.get("expected", ""),
            "actual_status": result.get("actual_status", ""),
            "actual_url": result.get("actual_url", ""),
            "redirect_location": result.get(
                "redirect_location",
                "",
            ),
            "observed_behavior": result.get("observed", ""),
            "body_excerpt": result.get("body_excerpt", ""),
            "status": status,
            "error": error,
        }
    )


def extract_accounts_from_transfer_page() -> tuple[
    requests.Response,
    list[dict[str, str]],
]:
    response = session.get(
        f"{BASE_URL}/transfer",
        timeout=TIMEOUT_SECONDS,
        allow_redirects=False,
    )

    parser = AccountOptionParser()
    parser.feed(response.text)

    return response, parser.accounts


def test_app_running() -> dict[str, Any]:
    response = session.get(
        f"{BASE_URL}/docs",
        timeout=TIMEOUT_SECONDS,
    )

    return make_result(
        response.status_code == 200,
        "Die Anwendung ist erreichbar und /docs liefert HTTP 200.",
        f"/docs lieferte HTTP {response.status_code}.",
        response,
    )


def test_register_page() -> dict[str, Any]:
    response = session.get(
        f"{BASE_URL}/register",
        timeout=TIMEOUT_SECONDS,
    )

    return make_result(
        response.status_code == 200,
        "Die Registrierungsseite ist erreichbar und liefert HTTP 200.",
        f"/register lieferte HTTP {response.status_code}.",
        response,
    )


def test_register_post() -> dict[str, Any]:
    response = session.post(
        f"{BASE_URL}/register",
        data={
            "username": TEST_USERNAME,
            "email": TEST_EMAIL,
            "password": TEST_PASSWORD,
        },
        timeout=TIMEOUT_SECONDS,
        allow_redirects=False,
    )

    redirect = response.headers.get("Location", "")
    passed = (
        response.status_code in {302, 303}
        and redirect == "/dashboard"
    )

    return make_result(
        passed,
        (
            "Ein neuer Benutzer wird registriert und anschließend "
            "zum Dashboard weitergeleitet."
        ),
        (
            f"Registrierung von {TEST_USERNAME}: "
            f"HTTP {response.status_code}; "
            f"Redirect: {redirect or '-'}"
        ),
        response,
    )


def test_login_page() -> dict[str, Any]:
    response = session.get(
        f"{BASE_URL}/login",
        timeout=TIMEOUT_SECONDS,
    )

    return make_result(
        response.status_code == 200,
        "Die Loginseite ist erreichbar und liefert HTTP 200.",
        f"/login lieferte HTTP {response.status_code}.",
        response,
    )


def test_login_post() -> dict[str, Any]:
    # Registrierung meldet den Benutzer bereits an.
    # Cookies werden gelöscht, damit der Login eigenständig geprüft wird.
    session.cookies.clear()

    response = session.post(
        f"{BASE_URL}/login",
        data={
            "username": TEST_USERNAME,
            "password": TEST_PASSWORD,
        },
        timeout=TIMEOUT_SECONDS,
        allow_redirects=False,
    )

    redirect = response.headers.get("Location", "")
    passed = (
        response.status_code in {302, 303}
        and redirect == "/dashboard"
    )

    return make_result(
        passed,
        (
            "Gültige Zugangsdaten erzeugen eine authentifizierte "
            "Sitzung und führen zum Dashboard."
        ),
        (
            f"Login von {TEST_USERNAME}: "
            f"HTTP {response.status_code}; "
            f"Redirect: {redirect or '-'}"
        ),
        response,
    )


def test_dashboard() -> dict[str, Any]:
    response = session.get(
        f"{BASE_URL}/dashboard",
        timeout=TIMEOUT_SECONDS,
        allow_redirects=False,
    )

    passed = response.status_code == 200

    return make_result(
        passed,
        "Das Dashboard ist nach erfolgreicher Anmeldung erreichbar.",
        (
            f"/dashboard lieferte HTTP {response.status_code}; "
            f"Redirect: "
            f"{response.headers.get('Location', '-')}"
        ),
        response,
    )


def test_transfer_page() -> dict[str, Any]:
    response, accounts = extract_accounts_from_transfer_page()

    passed = response.status_code == 200 and len(accounts) >= 1

    return make_result(
        passed,
        (
            "Die Überweisungsseite ist nach der Anmeldung erreichbar "
            "und zeigt mindestens ein Quellkonto."
        ),
        (
            f"/transfer lieferte HTTP {response.status_code}; "
            f"erkannte Konten: {len(accounts)}; "
            f"Redirect: "
            f"{response.headers.get('Location', '-')}"
        ),
        response,
    )


def test_invalid_login() -> dict[str, Any]:
    test_session = requests.Session()

    login_response = test_session.post(
        f"{BASE_URL}/login",
        data={
            "username": TEST_USERNAME,
            "password": "wrongpassword",
        },
        timeout=TIMEOUT_SECONDS,
        allow_redirects=False,
    )

    dashboard_response = test_session.get(
        f"{BASE_URL}/dashboard",
        timeout=TIMEOUT_SECONDS,
        allow_redirects=False,
    )

    login_rejected = login_response.status_code in {
        400,
        401,
        403,
    }

    dashboard_blocked = dashboard_response.status_code in {
        302,
        303,
        401,
        403,
    }

    passed = login_rejected and dashboard_blocked

    result = make_result(
        passed,
        (
            "Ungültige Zugangsdaten werden abgelehnt und erzeugen "
            "keine authentifizierte Sitzung."
        ),
        (
            f"Ungültiger Login: HTTP "
            f"{login_response.status_code}, "
            f"Redirect "
            f"{login_response.headers.get('Location', '-')}; "
            f"Dashboard danach: HTTP "
            f"{dashboard_response.status_code}, "
            f"Redirect "
            f"{dashboard_response.headers.get('Location', '-')}"
        ),
        login_response,
    )

    result["body_excerpt"] = (
        f"Login: {body_excerpt(login_response)} | "
        f"Dashboard: {body_excerpt(dashboard_response)}"
    )

    return result


def test_transfer_without_login() -> dict[str, Any]:
    test_session = requests.Session()

    response = test_session.post(
        f"{BASE_URL}/transfer",
        data={
            "from_account_id": "1",
            "to_account_number": "DEMO00000000",
            "amount": "10",
            "reference": "unauthorized transfer",
        },
        timeout=TIMEOUT_SECONDS,
        allow_redirects=False,
    )

    redirect = response.headers.get("Location", "")

    blocked = (
        response.status_code in {302, 303, 401, 403}
        and (
            response.status_code in {401, 403}
            or redirect == "/login"
        )
    )

    return make_result(
        blocked,
        (
            "Eine Überweisung ohne authentifizierte Sitzung wird "
            "verweigert oder zur Loginseite umgeleitet."
        ),
        (
            f"Transfer ohne Login: HTTP "
            f"{response.status_code}; "
            f"Redirect: {redirect or '-'}"
        ),
        response,
    )


def test_negative_transfer() -> dict[str, Any]:
    transfer_page, accounts = extract_accounts_from_transfer_page()

    if transfer_page.status_code != 200:
        return make_result(
            False,
            (
                "Die Überweisungsseite muss für den angemeldeten "
                "Benutzer erreichbar sein."
            ),
            (
                f"Die Überweisungsseite lieferte HTTP "
                f"{transfer_page.status_code}."
            ),
            transfer_page,
        )

    if len(accounts) < 2:
        return make_result(
            False,
            (
                "Für den Test werden mindestens zwei vorhandene "
                "Konten benötigt."
            ),
            f"Es wurden nur {len(accounts)} Konten erkannt.",
            transfer_page,
        )

    source_account = accounts[0]
    target_account = accounts[1]

    response = session.post(
        f"{BASE_URL}/transfer",
        data={
            "from_account_id": source_account["id"],
            "to_account_number": target_account["number"],
            "amount": "-100",
            "reference": "negative transfer",
        },
        timeout=TIMEOUT_SECONDS,
        allow_redirects=False,
    )

    body = response.text.lower()

    rejection_terms = [
        "positiv",
        "größer als 0",
        "greater than zero",
        "must be positive",
        "ungültig",
        "invalid",
        "negativ",
        "negative",
        "fehler",
        "error",
    ]

    rejected_by_status = response.status_code in {
        400,
        422,
    }

    rejected_by_content = any(
        term in body
        for term in rejection_terms
    )

    # HTTP 400 mit einer erkennbaren Fehlermeldung ist die erwartete
    # fachliche Ablehnung. HTTP 422 ist nur akzeptabel, wenn der
    # Antworttext den negativen Betrag tatsächlich thematisiert.
    passed = (
        response.status_code == 400
        and rejected_by_content
    ) or (
        response.status_code == 422
        and rejected_by_content
    )

    return make_result(
        passed,
        (
            "Ein vollständig formulierter Transfer mit negativem "
            "Betrag wird fachlich abgelehnt."
        ),
        (
            f"Quellkonto {source_account['id']}; "
            f"Zielkonto {target_account['number']}; "
            f"HTTP {response.status_code}; "
            f"Fehlermeldung erkannt: "
            f"{rejected_by_content}; "
            f"Redirect: "
            f"{response.headers.get('Location', '-')}"
        ),
        response,
    )


def test_sql_injection_login() -> dict[str, Any]:
    test_session = requests.Session()

    login_response = test_session.post(
        f"{BASE_URL}/login",
        data={
            "username": "' OR '1'='1",
            "password": "' OR '1'='1",
        },
        timeout=TIMEOUT_SECONDS,
        allow_redirects=False,
    )

    dashboard_response = test_session.get(
        f"{BASE_URL}/dashboard",
        timeout=TIMEOUT_SECONDS,
        allow_redirects=False,
    )

    login_rejected = login_response.status_code in {
        400,
        401,
        403,
    }

    dashboard_blocked = dashboard_response.status_code in {
        302,
        303,
        401,
        403,
    }

    passed = login_rejected and dashboard_blocked

    result = make_result(
        passed,
        (
            "Die SQL-Injection-Eingabe wird abgelehnt und führt "
            "nicht zu einer authentifizierten Sitzung."
        ),
        (
            f"SQL-Injection-Login: HTTP "
            f"{login_response.status_code}, "
            f"Redirect "
            f"{login_response.headers.get('Location', '-')}; "
            f"Dashboard danach: HTTP "
            f"{dashboard_response.status_code}, "
            f"Redirect "
            f"{dashboard_response.headers.get('Location', '-')}"
        ),
        login_response,
    )

    result["body_excerpt"] = (
        f"Login: {body_excerpt(login_response)} | "
        f"Dashboard: {body_excerpt(dashboard_response)}"
    )

    return result


def write_results() -> str:
    os.makedirs("banking_app/results", exist_ok=True)

    csv_path = (
        "banking_app/results/"
        "banking_benchmark_detailed_results.csv"
    )

    file_exists = os.path.exists(csv_path)

    fieldnames = [
        "timestamp",
        "model",
        "test",
        "expected",
        "actual_status",
        "actual_url",
        "redirect_location",
        "observed_behavior",
        "body_excerpt",
        "status",
        "error",
    ]

    with open(
        csv_path,
        "a",
        newline="",
        encoding="utf-8",
    ) as file:
        writer = csv.DictWriter(
            file,
            fieldnames=fieldnames,
        )

        if not file_exists:
            writer.writeheader()

        timestamp = datetime.now().isoformat(
            timespec="seconds"
        )

        for result in results:
            writer.writerow(
                {
                    "timestamp": timestamp,
                    **result,
                }
            )

    return csv_path


def print_results() -> None:
    print(f"\nBanking App Benchmark: {MODEL}")
    print("-" * 70)

    for result in results:
        symbol = (
            "✓"
            if result["status"] == "correct"
            else "✗"
        )

        print(
            f"{symbol} {result['test']}\n"
            f"  Status: {result['status']}\n"
            f"  Beobachtung: "
            f"{result['observed_behavior']}"
        )

        if result["error"]:
            print(f"  Fehler: {result['error']}")

    passed = sum(
        1
        for result in results
        if result["status"] == "correct"
    )

    total = len(results)

    print("-" * 70)
    print(f"Result: {passed}/{total} checks passed")


if __name__ == "__main__":
    time.sleep(1)

    check(
        "App starts / docs reachable",
        test_app_running,
    )
    check(
        "Register page",
        test_register_page,
    )
    check(
        "Register form submit",
        test_register_post,
    )
    check(
        "Login page",
        test_login_page,
    )
    check(
        "Login form submit",
        test_login_post,
    )
    check(
        "Dashboard route",
        test_dashboard,
    )
    check(
        "Transfer page",
        test_transfer_page,
    )
    check(
        "Invalid login rejected",
        test_invalid_login,
    )
    check(
        "Transfer without login blocked",
        test_transfer_without_login,
    )
    check(
        "Negative transfer handled",
        test_negative_transfer,
    )
    check(
        "SQL injection login handled",
        test_sql_injection_login,
    )

    print_results()
    output_path = write_results()

    print(
        "\nDetailliertes Testprotokoll gespeichert:"
    )
    print(output_path)