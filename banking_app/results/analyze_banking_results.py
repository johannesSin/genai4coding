import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

CSV_PATH = Path("banking_benchmark_results.csv")

if not CSV_PATH.exists():
    raise FileNotFoundError("banking_benchmark_results.csv wurde nicht gefunden.")

df = pd.read_csv(CSV_PATH)

print("\n=== Banking-App-Auswertung ===\n")

summary = (
    df.groupby(["model", "status"])
    .size()
    .unstack(fill_value=0)
)

print(summary)

summary["Gesamt"] = summary.sum(axis=1)

if "correct" not in summary.columns:
    summary["correct"] = 0

summary["Erfolgsrate"] = (
    summary["correct"] / summary["Gesamt"] * 100
).round(2)

print("\n=== Erfolgsraten ===\n")
print(summary[["correct", "Gesamt", "Erfolgsrate"]])

summary.to_csv("banking_summary.csv")

# Diagramm: Bestandene Tests
plt.figure(figsize=(7, 4))
summary["correct"].plot(kind="bar")
plt.ylabel("Bestandene Tests")
plt.xlabel("Modell")
plt.tight_layout()
plt.savefig("banking_passed_tests.png")
plt.close()

# Diagramm: Erfolgsrate pro Modell
plt.figure(figsize=(7, 4))
summary["Erfolgsrate"].plot(kind="bar")
plt.ylabel("Erfolgsrate (%)")
plt.xlabel("Modell")
plt.ylim(0, 100)
plt.tight_layout()
plt.savefig("banking_success_rate.png")
plt.close()

# Fehlgeschlagene Tests
error_df = df[df["status"] != "correct"]

if not error_df.empty:
    error_summary = (
        error_df.groupby(["model", "status"])
        .size()
        .unstack(fill_value=0)
    )

    print("\n=== Fehlgeschlagene Tests ===\n")
    print(error_summary)

    error_summary.to_csv("banking_error_summary.csv")

    plt.figure(figsize=(8, 4))
    error_summary.plot(kind="bar", stacked=True)
    plt.ylabel("Anzahl")
    plt.xlabel("Modell")
    plt.tight_layout()
    plt.savefig("banking_failed_tests.png")
    plt.close()

# Erfolgsrate pro Test
test_summary = (
    df.assign(is_correct=df["status"] == "correct")
    .groupby(["test", "model"])["is_correct"]
    .mean()
    .unstack(fill_value=0)
    * 100
).round(2)

print("\n=== Erfolgsrate pro Test ===\n")
print(test_summary)

test_summary.to_csv("banking_test_level_summary.csv")

plt.figure(figsize=(12, 6))
ax = test_summary.plot(kind="bar")
ax.set_ylabel("Erfolgsrate (%)")
ax.set_xlabel("Test")
ax.set_ylim(0, 100)
plt.xticks(rotation=45, ha="right")
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