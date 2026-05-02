pos = 50
count = 0

with open("tasks/day1/input.txt") as f:
    for line in f:
        line = line.strip()
        if not line:
            continue

        direction = line[0]
        dist = int(line[1:])

        if direction == "R":
            first = (-pos) % 100
            if first == 0:
                first = 100
            if dist >= first:
                count += 1 + (dist - first) // 100
            pos = (pos + dist) % 100
        else:
            first = pos if pos != 0 else 100
            if dist >= first:
                count += 1 + (dist - first) // 100
            pos = (pos - dist) % 100

print(count)