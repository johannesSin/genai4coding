import subprocess

cases = [
    ("day1_part1", "day1_part1.py", "tasks/day1/expected_part1.txt"),
    ("day1_part2", "day1_part2.py", "tasks/day1/expected_part2.txt"),
    ("day2_part1", "day2_part1.py", "tasks/day2/expected_part1.txt"),
    ("day2_part2", "day2_part2.py", "tasks/day2/expected_part2.txt"),
    ("day3_part1", "day3_part1.py", "tasks/day3/expected_part1.txt"),
    ("day3_part2", "day3_part2.py", "tasks/day3/expected_part2.txt"),
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