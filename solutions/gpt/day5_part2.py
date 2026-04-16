def main():
    with open("tasks/day5/input.txt", "r", encoding="utf-8") as f:
        lines = [line.strip() for line in f]

    blank = lines.index("")
    ranges = []
    for line in lines[:blank]:
        a, b = map(int, line.split("-"))
        ranges.append((a, b))

    ranges.sort()
    merged = []

    for start, end in ranges:
        if not merged or start > merged[-1][1] + 1:
            merged.append([start, end])
        else:
            merged[-1][1] = max(merged[-1][1], end)

    total = 0
    for start, end in merged:
        total += end - start + 1

    print(total)


if __name__ == "__main__":
    main()