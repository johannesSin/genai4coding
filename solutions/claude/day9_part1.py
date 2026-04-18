with open("tasks/day9/input.txt") as f:
    points = [tuple(map(int, line.strip().split(','))) for line in f if line.strip()]

max_area = 0
n = len(points)
for i in range(n):
    for j in range(i + 1, n):
        x1, y1 = points[i]
        x2, y2 = points[j]
        area = abs(x2 - x1) * abs(y2 - y1)
        if area > max_area:
            max_area = area

print(max_area)