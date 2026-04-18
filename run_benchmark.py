import subprocess

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

for case_name, filename, expected_file in cases:
    print(f"\n--- {case_name} ---")
    for model in models:
        file = f"solutions/{model}/{filename}"

        result = subprocess.run(
            ["python3", file],
            capture_output=True,
            text=True
        )

        output = result.stdout.strip()

        with open(expected_file, "r", encoding="utf-8") as f:
            expected = f.read().strip()

        if output == expected:
            print(model, "✓")
        else:
            err = result.stderr.strip()
            print(model, "✗", output if output else err)