def solve():
    try:
        with open('tasks/day4/input.txt', 'r') as f:
            grid_lines = [list(line.strip()) for line in f if line.strip()]
    except FileNotFoundError:
        return

    if not grid_lines:
        return

    rows = len(grid_lines)
    cols = len(grid_lines[0])
    total_removed = 0

    while True:
        to_remove = []
        for r in range(rows):
            for c in range(cols):
                if grid_lines[r][c] == '@':
                    neighbors = 0
                    for dr in [-1, 0, 1]:
                        for dc in [-1, 0, 1]:
                            if dr == 0 and dc == 0:
                                continue
                            nr, nc = r + dr, c + dc
                            if 0 <= nr < rows and 0 <= nc < cols:
                                if grid_lines[nr][nc] == '@':
                                    neighbors += 1
                    
                    if neighbors < 4:
                        to_remove.append((r, c))
        
        if not to_remove:
            break
            
        total_removed += len(to_remove)
        for r, c in to_remove:
            grid_lines[r][c] = '.'

    print(total_removed)

if __name__ == "__main__":
    solve()