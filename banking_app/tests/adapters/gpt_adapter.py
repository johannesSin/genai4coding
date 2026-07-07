import re
from html.parser import HTMLParser
from typing import Any

import requests

from .base import BankingAdapter


class AccountOptionParser(HTMLParser):
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

        match = re.search(
            r"\bDEMO[A-Z0-9]+\b",
            text,
            flags=re.IGNORECASE,
        )

        if self.current_value and match:
            self.accounts.append(
                {
                    "id": self.current_value,
                    "number": match.group(0),
                    "text": text,
                }
            )

        self.in_option = False
        self.current_value = ""
        self.current_text = []


class GPTAdapter(BankingAdapter):
    def __init__(
        self,
        base_url: str,
        timeout_seconds: int,
    ) -> None:
        super().__init__(base_url, timeout_seconds)
        self.session = requests.Session()

    @staticmethod
    def body_excerpt(
        response: requests.Response,
        limit: int = 500,
    ) -> str:
        text = " ".join(response.text.split())
        return text[:limit]

    def result(
        self,
        passed: bool,
        expected: str,
        observed: str,
        response: requests.Response | None = None,
    ) -> dict[str, Any]:
        data: dict[str, Any] = {
            "passed": passed,
            "expected": expected,
            "observed": observed,
            "actual_status": "",
            "actual_url": "",
            "redirect_location": "",
            "body_excerpt": "",
        }

        if response is not None:
            data.update(
                {
                    "actual_status": response.status_code,
                    "actual_url": response.url,
                    "redirect_location": response.headers.get(
                        "Location",
                        "",
                    ),
                    "body_excerpt": self.body_excerpt(response),
                }
            )

        return data

    def extract_accounts(
        self,
    ) -> tuple[requests.Response, list[dict[str, str]]]:
        response = self.session.get(
            f"{self.base_url}/transfer",
            timeout=self.timeout_seconds,
            allow_redirects=False,
        )

        parser = AccountOptionParser()
        parser.feed(response.text)

        return response, parser.accounts

    def app_running(self) -> dict[str, Any]:
        response = self.session.get(
            f"{self.base_url}/docs",
            timeout=self.timeout_seconds,
        )

        return self.result(
            response.status_code == 200,
            "Die Anwendung ist erreichbar und /docs liefert HTTP 200.",
            f"/docs lieferte HTTP {response.status_code}.",
            response,
        )

    def register_page(self) -> dict[str, Any]:
        response = self.session.get(
            f"{self.base_url}/register",
            timeout=self.timeout_seconds,
        )

        return self.result(
            response.status_code == 200,
            "Die Registrierungsseite ist erreichbar.",
            f"/register lieferte HTTP {response.status_code}.",
            response,
        )

    def register_user(
        self,
        username: str,
        email: str,
        password: str,
    ) -> dict[str, Any]:
        response = self.session.post(
            f"{self.base_url}/register",
            data={
                "username": username,
                "email": email,
                "password": password,
            },
            timeout=self.timeout_seconds,
            allow_redirects=False,
        )

        redirect = response.headers.get("Location", "")
        passed = (
            response.status_code in {302, 303}
            and redirect == "/dashboard"
        )

        return self.result(
            passed,
            (
                "Ein neuer Benutzer wird registriert und zum "
                "Dashboard weitergeleitet."
            ),
            (
                f"Registrierung: HTTP {response.status_code}; "
                f"Redirect: {redirect or '-'}"
            ),
            response,
        )

    def login_page(self) -> dict[str, Any]:
        response = self.session.get(
            f"{self.base_url}/login",
            timeout=self.timeout_seconds,
        )

        return self.result(
            response.status_code == 200,
            "Die Loginseite ist erreichbar.",
            f"/login lieferte HTTP {response.status_code}.",
            response,
        )

    def login_user(
        self,
        username: str,
        email: str,
        password: str,
    ) -> dict[str, Any]:
        self.session.cookies.clear()

        response = self.session.post(
            f"{self.base_url}/login",
            data={
                "username": username,
                "password": password,
            },
            timeout=self.timeout_seconds,
            allow_redirects=False,
        )

        redirect = response.headers.get("Location", "")
        passed = (
            response.status_code in {302, 303}
            and redirect == "/dashboard"
        )

        return self.result(
            passed,
            (
                "Gültige Zugangsdaten erzeugen eine "
                "authentifizierte Sitzung."
            ),
            (
                f"Login: HTTP {response.status_code}; "
                f"Redirect: {redirect or '-'}"
            ),
            response,
        )

    def dashboard(self) -> dict[str, Any]:
        response = self.session.get(
            f"{self.base_url}/dashboard",
            timeout=self.timeout_seconds,
            allow_redirects=False,
        )

        return self.result(
            response.status_code == 200,
            "Das Dashboard ist nach erfolgreichem Login erreichbar.",
            (
                f"/dashboard lieferte HTTP {response.status_code}; "
                f"Redirect: "
                f"{response.headers.get('Location', '-')}"
            ),
            response,
        )

    def transfer_page(self) -> dict[str, Any]:
        response, accounts = self.extract_accounts()

        passed = (
            response.status_code == 200
            and len(accounts) >= 1
        )

        return self.result(
            passed,
            (
                "Die Überweisungsseite ist erreichbar und zeigt "
                "mindestens ein Quellkonto."
            ),
            (
                f"/transfer lieferte HTTP {response.status_code}; "
                f"erkannte Konten: {len(accounts)}"
            ),
            response,
        )

    def invalid_login(
        self,
        username: str,
        email: str,
    ) -> dict[str, Any]:
        test_session = requests.Session()

        login_response = test_session.post(
            f"{self.base_url}/login",
            data={
                "username": username,
                "password": "wrongpassword",
            },
            timeout=self.timeout_seconds,
            allow_redirects=False,
        )

        dashboard_response = test_session.get(
            f"{self.base_url}/dashboard",
            timeout=self.timeout_seconds,
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

        result = self.result(
            login_rejected and dashboard_blocked,
            (
                "Ungültige Zugangsdaten werden abgelehnt und "
                "erzeugen keine Sitzung."
            ),
            (
                f"Login: HTTP {login_response.status_code}; "
                f"Dashboard danach: HTTP "
                f"{dashboard_response.status_code}; "
                f"Redirect: "
                f"{dashboard_response.headers.get('Location', '-')}"
            ),
            login_response,
        )

        result["body_excerpt"] = (
            f"Login: {self.body_excerpt(login_response)} | "
            f"Dashboard: {self.body_excerpt(dashboard_response)}"
        )

        return result

    def transfer_without_login(self) -> dict[str, Any]:
        test_session = requests.Session()

        response = test_session.post(
            f"{self.base_url}/transfer",
            data={
                "from_account_id": "1",
                "to_account_number": "DEMO00000000",
                "amount": "10",
                "reference": "unauthorized transfer",
            },
            timeout=self.timeout_seconds,
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

        return self.result(
            blocked,
            "Eine Überweisung ohne Login wird verweigert.",
            (
                f"HTTP {response.status_code}; "
                f"Redirect: {redirect or '-'}"
            ),
            response,
        )

    def negative_transfer(self) -> dict[str, Any]:
        transfer_page, accounts = self.extract_accounts()

        if transfer_page.status_code != 200:
            return self.result(
                False,
                "Die Überweisungsseite muss erreichbar sein.",
                (
                    f"/transfer lieferte HTTP "
                    f"{transfer_page.status_code}."
                ),
                transfer_page,
            )

        if len(accounts) < 2:
            return self.result(
                False,
                "Mindestens zwei Konten werden benötigt.",
                f"Es wurden {len(accounts)} Konten erkannt.",
                transfer_page,
            )

        source = accounts[0]
        target = accounts[1]

        response = self.session.post(
            f"{self.base_url}/transfer",
            data={
                "from_account_id": source["id"],
                "to_account_number": target["number"],
                "amount": "-100",
                "reference": "negative transfer",
            },
            timeout=self.timeout_seconds,
            allow_redirects=False,
        )

        body = response.text.lower()

        rejection_terms = [
            "positiv",
            "größer als 0",
            "must be positive",
            "ungültig",
            "invalid",
            "negativ",
            "negative",
            "fehler",
            "error",
        ]

        rejected_by_content = any(
            term in body
            for term in rejection_terms
        )

        passed = (
            response.status_code in {400, 422}
            and rejected_by_content
        )

        return self.result(
            passed,
            "Ein negativer Überweisungsbetrag wird abgelehnt.",
            (
                f"Quellkonto {source['id']}; "
                f"Zielkonto {target['number']}; "
                f"HTTP {response.status_code}; "
                f"Fehlermeldung erkannt: "
                f"{rejected_by_content}"
            ),
            response,
        )

    def sql_injection_login(self) -> dict[str, Any]:
        test_session = requests.Session()

        login_response = test_session.post(
            f"{self.base_url}/login",
            data={
                "username": "' OR '1'='1",
                "password": "' OR '1'='1",
            },
            timeout=self.timeout_seconds,
            allow_redirects=False,
        )

        dashboard_response = test_session.get(
            f"{self.base_url}/dashboard",
            timeout=self.timeout_seconds,
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

        result = self.result(
            login_rejected and dashboard_blocked,
            (
                "SQL-Injection führt nicht zu einer "
                "authentifizierten Sitzung."
            ),
            (
                f"Login: HTTP {login_response.status_code}; "
                f"Dashboard danach: HTTP "
                f"{dashboard_response.status_code}"
            ),
            login_response,
        )

        result["body_excerpt"] = (
            f"Login: {self.body_excerpt(login_response)} | "
            f"Dashboard: {self.body_excerpt(dashboard_response)}"
        )

        return result