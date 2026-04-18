from pathlib import Path
import heapq

points = []
for line in Path("tasks/day8/input.txt").read_text().splitlines():
    if line.strip():
        points.append(tuple(map(int, line.split(","))))

k = 1000
heap = []

n = len(points)
for i in range(n):
    x1, y1, z1 = points[i]
    for j in range(i + 1, n):
        x2, y2, z2 = points[j]
        dx = x1 - x2
        dy = y1 - y2
        dz = z1 - z2
        d = dx * dx + dy * dy + dz * dz
        item = (-d, i, j)
        if len(heap) < k:
            heapq.heappush(heap, item)
        elif d < -heap[0][0]:
            heapq.heapreplace(heap, item)

pairs = sorted((-neg_d, i, j) for neg_d, i, j in heap)

parent = list(range(n))
size = [1] * n

def find(x):
    while parent[x] != x:
        parent[x] = parent[parent[x]]
        x = parent[x]
    return x

def union(a, b):
    ra = find(a)
    rb = find(b)
    if ra == rb:
        return
    if size[ra] < size[rb]:
        ra, rb = rb, ra
    parent[rb] = ra
    size[ra] += size[rb]

for _, i, j in pairs:
    union(i, j)

components = []
for i in range(n):
    if find(i) == i:
        components.append(size[i])

components.sort(reverse=True)
print(components[0] * components[1] * components[2])