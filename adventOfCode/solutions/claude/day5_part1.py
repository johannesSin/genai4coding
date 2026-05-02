import sys

with open("tasks/day5/input.txt") as f:
    content = f.read()

parts = content.strip().split("\n\n")
ranges_section = parts[0].strip().splitlines()
ids_section = parts[1].strip().splitlines()

ranges = []
for line in ranges_section:
    a, b = line.strip().split("-")
    ranges.append((int(a), int(b)))

count = 0
for line in ids_section:
    ingredient_id = int(line.strip())
    if any(lo <= ingredient_id <= hi for lo, hi in ranges):
        count += 1

print(count)