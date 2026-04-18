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

    beams = {start_col}
    splits = 0

    for r in range(start_row + 1, rows):
        next_beams = set()
        for c in beams:
            if not (0 <= c < cols):
                continue
            if grid[r][c] == "^":
                splits += 1
                if c - 1 >= 0:
                    next_beams.add(c - 1)
                if c + 1 < cols:
                    next_beams.add(c + 1)
            else:
                next_beams.add(c)
        beams = next_beams
        if not beams:
            break

    print(splits)


if __name__ == "__main__":
    main()