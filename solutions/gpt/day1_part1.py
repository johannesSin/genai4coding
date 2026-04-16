pos = 50
count = 0

with open("tasks/day1/input.txt") as f:
    for line in f:
        line = line.strip()
        if not line:
            continue
        direction = line[0]
        dist = int(line[1:]) % 100
        if direction == "L":
            pos = (pos - dist) % 100
        else:
            pos = (pos + dist) % 100
        if pos == 0:
            count += 1

print(count)