import subprocess

models = ["gpt", "claude", "gemini"]

for model in models:
    file = f"solutions/{model}/day1.py"

    result = subprocess.run(
        ["python3", file],
        capture_output=True,
        text=True
    )

    output = result.stdout.strip()

    with open("tasks/day1/expected.txt", "r", encoding="utf-8") as f:
        expected = f.read().strip()

    if output == expected:
        print(model, "✓ korrekt")
    else:
        print(model, "✗ falsch:", output)