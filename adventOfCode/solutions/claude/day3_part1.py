from itertools import combinations

total = 0
with open("tasks/day3/input.txt") as f:
    for line in f:
        line = line.strip()
        if not line:
            continue
        best = max(int(a + b) for a, b in combinations(line, 2))
        total += best

print(total)