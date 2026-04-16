with open("tasks/day4/input.txt") as f:
    grid = [line.rstrip("\n") for line in f]

rows = len(grid)
cols = max(len(row) for row in grid)

count = 0
for r in range(rows):
    for c in range(len(grid[r])):
        if grid[r][c] == "@":
            neighbors = 0
            for dr in [-1, 0, 1]:
                for dc in [-1, 0, 1]:
                    if dr == 0 and dc == 0:
                        continue
                    nr, nc = r + dr, c + dc
                    if 0 <= nr < rows and 0 <= nc < len(grid[nr]) and grid[nr][nc] == "@":
                        neighbors += 1
            if neighbors < 4:
                count += 1

print(count)