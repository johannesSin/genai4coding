import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

CSV_PATH = Path("benchmark_results.csv")

if not CSV_PATH.exists():
    raise FileNotFoundError("benchmark_results.csv wurde nicht gefunden.")

df = pd.read_csv(CSV_PATH)

print("\n=== Advent of Code Evaluation ===\n")

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

summary.to_csv("aoc_summary.csv")

# Diagramm: Correct Solutions
plt.figure(figsize=(7, 4))
summary["correct"].plot(kind="bar")
plt.ylabel("Correct Solutions")
plt.xlabel("Model")
plt.tight_layout()
plt.savefig("aoc_correct_solutions.png")
plt.close()

# Diagramm: Success Rate
plt.figure(figsize=(7, 4))
summary["success_rate"].plot(kind="bar")
plt.ylabel("Success Rate (%)")
plt.xlabel("Model")
plt.ylim(0, 100)
plt.tight_layout()
plt.savefig("aoc_success_rate.png")
plt.close()

# Fehlertypen ohne correct
error_df = df[df["status"] != "correct"]

if not error_df.empty:
    error_summary = (
        error_df.groupby(["model", "status"])
        .size()
        .unstack(fill_value=0)
    )

    print("\n=== Error Types ===\n")
    print(error_summary)

    error_summary.to_csv("aoc_error_summary.csv")

    plt.figure(figsize=(8, 4))
    error_summary.plot(kind="bar", stacked=True)
    plt.ylabel("Count")
    plt.xlabel("Model")
    plt.tight_layout()
    plt.savefig("aoc_error_types.png")
    plt.close()

# Part 1 vs Part 2
df["part"] = df["case"].apply(lambda x: "part1" if "part1" in x else "part2")

part_summary = (
    df.assign(is_correct=df["status"] == "correct")
    .groupby(["model", "part"])["is_correct"]
    .mean()
    .unstack(fill_value=0)
    * 100
).round(2)

print("\n=== Part 1 vs Part 2 Success Rate ===\n")
print(part_summary)

part_summary.to_csv("aoc_part_summary.csv")

plt.figure(figsize=(7, 4))
part_summary.plot(kind="bar")
plt.ylabel("Success Rate (%)")
plt.xlabel("Model")
plt.ylim(0, 100)
plt.tight_layout()
plt.savefig("aoc_part1_vs_part2.png")
plt.close()

print("\nAuswertung abgeschlossen.")
print("Erzeugte Dateien:")
print("- aoc_summary.csv")
print("- aoc_error_summary.csv")
print("- aoc_part_summary.csv")
print("- aoc_correct_solutions.png")
print("- aoc_success_rate.png")
print("- aoc_error_types.png")
print("- aoc_part1_vs_part2.png")