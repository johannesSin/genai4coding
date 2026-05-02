def main():
    with open("tasks/day5/input.txt", "r", encoding="utf-8") as f:
        lines = [line.strip() for line in f]

    blank = lines.index("")
    ranges = []
    for line in lines[:blank]:
        a, b = map(int, line.split("-"))
        ranges.append((a, b))

    count = 0
    for line in lines[blank + 1:]:
        if not line:
            continue
        x = int(line)
        for a, b in ranges:
            if a <= x <= b:
                count += 1
                break

    print(count)


if __name__ == "__main__":
    main()