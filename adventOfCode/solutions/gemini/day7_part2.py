def solve():
    with open('tasks/day7/input.txt', 'r') as f:
        grid = [line.rstrip('\n') for line in f if line.strip()]

    if not grid:
        return

    start_col = -1
    for c, char in enumerate(grid[0]):
        if char == 'S':
            start_col = c
            break

    # We track how many timelines have a particle at each column position.
    # Initially, 1 timeline starts at start_col.
    positions = {start_col: 1}

    for r in range(1, len(grid)):
        next_positions = {}
        for col, count in positions.items():
            if grid[r][col] == '^':
                # Quantum split: The timeline itself splits. 
                # One version of the particle goes left, one goes right.
                left = col - 1
                right = col + 1
                
                if left >= 0:
                    next_positions[left] = next_positions.get(left, 0) + count
                if right < len(grid[r]):
                    next_positions[right] = next_positions.get(right, 0) + count
            else:
                # Particle continues in its current timeline's column
                next_positions[col] = next_positions.get(col, 0) + count
        positions = next_positions

    print(sum(positions.values()))

if __name__ == "__main__":
    solve()