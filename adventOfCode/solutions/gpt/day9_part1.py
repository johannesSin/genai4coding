points = []
with open("tasks/day9/input.txt") as f:
    for line in f:
        line = line.strip()
        if line:
            x, y = map(int, line.split(","))
            points.append((x, y))

best = 0
n = len(points)

for i in range(n):
    x1, y1 = points[i]
    for j in range(i + 1, n):
        x2, y2 = points[j]
        area = (abs(x1 - x2) + 1) * (abs(y1 - y2) + 1)
        if area > best:
            best = area

print(best)