from collections import deque
from pathlib import Path

grid = [list(line.strip()) for line in Path("tasks/day4/input.txt").read_text().splitlines() if line.strip()]
rows = len(grid)
cols = len(grid[0]) if rows else 0

dirs = [(-1, -1), (-1, 0), (-1, 1),
        (0, -1),           (0, 1),
        (1, -1),  (1, 0),  (1, 1)]

neighbor_count = [[0] * cols for _ in range(rows)]
for r in range(rows):
    for c in range(cols):
        if grid[r][c] != "@":
            continue
        count = 0
        for dr, dc in dirs:
            nr, nc = r + dr, c + dc
            if 0 <= nr < rows and 0 <= nc < cols and grid[nr][nc] == "@":
                count += 1
        neighbor_count[r][c] = count

q = deque()
in_queue = [[False] * cols for _ in range(rows)]

for r in range(rows):
    for c in range(cols):
        if grid[r][c] == "@" and neighbor_count[r][c] < 4:
            q.append((r, c))
            in_queue[r][c] = True

removed = 0

while q:
    r, c = q.popleft()
    if grid[r][c] != "@":
        continue

    grid[r][c] = "."
    removed += 1

    for dr, dc in dirs:
        nr, nc = r + dr, c + dc
        if 0 <= nr < rows and 0 <= nc < cols and grid[nr][nc] == "@":
            neighbor_count[nr][nc] -= 1
            if neighbor_count[nr][nc] < 4 and not in_queue[nr][nc]:
                q.append((nr, nc))
                in_queue[nr][nc] = True

print(removed)