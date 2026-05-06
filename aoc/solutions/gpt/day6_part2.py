from math import prod

with open("tasks/day6/input.txt", "r", encoding="utf-8") as f:
    grid = [list(line.rstrip("\n")) for line in f]

ops_row = grid[-1]
grid = grid[:-1]

h = len(grid)
w = max(len(row) for row in grid)

for row in grid:
    row.extend([' '] * (w - len(row)))
ops_row.extend([' '] * (w - len(ops_row)))

problems = []
c = w - 1

while c >= 0:
    if all(grid[r][c] == ' ' for r in range(h)) and ops_row[c] == ' ':
        c -= 1
        continue

    cols = []
    while c >= 0 and not (all(grid[r][c] == ' ' for r in range(h)) and ops_row[c] == ' '):
        cols.append(c)
        c -= 1

    cols.reverse()

    numbers = []
    for col in cols:
        digits = [grid[r][col] for r in range(h) if grid[r][col].isdigit()]
        if digits:
            numbers.append(int(''.join(digits)))

    op = next((ops_row[col] for col in cols if ops_row[col] in "+*"), None)
    problems.append((numbers, op))

total = 0
for numbers, op in problems:
    total += sum(numbers) if op == '+' else prod(numbers)

print(total)