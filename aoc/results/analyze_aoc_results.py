import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

CSV_PATH = Path("benchmark_results.csv")

if not CSV_PATH.exists():
    raise FileNotFoundError("benchmark_results.csv wurde nicht gefunden.")

df = pd.read_csv(CSV_PATH)

print("\n=== Advent-of-Code-Auswertung ===\n")

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

summary.to_csv("aoc_summary.csv")

# Diagramm: Korrekte Lösungen
plt.figure(figsize=(7, 4))
summary["correct"].plot(kind="bar")
plt.ylabel("Korrekte Lösungen")
plt.xlabel("Modell")
plt.tight_layout()
plt.savefig("aoc_correct_solutions.png")
plt.close()

# Diagramm: Erfolgsrate pro Modell
plt.figure(figsize=(7, 4))
summary["Erfolgsrate"].plot(kind="bar")
plt.ylabel("Erfolgsrate (%)")
plt.xlabel("Modell")
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

    print("\n=== Fehlertypen ===\n")
    print(error_summary)

    error_summary.to_csv("aoc_error_summary.csv")

    plt.figure(figsize=(8, 4))
    error_summary.plot(kind="bar", stacked=True)
    plt.ylabel("Anzahl")
    plt.xlabel("Modell")
    plt.tight_layout()
    plt.savefig("aoc_error_types.png")
    plt.close()

# Part 1 vs Part 2
df["part"] = df["case"].apply(lambda x: "Part 1" if "part1" in x else "Part 2")

part_summary = (
    df.assign(is_correct=df["status"] == "correct")
    .groupby(["model", "part"])["is_correct"]
    .mean()
    .unstack(fill_value=0)
    * 100
).round(2)

print("\n=== Erfolgsrate Part 1 vs. Part 2 ===\n")
print(part_summary)

part_summary.to_csv("aoc_part_summary.csv")

plt.figure(figsize=(7, 4))
part_summary.plot(kind="bar")
plt.ylabel("Erfolgsrate (%)")
plt.xlabel("Modell")
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