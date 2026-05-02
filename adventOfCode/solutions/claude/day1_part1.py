pos = 50
count = 0
with open("tasks/day1/input.txt") as f:
    for line in f:
        line = line.strip()
        if not line:
            continue
        d, n = line[0], int(line[1:])
        if d == 'L':
            pos = (pos - n) % 100
        else:
            pos = (pos + n) % 100
        if pos == 0:
            count += 1
print(count)