def solve():
    with open("tasks/day8/input.txt") as f:
        points = []
        for line in f:
            line = line.strip()
            if line:
                x, y, z = map(int, line.split(","))
                points.append((x, y, z))

    n = len(points)

    parent = list(range(n))
    size = [1] * n

    def find(a):
        while parent[a] != a:
            parent[a] = parent[parent[a]]
            a = parent[a]
        return a

    def union(a, b):
        a, b = find(a), find(b)
        if a == b:
            return
        if size[a] < size[b]:
            a, b = b, a
        parent[b] = a
        size[a] += size[b]

    distances = []
    for i in range(n):
        for j in range(i + 1, n):
            dx = points[i][0] - points[j][0]
            dy = points[i][1] - points[j][1]
            dz = points[i][2] - points[j][2]
            distances.append((dx*dx + dy*dy + dz*dz, i, j))

    distances.sort()

    for k in range(min(1000, len(distances))):
        _, i, j = distances[k]
        union(i, j)

    circuit_sizes = sorted(
        [size[find(i)] for i in range(n) if find(i) == i],
        reverse=True
    )

    print(circuit_sizes[0] * circuit_sizes[1] * circuit_sizes[2])

solve()