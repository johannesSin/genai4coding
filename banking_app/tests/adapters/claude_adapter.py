from typing import Any

import requests

from .base import BankingAdapter


class ClaudeAdapter(BankingAdapter):
    def __init__(
        self,
        base_url: str,
        timeout_seconds: int,
    ) -> None:
        super().__init__(base_url, timeout_seconds)

        self.session = requests.Session()
        self.token = ""
        self.user_id: int | None = None
        self.accounts: list[dict[str, Any]] = []

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

    def auth_headers(self) -> dict[str, str]:
        if not self.token:
            return {}

        return {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json",
        }

    def load_accounts(self) -> requests.Response:
        response = self.session.get(
            f"{self.base_url}/api/accounts",
            headers=self.auth_headers(),
            timeout=self.timeout_seconds,
        )

        if response.status_code == 200:
            data = response.json()

            if isinstance(data, list):
                self.accounts = data

        return response

    def app_running(self) -> dict[str, Any]:
        response = self.session.get(
            f"{self.base_url}/api/docs",
            timeout=self.timeout_seconds,
        )

        return self.result(
            response.status_code == 200,
            (
                "Die Anwendung ist erreichbar und die "
                "API-Dokumentation liefert HTTP 200."
            ),
            f"/api/docs lieferte HTTP {response.status_code}.",
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
            and (
                "register-form" in body
                or "registrieren" in body
                or "konto erstellen" in body
            )
        )

        return self.result(
            form_visible,
            (
                "Das Frontend ist erreichbar und enthält eine "
                "Registrierungsmöglichkeit."
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
            f"{self.base_url}/api/auth/register",
            json={
                "full_name": username,
                "email": email,
                "password": password,
            },
            timeout=self.timeout_seconds,
        )

        response_data: dict[str, Any] = {}

        try:
            parsed = response.json()

            if isinstance(parsed, dict):
                response_data = parsed
        except ValueError:
            pass

        self.user_id = response_data.get("user_id")

        passed = (
            response.status_code == 201
            and isinstance(self.user_id, int)
        )

        return self.result(
            passed,
            (
                "Ein neuer Benutzer wird über die API registriert "
                "und erhält eine Benutzer-ID."
            ),
            (
                f"Registrierung: HTTP {response.status_code}; "
                f"user_id: {self.user_id or '-'}"
            ),
            response,
        )

    def login_page(self) -> dict[str, Any]:
        response = self.session.get(
            f"{self.base_url}/",
            timeout=self.timeout_seconds,
        )

        body = response.text.lower()

        login_visible = (
            response.status_code == 200
            and (
                "login-form" in body
                or "anmelden" in body
                or "login" in body
            )
        )

        return self.result(
            login_visible,
            (
                "Das Frontend ist erreichbar und enthält eine "
                "Loginmöglichkeit."
            ),
            (
                f"/ lieferte HTTP {response.status_code}; "
                f"Loginformular erkannt: {login_visible}"
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
            f"{self.base_url}/api/auth/login",
            json={
                "email": email,
                "password": password,
            },
            timeout=self.timeout_seconds,
        )

        response_data: dict[str, Any] = {}

        try:
            parsed = response.json()

            if isinstance(parsed, dict):
                response_data = parsed
        except ValueError:
            pass

        token = response_data.get("access_token")
        token_type = response_data.get("token_type")
        user = response_data.get("user", {})

        if isinstance(token, str):
            self.token = token

        if isinstance(user, dict) and isinstance(user.get("id"), int):
            self.user_id = user["id"]

        passed = (
            response.status_code == 200
            and bool(self.token)
            and token_type == "bearer"
        )

        return self.result(
            passed,
            (
                "Gültige Zugangsdaten liefern einen Bearer-Token "
                "für eine authentifizierte Sitzung."
            ),
            (
                f"Login: HTTP {response.status_code}; "
                f"Token vorhanden: {bool(self.token)}; "
                f"Token-Typ: {token_type or '-'}"
            ),
            response,
        )

    def dashboard(self) -> dict[str, Any]:
        response = self.session.get(
            f"{self.base_url}/api/auth/me",
            headers=self.auth_headers(),
            timeout=self.timeout_seconds,
        )

        user_id = None

        if response.status_code == 200:
            try:
                data = response.json()

                if isinstance(data, dict):
                    user_id = data.get("id")
            except ValueError:
                pass

        passed = (
            response.status_code == 200
            and isinstance(user_id, int)
        )

        return self.result(
            passed,
            (
                "Der geschützte Benutzerbereich ist mit dem "
                "Bearer-Token erreichbar."
            ),
            (
                f"/api/auth/me lieferte HTTP "
                f"{response.status_code}; "
                f"user_id: {user_id or '-'}"
            ),
            response,
        )

    def transfer_page(self) -> dict[str, Any]:
        response = self.load_accounts()

        passed = (
            response.status_code == 200
            and len(self.accounts) >= 1
        )

        return self.result(
            passed,
            (
                "Die für eine Überweisung benötigten Konten sind "
                "nach der Anmeldung abrufbar."
            ),
            (
                f"/api/accounts lieferte HTTP "
                f"{response.status_code}; "
                f"erkannte Konten: {len(self.accounts)}"
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
            f"{self.base_url}/api/auth/login",
            json={
                "email": email,
                "password": "wrongpassword",
            },
            timeout=self.timeout_seconds,
        )

        protected_response = test_session.get(
            f"{self.base_url}/api/auth/me",
            timeout=self.timeout_seconds,
        )

        login_rejected = login_response.status_code in {
            400,
            401,
            403,
        }

        protected_blocked = protected_response.status_code in {
            401,
            403,
        }

        result = self.result(
            login_rejected and protected_blocked,
            (
                "Ungültige Zugangsdaten werden abgelehnt und "
                "erzeugen keinen gültigen Bearer-Token."
            ),
            (
                f"Ungültiger Login: HTTP "
                f"{login_response.status_code}; "
                f"/api/auth/me ohne Token: HTTP "
                f"{protected_response.status_code}"
            ),
            login_response,
        )

        result["body_excerpt"] = (
            f"Login: {self.body_excerpt(login_response)} | "
            f"Geschützter Bereich: "
            f"{self.body_excerpt(protected_response)}"
        )

        return result

    def transfer_without_login(self) -> dict[str, Any]:
        response = requests.post(
            f"{self.base_url}/api/transactions/transfer",
            json={
                "from_account_id": 1,
                "to_account_number": "DE00000000000000000000",
                "amount": 10.0,
                "description": "unauthorized transfer",
            },
            timeout=self.timeout_seconds,
        )

        blocked = response.status_code in {
            401,
            403,
        }

        return self.result(
            blocked,
            (
                "Eine Überweisung ohne Bearer-Token wird "
                "verweigert."
            ),
            (
                f"Transfer ohne Token lieferte HTTP "
                f"{response.status_code}."
            ),
            response,
        )

    def negative_transfer(self) -> dict[str, Any]:
        if not self.accounts:
            account_response = self.load_accounts()

            if account_response.status_code != 200:
                return self.result(
                    False,
                    (
                        "Die Konten müssen vor dem Transfertest "
                        "abrufbar sein."
                    ),
                    (
                        f"/api/accounts lieferte HTTP "
                        f"{account_response.status_code}."
                    ),
                    account_response,
                )

        if len(self.accounts) < 2:
            create_response = self.session.post(
                f"{self.base_url}/api/accounts",
                headers=self.auth_headers(),
                json={
                    "account_type": "Sparkonto",
                },
                timeout=self.timeout_seconds,
            )

            if create_response.status_code != 201:
                return self.result(
                    False,
                    (
                        "Für den Transfertest muss ein zweites "
                        "Konto erzeugt werden können."
                    ),
                    (
                        f"Kontoerstellung lieferte HTTP "
                        f"{create_response.status_code}."
                    ),
                    create_response,
                )

            self.load_accounts()

        if len(self.accounts) < 2:
            return self.result(
                False,
                (
                    "Für den Transfertest werden mindestens zwei "
                    "Konten benötigt."
                ),
                f"Es wurden {len(self.accounts)} Konten erkannt.",
            )

        source = self.accounts[0]
        target = self.accounts[1]

        response = self.session.post(
            f"{self.base_url}/api/transactions/transfer",
            headers=self.auth_headers(),
            json={
                "from_account_id": source["id"],
                "to_account_number": target["account_number"],
                "amount": -100.0,
                "description": "negative transfer",
            },
            timeout=self.timeout_seconds,
        )

        body = response.text.lower()

        rejection_terms = [
            "positiv",
            "positive",
            "greater than",
            "betrag",
            "value_error",
            "validation",
            "fehler",
            "error",
        ]

        rejection_visible = any(
            term in body
            for term in rejection_terms
        )

        passed = (
            response.status_code in {400, 422}
            and rejection_visible
        )

        return self.result(
            passed,
            (
                "Ein vollständig formulierter Transfer mit "
                "negativem Betrag wird fachlich abgelehnt."
            ),
            (
                f"Quellkonto {source['id']}; "
                f"Zielkonto {target['account_number']}; "
                f"HTTP {response.status_code}; "
                f"Fehlermeldung erkannt: {rejection_visible}"
            ),
            response,
        )

    def sql_injection_login(self) -> dict[str, Any]:
        test_session = requests.Session()

        login_response = test_session.post(
            f"{self.base_url}/api/auth/login",
            json={
                "email": "sql@example.com",
                "password": "' OR '1'='1",
            },
            timeout=self.timeout_seconds,
        )

        protected_response = test_session.get(
            f"{self.base_url}/api/auth/me",
            timeout=self.timeout_seconds,
        )

        login_rejected = login_response.status_code in {
            400,
            401,
            403,
            422,
        }

        protected_blocked = protected_response.status_code in {
            401,
            403,
        }

        result = self.result(
            login_rejected and protected_blocked,
            (
                "SQL-Injection-Eingaben führen nicht zu einem "
                "gültigen Bearer-Token."
            ),
            (
                f"SQL-Injection-Login: HTTP "
                f"{login_response.status_code}; "
                f"/api/auth/me danach: HTTP "
                f"{protected_response.status_code}"
            ),
            login_response,
        )

        result["body_excerpt"] = (
            f"Login: {self.body_excerpt(login_response)} | "
            f"Geschützter Bereich: "
            f"{self.body_excerpt(protected_response)}"
        )

        return result