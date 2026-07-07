from abc import ABC, abstractmethod
from typing import Any


class BankingAdapter(ABC):
    def __init__(self, base_url: str, timeout_seconds: int) -> None:
        self.base_url = base_url.rstrip("/")
        self.timeout_seconds = timeout_seconds

    @abstractmethod
    def app_running(self) -> dict[str, Any]:
        pass

    @abstractmethod
    def register_page(self) -> dict[str, Any]:
        pass

    @abstractmethod
    def register_user(
        self,
        username: str,
        email: str,
        password: str,
    ) -> dict[str, Any]:
        pass

    @abstractmethod
    def login_page(self) -> dict[str, Any]:
        pass

    @abstractmethod
    def login_user(
        self,
        username: str,
        email: str,
        password: str,
    ) -> dict[str, Any]:
        pass

    @abstractmethod
    def dashboard(self) -> dict[str, Any]:
        pass

    @abstractmethod
    def transfer_page(self) -> dict[str, Any]:
        pass

    @abstractmethod
    def invalid_login(
        self,
        username: str,
        email: str,
    ) -> dict[str, Any]:
        pass

    @abstractmethod
    def transfer_without_login(self) -> dict[str, Any]:
        pass

    @abstractmethod
    def negative_transfer(self) -> dict[str, Any]:
        pass

    @abstractmethod
    def sql_injection_login(self) -> dict[str, Any]:
        pass