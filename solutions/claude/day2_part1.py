import re

with open("tasks/day2/input.txt") as f:
    data = f.read().strip()

ranges = data.split(",")

total = 0
for r in ranges:
    r = r.strip()
    if not r:
        continue
    lo, hi = map(int, r.split("-"))
    for n in range(lo, hi + 1):
        s = str(n)
        length = len(s)
        if length % 2 == 0:
            half = length // 2
            if s[:half] == s[half:]:
                total += n

print(total)