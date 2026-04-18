import subprocess
import csv
import os
from datetime import datetime

cases = [
    ("day1_part1", "day1_part1.py", "tasks/day1/expected_part1.txt"),
    ("day1_part2", "day1_part2.py", "tasks/day1/expected_part2.txt"),
    ("day2_part1", "day2_part1.py", "tasks/day2/expected_part1.txt"),
    ("day2_part2", "day2_part2.py", "tasks/day2/expected_part2.txt"),
    ("day3_part1", "day3_part1.py", "tasks/day3/expected_part1.txt"),
    ("day3_part2", "day3_part2.py", "tasks/day3/expected_part2.txt"),
    ("day4_part1", "day4_part1.py", "tasks/day4/expected_part1.txt"),
    ("day4_part2", "day4_part2.py", "tasks/day4/expected_part2.txt"),
    ("day5_part1", "day5_part1.py", "tasks/day5/expected_part1.txt"),
    ("day5_part2", "day5_part2.py", "tasks/day5/expected_part2.txt"),
    ("day6_part1", "day6_part1.py", "tasks/day6/expected_part1.txt"),
    ("day6_part2", "day6_part2.py", "tasks/day6/expected_part2.txt"),
    ("day7_part1", "day7_part1.py", "tasks/day7/expected_part1.txt"),
    ("day7_part2", "day7_part2.py", "tasks/day7/expected_part2.txt"),
    ("day8_part1", "day8_part1.py", "tasks/day8/expected_part1.txt"),
    ("day8_part2", "day8_part2.py", "tasks/day8/expected_part2.txt"),
    ("day9_part1", "day9_part1.py", "tasks/day9/expected_part1.txt"),
    ("day9_part2", "day9_part2.py", "tasks/day9/expected_part2.txt"),
    ("day10_part1", "day10_part1.py", "tasks/day10/expected_part1.txt"),
    ("day10_part2", "day10_part2.py", "tasks/day10/expected_part2.txt"),
    ("day11_part1", "day11_part1.py", "tasks/day11/expected_part1.txt"),
    ("day11_part2", "day11_part2.py", "tasks/day11/expected_part2.txt"),
    ("day12_part1", "day12_part1.py", "tasks/day12/expected_part1.txt"),
    ("day12_part2", "day12_part2.py", "tasks/day12/expected_part2.txt"),
]

models = ["gpt", "claude", "gemini"]
timeout_seconds = 15

os.makedirs("results", exist_ok=True)
csv_path = "results/benchmark_results.csv"

rows = []

def classify_error(stderr: str) -> str:
    s = stderr.strip()
    if "ModuleNotFoundError" in s:
        return "missing_dependency"
    if "FileNotFoundError" in s:
        return "missing_file"
    if "SyntaxError" in s:
        return "syntax_error"
    if "IndentationError" in s:
        return "indentation_error"
    if "NameError" in s:
        return "name_error"
    if "TypeError" in s:
        return "type_error"
    if "ValueError" in s:
        return "value_error"
    if "IndexError" in s:
        return "index_error"
    if "KeyError" in s:
        return "key_error"
    if "ZeroDivisionError" in s:
        return "zero_division"
    return "runtime_error"

for case_name, filename, expected_file in cases:
    print(f"\n--- {case_name} ---")
    for model in models:
        file_path = f"solutions/{model}/{filename}"

        if not os.path.exists(file_path):
            print(model, "❌ missing solution file")
            rows.append([
                case_name, model, "missing_solution_file", "", "", ""
            ])
            continue

        if not os.path.exists(expected_file):
            print(model, "❌ missing expected file")
            rows.append([
                case_name, model, "missing_expected_file", "", "", ""
            ])
            continue

        with open(expected_file, "r", encoding="utf-8") as f:
            expected = f.read().strip()

        try:
            result = subprocess.run(
                ["python3", file_path],
                capture_output=True,
                text=True,
                timeout=timeout_seconds
            )

            stdout = result.stdout.strip()
            stderr = result.stderr.strip()

            if result.returncode != 0:
                error_type = classify_error(stderr)
                print(model, f"❌ {error_type}")
                rows.append([
                    case_name, model, error_type, stdout, stderr, expected
                ])
            elif stdout == expected:
                print(model, "✓ correct")
                rows.append([
                    case_name, model, "correct", stdout, "", expected
                ])
            else:
                print(model, f"✗ wrong_output: {stdout}")
                rows.append([
                    case_name, model, "wrong_output", stdout, "", expected
                ])

        except subprocess.TimeoutExpired:
            print(model, "❌ timeout")
            rows.append([
                case_name, model, "timeout", "", "", expected
            ])
        except Exception as e:
            print(model, f"❌ exception: {type(e).__name__}")
            rows.append([
                case_name, model, f"exception_{type(e).__name__}", "", str(e), expected
            ])

with open(csv_path, "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow([
        "case",
        "model",
        "status",
        "stdout",
        "stderr",
        "expected"
    ])
    writer.writerows(rows)

print(f"\nCSV gespeichert: {csv_path}")
print(f"Zeitpunkt: {datetime.now().isoformat(timespec='seconds')}")