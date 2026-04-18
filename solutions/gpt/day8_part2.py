from pathlib import Path

points = []
for line in Path("tasks/day8/input.txt").read_text().splitlines():
    if line.strip():
        points.append(tuple(map(int, line.split(","))))

n = len(points)
edges = []

for i in range(n):
    x1, y1, z1 = points[i]
    for j in range(i + 1, n):
        x2, y2, z2 = points[j]
        dx = x1 - x2
        dy = y1 - y2
        dz = z1 - z2
        d = dx * dx + dy * dy + dz * dz
        edges.append((d, i, j))

edges.sort()

parent = list(range(n))
size = [1] * n

def find(x):
    while parent[x] != x:
        parent[x] = parent[parent[x]]
        x = parent[x]
    return x

components = n
answer = None

for _, a, b in edges:
    ra = find(a)
    rb = find(b)
    if ra == rb:
        continue
    if size[ra] < size[rb]:
        ra, rb = rb, ra
    parent[rb] = ra
    size[ra] += size[rb]
    components -= 1
    if components == 1:
        answer = points[a][0] * points[b][0]
        break

print(answer)