import csv
import os
import re
import sys
import time
from datetime import datetime
from html.parser import HTMLParser
from typing import Any, Callable
try:
    from banking_app.tests.adapters.gpt_adapter import GPTAdapter
    from banking_app.tests.adapters.claude_adapter import ClaudeAdapter
    from banking_app.tests.adapters.gemini_adapter import GeminiAdapter
except ModuleNotFoundError:
    from adapters.gpt_adapter import GPTAdapter
    from adapters.claude_adapter import ClaudeAdapter
    from adapters.gemini_adapter import GeminiAdapter


import requests
import platform
import subprocess


BASE_URL = "http://127.0.0.1:8000"
MODEL = sys.argv[1] if len(sys.argv) > 1 else "unknown"
if MODEL not in {"gpt", "claude", "gemini"}:
    raise SystemExit(
        "Benchmark V2 unterstützt aktuell nur die Modelle 'gpt', 'claude' und 'gemini'."
    )
TIMEOUT_SECONDS = 5
BENCHMARK_VERSION = "2.0"

# Eindeutige Zugangsdaten pro Testlauf.
RUN_ID = datetime.now().strftime("%Y%m%d%H%M%S")
TEST_USERNAME = f"bench_{MODEL}_{RUN_ID}"
TEST_EMAIL = f"{TEST_USERNAME}@example.com"
TEST_PASSWORD = "Test12345!"

if MODEL == "gpt":
    adapter = GPTAdapter(
        base_url=BASE_URL,
        timeout_seconds=TIMEOUT_SECONDS,
    )
elif MODEL == "claude":
    adapter = ClaudeAdapter(
        base_url=BASE_URL,
        timeout_seconds=TIMEOUT_SECONDS,
    )
elif MODEL == "gemini":
    adapter = GeminiAdapter(
        base_url=BASE_URL,
        timeout_seconds=TIMEOUT_SECONDS,
    )
session = requests.Session()
results: list[dict[str, Any]] = []


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


def get_git_commit() -> str:
    try:
        return subprocess.check_output(
            ["git", "rev-parse", "--short", "HEAD"],
            text=True,
        ).strip()
    except Exception:
        return "unknown"

def write_results() -> str:
    os.makedirs("banking_app/results", exist_ok=True)

    csv_path = (
        "banking_app/results/"
        "banking_benchmark_final.csv"
    )

    file_exists = os.path.exists(csv_path)

    fieldnames = [
        "timestamp",
        "benchmark_version",
        "git_commit",
        "python_version",
        "adapter",
        "timeout_seconds",
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
                    "benchmark_version": BENCHMARK_VERSION,
                    "git_commit": get_git_commit(),
                    "python_version": platform.python_version(),
                    "adapter": MODEL,
                    "timeout_seconds": TIMEOUT_SECONDS,
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
    adapter.app_running,
    )

    check(
        "Register page",
        adapter.register_page,
    )

    check(
        "Register form submit",
        lambda: adapter.register_user(
            TEST_USERNAME,
            TEST_EMAIL,
            TEST_PASSWORD,
        ),
    )

    check(
        "Login page",
        adapter.login_page,
    )

    check(
        "Login form submit",
        lambda: adapter.login_user(
            TEST_USERNAME,
            TEST_EMAIL,
            TEST_PASSWORD,
        ),
    )

    check(
        "Dashboard route",
        adapter.dashboard,
    )

    check(
        "Transfer page",
        adapter.transfer_page,
    )

    check(
        "Invalid login rejected",
        lambda: adapter.invalid_login(
            TEST_USERNAME,
            TEST_EMAIL,
        ),
    )

    check(
        "Transfer without login blocked",
        adapter.transfer_without_login,
    )

    check(
        "Negative transfer handled",
        adapter.negative_transfer,
    )

    check(
        "SQL injection login handled",
        adapter.sql_injection_login,
    )

    print_results()
    output_path = write_results()

    print(
        "\nDetailliertes Testprotokoll gespeichert:"
    )
    print(output_path)