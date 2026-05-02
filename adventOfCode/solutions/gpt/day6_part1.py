from math import prod

with open("tasks/day6/input.txt", "r", encoding="utf-8") as f:
    lines = [line.rstrip("\n") for line in f]

ops = lines[-1].split()
rows = [list(map(int, line.split())) for line in lines[:-1]]

total = 0
for i, op in enumerate(ops):
    col = [row[i] for row in rows]
    total += sum(col) if op == "+" else prod(col)

print(total)