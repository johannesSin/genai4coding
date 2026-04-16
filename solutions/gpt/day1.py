def main():
    pos = 50
    count_zero = 0

    with open("tasks/day1/input.txt", "r") as f:
        for line in f:
            s = line.strip()
            if not s:
                continue

            direction = s[0]
            distance = int(s[1:]) % 100

            if direction == "L":
                pos = (pos - distance) % 100
            elif direction == "R":
                pos = (pos + distance) % 100
            else:
                raise ValueError(f"Invalid rotation: {s}")

            if pos == 0:
                count_zero += 1

    print(count_zero)


if __name__ == "__main__":
    main()