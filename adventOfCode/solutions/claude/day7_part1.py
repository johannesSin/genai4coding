from collections import deque

def solve():
    with open("tasks/day7/input.txt") as f:
        grid = [line.rstrip('\n') for line in f.readlines()]

    rows = len(grid)
    cols = len(grid[0]) if rows > 0 else 0

    # Find starting position S
    start_col = None
    for c in range(cols):
        if grid[0][c] == 'S':
            start_col = c
            break

    if start_col is None:
        print(0)
        return

    # BFS/simulation
    # State: (row, col) with beam moving downward
    # When beam hits '^', it splits: two new beams go left and right from that splitter
    # Count total number of splits

    splits = 0
    visited_splits = set()  # splitters already activated

    # Queue of beam positions moving downward: (row, col)
    queue = deque()
    queue.append((1, start_col))  # beam starts below S, moving down

    # Track visited (row, col) for beams to avoid infinite loops
    visited_beams = set()

    while queue:
        r, c = queue.popleft()

        # Move beam downward until it hits a splitter or exits
        while 0 <= r < rows and 0 <= c < cols:
            if (r, c) in visited_beams:
                break
            visited_beams.add((r, c))

            if grid[r][c] == '^':
                if (r, c) not in visited_splits:
                    visited_splits.add((r, c))
                    splits += 1
                    # Emit beams left and right from (r, c+1) and (r, c-1) going down
                    # Left beam: starts at (r+1, c-1) going down... 
                    # Actually: new beams continue from immediate left and right of splitter
                    # "a new tachyon beam continues from the immediate left and from the immediate right"
                    # They move downward from (r, c-1) and (r, c+1)
                    if c - 1 >= 0:
                        queue.append((r + 1, c - 1))
                    if c + 1 < cols:
                        queue.append((r + 1, c + 1))
                break  # original beam stops at splitter
            else:
                r += 1  # continue downward through empty space

    print(splits)

solve()