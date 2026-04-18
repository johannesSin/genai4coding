from shapely.geometry import Polygon, box

with open("tasks/day9/input.txt") as f:
    points = [tuple(map(int, line.strip().split(','))) for line in f if line.strip()]

polygon = Polygon(points)

max_area = 0
n = len(points)

for i in range(n):
    for j in range(i + 1, n):
        x1, y1 = points[i]
        x2, y2 = points[j]
        if x1 == x2 or y1 == y2:
            continue
        rx_min, rx_max = min(x1, x2), max(x1, x2)
        ry_min, ry_max = min(y1, y2), max(y1, y2)
        rect = box(rx_min, ry_min, rx_max, ry_max)
        if polygon.covers(rect):
            area = (rx_max - rx_min + 1) * (ry_max - ry_min + 1)
            if area > max_area:
                max_area = area

print(max_area)