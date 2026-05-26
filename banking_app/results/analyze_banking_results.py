import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

CSV_PATH = Path("banking_benchmark_results.csv")

if not CSV_PATH.exists():
    raise FileNotFoundError("banking_benchmark_results.csv wurde nicht gefunden.")

df = pd.read_csv(CSV_PATH)

print("\n=== Banking App Evaluation ===\n")

summary = (
    df.groupby(["model", "status"])
    .size()
    .unstack(fill_value=0)
)

print(summary)

summary["total"] = summary.sum(axis=1)

if "correct" not in summary.columns:
    summary["correct"] = 0

summary["success_rate"] = (
    summary["correct"] / summary["total"] * 100
).round(2)

print("\n=== Success Rates ===\n")
print(summary[["correct", "total", "success_rate"]])

summary.to_csv("banking_summary.csv")

# Diagramm: Passed Tests
plt.figure(figsize=(7, 4))
summary["correct"].plot(kind="bar")
plt.ylabel("Passed Tests")
plt.xlabel("Model")
plt.tight_layout()
plt.savefig("banking_passed_tests.png")
plt.close()

# Diagramm: Success Rate
plt.figure(figsize=(7, 4))
summary["success_rate"].plot(kind="bar")
plt.ylabel("Success Rate (%)")
plt.xlabel("Model")
plt.ylim(0, 100)
plt.tight_layout()
plt.savefig("banking_success_rate.png")
plt.close()

# Fehlertypen ohne correct
error_df = df[df["status"] != "correct"]

if not error_df.empty:
    error_summary = (
        error_df.groupby(["model", "status"])
        .size()
        .unstack(fill_value=0)
    )

    print("\n=== Error / Failed Tests ===\n")
    print(error_summary)

    error_summary.to_csv("banking_error_summary.csv")

    plt.figure(figsize=(8, 4))
    error_summary.plot(kind="bar", stacked=True)
    plt.ylabel("Count")
    plt.xlabel("Model")
    plt.tight_layout()
    plt.savefig("banking_failed_tests.png")
    plt.close()

# Testweise Auswertung: welcher Test schlägt bei welchem Modell fehl?
test_summary = (
    df.assign(is_correct=df["status"] == "correct")
    .groupby(["test", "model"])["is_correct"]
    .mean()
    .unstack(fill_value=0)
    * 100
).round(2)

print("\n=== Test-Level Success Rate ===\n")
print(test_summary)

test_summary.to_csv("banking_test_level_summary.csv")

plt.figure(figsize=(10, 5))
test_summary.plot(kind="bar")
plt.ylabel("Success Rate (%)")
plt.xlabel("Test")
plt.ylim(0, 100)
plt.tight_layout()
plt.savefig("banking_test_level_success.png")
plt.close()

print("\nAuswertung abgeschlossen.")
print("Erzeugte Dateien:")
print("- banking_summary.csv")
print("- banking_error_summary.csv")
print("- banking_test_level_summary.csv")
print("- banking_passed_tests.png")
print("- banking_success_rate.png")
print("- banking_failed_tests.png")
print("- banking_test_level_success.png")