# analyze_results.py

import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path
import os

os.makedirs("aoc/results", exist_ok=True)
os.makedirs("banking_app/results", exist_ok=True)

# --- Dateien laden ---
aoc_path = "aoc/results/benchmark_results.csv"
banking_path = "banking_app/results/banking_benchmark_results.csv"

# --- AoC Ergebnisse ---
print("\n=== Advent of Code Evaluation ===\n")

if Path(aoc_path).exists():
    aoc = pd.read_csv(aoc_path)

    summary = (
        aoc.groupby(["model", "status"])
        .size()
        .unstack(fill_value=0)
    )

    print(summary)

    # Erfolgsrate
    if "correct" in summary.columns:
        summary["success_rate"] = (
            summary["correct"] / summary.sum(axis=1) * 100
        ).round(2)

    print("\nSuccess Rates:\n")
    print(summary[["success_rate"]])

    # Diagramm
    if "correct" in summary.columns:
        plt.figure(figsize=(6, 4))
        summary["correct"].plot(kind="bar")
        plt.title("AoC Correct Solutions per Model")
        plt.ylabel("Correct Solutions")
        plt.tight_layout()
        plt.savefig("aoc/results/aoc_correct_solutions.png")
        plt.close()

else:
    print("AoC benchmark_results.csv not found")


# --- Banking Ergebnisse ---
print("\n=== Banking App Evaluation ===\n")

if Path(banking_path).exists():
    banking = pd.read_csv(banking_path)

    banking_summary = (
        banking.groupby(["model", "status"])
        .size()
        .unstack(fill_value=0)
    )

    print(banking_summary)

    if "correct" in banking_summary.columns:
        banking_summary["success_rate"] = (
            banking_summary["correct"] / banking_summary.sum(axis=1) * 100
        ).round(2)

    print("\nSuccess Rates:\n")
    print(banking_summary[["success_rate"]])

    # Diagramm
    if "correct" in banking_summary.columns:
        plt.figure(figsize=(6, 4))
        banking_summary["correct"].plot(kind="bar")
        plt.title("Banking Benchmark Passed Tests")
        plt.ylabel("Passed Tests")
        plt.tight_layout()
        plt.savefig("banking_app/results/banking_passed_tests.png")
        plt.close()

else:
    print("banking_benchmark_results.csv not found")


print("\nCharts gespeichert in results/")