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

    # Count timelines: each splitter encountered creates 2 timelines from 1.
    # Total timelines = 2^(number of splitters hit along the particle's paths)
    # But splitters can be shared across paths, so we need to count
    # unique timeline-ending paths.
    #
    # Each particle travels downward. At each splitter it hits, the timeline splits:
    # one goes left-down, one goes right-down. So timelines = leaves of the split tree.
    # We need total number of distinct timelines = total leaf count of the recursion tree.
    # A timeline ends when a beam exits the grid without hitting a splitter.
    #
    # Key insight: a beam state is (row, col) moving downward.
    # At a splitter, it spawns two beams. We need to count total leaf paths.
    # Use memoization: for each starting (row, col), how many timelines does it produce?

    from functools import lru_cache

    # Precompute: for a beam starting at (r, c) going down,
    # find the first splitter it hits (or None if it exits)
    # Build a map: (r, c) -> first splitter position going down, or None

    @lru_cache(maxsize=None)
    def count_timelines(r, c):
        # Beam moves downward from (r, c)
        while 0 <= r < rows and 0 <= c < cols:
            if grid[r][c] == '^':
                # Split: left beam goes from (r+1, c-1), right from (r+1, c+1)
                left = count_timelines(r + 1, c - 1) if c - 1 >= 0 else 0
                right = count_timelines(r + 1, c + 1) if c + 1 < cols else 0
                total = left + right
                return total if total > 0 else 0
            r += 1
        # Beam exited grid: this is 1 timeline
        return 1

    result = count_timelines(1, start_col)
    print(result)

solve()