import re
from typing import Any

import requests

from .base import BankingAdapter


class GeminiAdapter(BankingAdapter):
    def __init__(
        self,
        base_url: str,
        timeout_seconds: int,
    ) -> None:
        super().__init__(base_url, timeout_seconds)

        self.session = requests.Session()
        self.user_id: int | None = None

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

    @staticmethod
    def extract_balance(html: str) -> float | None:
        match = re.search(
            r"Kontostand:\s*<strong>\s*"
            r"(-?\d+(?:[.,]\d+)?)\s*€",
            html,
            flags=re.IGNORECASE,
        )

        if not match:
            return None

        value = match.group(1).replace(",", ".")

        try:
            return float(value)
        except ValueError:
            return None

    def app_running(self) -> dict[str, Any]:
        response = self.session.get(
            f"{self.base_url}/docs",
            timeout=self.timeout_seconds,
        )

        return self.result(
            response.status_code == 200,
            (
                "Die Anwendung ist erreichbar und die "
                "API-Dokumentation liefert HTTP 200."
            ),
            f"/docs lieferte HTTP {response.status_code}.",
            response,
        )

    def register_page(self) -> dict[str, Any]:
        response = self.session.get(
            f"{self.base_url}/",
            timeout=self.timeout_seconds,
        )

        body = response.text.lower()

        form_visible = (
            response.status_code == 200
            and 'action="/register"' in body
            and 'name="username"' in body
            and 'name="password"' in body
        )

        return self.result(
            form_visible,
            (
                "Die Startseite ist erreichbar und enthält ein "
                "Registrierungsformular."
            ),
            (
                f"/ lieferte HTTP {response.status_code}; "
                f"Registrierungsformular erkannt: {form_visible}"
            ),
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
                "password": password,
            },
            timeout=self.timeout_seconds,
            allow_redirects=False,
        )

        redirect = response.headers.get("Location", "")

        passed = (
            response.status_code in {302, 303}
            and redirect == "/"
        )

        return self.result(
            passed,
            (
                "Ein neuer Benutzer wird registriert und "
                "anschließend zur Startseite weitergeleitet."
            ),
            (
                f"Registrierung: HTTP {response.status_code}; "
                f"Redirect: {redirect or '-'}"
            ),
            response,
        )

    def login_page(self) -> dict[str, Any]:
        response = self.session.get(
            f"{self.base_url}/",
            timeout=self.timeout_seconds,
        )

        body = response.text.lower()

        form_visible = (
            response.status_code == 200
            and 'action="/login"' in body
            and 'name="username"' in body
            and 'name="password"' in body
        )

        return self.result(
            form_visible,
            (
                "Die Startseite ist erreichbar und enthält ein "
                "Loginformular."
            ),
            (
                f"/ lieferte HTTP {response.status_code}; "
                f"Loginformular erkannt: {form_visible}"
            ),
            response,
        )

    def login_user(
        self,
        username: str,
        email: str,
        password: str,
    ) -> dict[str, Any]:
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

        match = re.fullmatch(
            r"/dashboard/(\d+)",
            redirect,
        )

        if match:
            self.user_id = int(match.group(1))

        passed = (
            response.status_code in {302, 303}
            and self.user_id is not None
        )

        return self.result(
            passed,
            (
                "Gültige Zugangsdaten führen zum Dashboard des "
                "registrierten Benutzers."
            ),
            (
                f"Login: HTTP {response.status_code}; "
                f"Redirect: {redirect or '-'}; "
                f"user_id: {self.user_id or '-'}"
            ),
            response,
        )

    def dashboard(self) -> dict[str, Any]:
        if self.user_id is None:
            return self.result(
                False,
                "Nach dem Login muss eine Benutzer-ID vorliegen.",
                "Es wurde keine Benutzer-ID aus dem Login ermittelt.",
            )

        response = self.session.get(
            f"{self.base_url}/dashboard/{self.user_id}",
            timeout=self.timeout_seconds,
            allow_redirects=False,
        )

        body = response.text.lower()

        dashboard_visible = (
            response.status_code == 200
            and "kontostand" in body
            and "neue überweisung" in body
        )

        return self.result(
            dashboard_visible,
            (
                "Das Dashboard ist nach erfolgreichem Login "
                "erreichbar."
            ),
            (
                f"/dashboard/{self.user_id} lieferte HTTP "
                f"{response.status_code}; "
                f"Dashboard erkannt: {dashboard_visible}"
            ),
            response,
        )

    def transfer_page(self) -> dict[str, Any]:
        if self.user_id is None:
            return self.result(
                False,
                "Für die Überweisungsseite muss eine Benutzer-ID vorliegen.",
                "Es wurde keine Benutzer-ID ermittelt.",
            )

        response = self.session.get(
            f"{self.base_url}/dashboard/{self.user_id}",
            timeout=self.timeout_seconds,
        )

        body = response.text.lower()

        transfer_form_visible = (
            response.status_code == 200
            and f'action="/transfer/{self.user_id}"' in body
            and 'name="recipient"' in body
            and 'name="amount"' in body
        )

        return self.result(
            transfer_form_visible,
            (
                "Das Dashboard enthält eine erreichbare "
                "Überweisungsfunktion."
            ),
            (
                f"Dashboard: HTTP {response.status_code}; "
                f"Transferformular erkannt: "
                f"{transfer_form_visible}"
            ),
            response,
        )

    def invalid_login(
        self,
        username: str,
        email: str,
    ) -> dict[str, Any]:
        response = requests.post(
            f"{self.base_url}/login",
            data={
                "username": username,
                "password": "wrongpassword",
            },
            timeout=self.timeout_seconds,
            allow_redirects=False,
        )

        body = response.text.lower()

        rejected = (
            response.status_code in {400, 401, 403}
            and (
                "fehlgeschlagen" in body
                or "ungültig" in body
                or response.status_code in {401, 403}
            )
        )

        return self.result(
            rejected,
            "Ungültige Zugangsdaten werden abgelehnt.",
            (
                f"Ungültiger Login lieferte HTTP "
                f"{response.status_code}; "
                f"Ablehnung erkannt: {rejected}"
            ),
            response,
        )

    def transfer_without_login(self) -> dict[str, Any]:
        if self.user_id is None:
            return self.result(
                False,
                (
                    "Für den Zugriffstest muss die Benutzer-ID "
                    "des zuvor angelegten Kontos bekannt sein."
                ),
                "Es wurde keine Benutzer-ID ermittelt.",
            )

        test_session = requests.Session()

        response = test_session.post(
            f"{self.base_url}/transfer/{self.user_id}",
            data={
                "recipient": "unauthorized-recipient",
                "amount": "10",
            },
            timeout=self.timeout_seconds,
            allow_redirects=False,
        )

        redirect = response.headers.get("Location", "")

        blocked = response.status_code in {
            401,
            403,
        }

        return self.result(
            blocked,
            (
                "Eine Überweisung ohne authentifizierte Sitzung "
                "wird verweigert."
            ),
            (
                f"Transfer ohne Sitzung: HTTP "
                f"{response.status_code}; "
                f"Redirect: {redirect or '-'}; "
                f"blockiert: {blocked}"
            ),
            response,
        )

    def negative_transfer(self) -> dict[str, Any]:
        if self.user_id is None:
            return self.result(
                False,
                "Für den Transfertest muss eine Benutzer-ID vorliegen.",
                "Es wurde keine Benutzer-ID ermittelt.",
            )

        before_response = self.session.get(
            f"{self.base_url}/dashboard/{self.user_id}",
            timeout=self.timeout_seconds,
        )

        balance_before = self.extract_balance(
            before_response.text
        )

        transfer_response = self.session.post(
            f"{self.base_url}/transfer/{self.user_id}",
            data={
                "recipient": "negative-test",
                "amount": "-100",
            },
            timeout=self.timeout_seconds,
            allow_redirects=False,
        )

        after_response = self.session.get(
            f"{self.base_url}/dashboard/{self.user_id}",
            timeout=self.timeout_seconds,
        )

        balance_after = self.extract_balance(
            after_response.text
        )

        rejected_by_status = transfer_response.status_code in {
            400,
            401,
            403,
            422,
        }

        balance_unchanged = (
            balance_before is not None
            and balance_after is not None
            and balance_before == balance_after
        )

        passed = (
            rejected_by_status
            and balance_unchanged
        )

        result = self.result(
            passed,
            (
                "Ein negativer Überweisungsbetrag wird abgelehnt "
                "und verändert den Kontostand nicht."
            ),
            (
                f"Transfer: HTTP "
                f"{transfer_response.status_code}; "
                f"Kontostand vorher: {balance_before}; "
                f"Kontostand danach: {balance_after}; "
                f"unverändert: {balance_unchanged}"
            ),
            transfer_response,
        )

        result["body_excerpt"] = (
            f"Transfer: "
            f"{self.body_excerpt(transfer_response)} | "
            f"Dashboard danach: "
            f"{self.body_excerpt(after_response)}"
        )

        return result

    def sql_injection_login(self) -> dict[str, Any]:
        response = requests.post(
            f"{self.base_url}/login",
            data={
                "username": "' OR '1'='1",
                "password": "' OR '1'='1",
            },
            timeout=self.timeout_seconds,
            allow_redirects=False,
        )

        body = response.text.lower()

        rejected = (
            response.status_code in {400, 401, 403}
            and (
                "fehlgeschlagen" in body
                or "ungültig" in body
                or response.status_code in {401, 403}
            )
        )

        return self.result(
            rejected,
            (
                "SQL-Injection-Eingaben führen nicht zu einem "
                "erfolgreichen Login."
            ),
            (
                f"SQL-Injection-Login: HTTP "
                f"{response.status_code}; "
                f"Ablehnung erkannt: {rejected}"
            ),
            response,
        )