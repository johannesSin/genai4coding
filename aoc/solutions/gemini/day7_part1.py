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

    # Set of beams currently active, represented by their column index
    active_beams = {start_col}
    total_splits = 0
    
    # Track splitters that have already been activated to avoid double counting
    # though the problem implies beams stop at splitters, processing row by row 
    # handles the downward movement naturally.
    for r in range(1, len(grid)):
        new_beams = set()
        splitters_this_row = set()
        
        for col in active_beams:
            if grid[r][col] == '^':
                splitters_this_row.add(col)
            else:
                # Beam continues downward
                new_beams.add(col)
        
        for s_col in splitters_this_row:
            total_splits += 1
            # Splitter emits beams to the immediate left and right
            if s_col - 1 >= 0:
                new_beams.add(s_col - 1)
            if s_col + 1 < len(grid[r]):
                new_beams.add(s_col + 1)
        
        active_beams = new_beams

    print(total_splits)

if __name__ == "__main__":
    solve()