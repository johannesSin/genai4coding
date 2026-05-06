from pathlib import Path

grid = [list(line.strip()) for line in Path("tasks/day4/input.txt").read_text().splitlines() if line.strip()]
rows = len(grid)
cols = len(grid[0]) if rows else 0

result = 0
for r in range(rows):
    for c in range(cols):
        if grid[r][c] != "@":
            continue
        neighbors = 0
        for dr in (-1, 0, 1):
            for dc in (-1, 0, 1):
                if dr == 0 and dc == 0:
                    continue
                nr, nc = r + dr, c + dc
                if 0 <= nr < rows and 0 <= nc < cols and grid[nr][nc] == "@":
                    neighbors += 1
        if neighbors < 4:
            result += 1

print(result)