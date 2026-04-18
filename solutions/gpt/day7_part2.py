def main():
    with open("tasks/day7/input.txt", "r", encoding="utf-8") as f:
        grid = [line.rstrip("\n") for line in f if line.rstrip("\n")]

    rows = len(grid)
    cols = len(grid[0])

    start_row = start_col = None
    for r in range(rows):
        c = grid[r].find("S")
        if c != -1:
            start_row, start_col = r, c
            break

    ways = {start_col: 1}

    for r in range(start_row + 1, rows):
        next_ways = {}
        for c, count in ways.items():
            if not (0 <= c < cols):
                continue
            if grid[r][c] == "^":
                if c - 1 >= 0:
                    next_ways[c - 1] = next_ways.get(c - 1, 0) + count
                if c + 1 < cols:
                    next_ways[c + 1] = next_ways.get(c + 1, 0) + count
            else:
                next_ways[c] = next_ways.get(c, 0) + count
        ways = next_ways
        if not ways:
            break

    print(sum(ways.values()))


if __name__ == "__main__":
    main()