with open("tasks/day4/input.txt") as f:
    grid = [list(line.rstrip("\n")) for line in f]

rows = len(grid)

def accessible(grid, r, c):
    if grid[r][c] != "@":
        return False
    neighbors = 0
    for dr in [-1, 0, 1]:
        for dc in [-1, 0, 1]:
            if dr == 0 and dc == 0:
                continue
            nr, nc = r + dr, c + dc
            if 0 <= nr < len(grid) and 0 <= nc < len(grid[nr]) and grid[nr][nc] == "@":
                neighbors += 1
    return neighbors < 4

total = 0
while True:
    to_remove = [(r, c) for r in range(len(grid)) for c in range(len(grid[r])) if accessible(grid, r, c)]
    if not to_remove:
        break
    for r, c in to_remove:
        grid[r][c] = "."
    total += len(to_remove)

print(total)