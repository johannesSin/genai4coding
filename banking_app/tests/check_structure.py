import os
import sys
import csv
from datetime import datetime

model = sys.argv[1]
base = f"banking_app/{model}"

checks = []

def check(name, condition):
    checks.append((name, "correct" if condition else "failed"))

def count_py_files(path):
    total = 0
    for root, _, files in os.walk(path):
        total += sum(1 for f in files if f.endswith(".py"))
    return total

check("project_folder_exists", os.path.exists(base))
check("requirements_exists", os.path.exists(os.path.join(base, "requirements.txt")))
check("has_multiple_python_files", count_py_files(base) >= 3)
check("has_app_directory", os.path.exists(os.path.join(base, "app")))
check("has_main_file", any(
    os.path.exists(os.path.join(base, p))
    for p in ["main.py", "app.py", "app/main.py"]
))

os.makedirs("banking_app/results", exist_ok=True)
csv_path = "banking_app/results/banking_structure_results.csv"
exists = os.path.exists(csv_path)

with open(csv_path, "a", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    if not exists:
        writer.writerow(["timestamp", "model", "check", "status"])
    ts = datetime.now().isoformat(timespec="seconds")
    for name, status in checks:
        writer.writerow([ts, model, name, status])

for name, status in checks:
    print(model, name, status)