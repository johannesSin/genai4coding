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
            return False
        if size[a] < size[b]:
            a, b = b, a
        parent[b] = a
        size[a] += size[b]
        return True

    distances = []
    for i in range(n):
        for j in range(i + 1, n):
            dx = points[i][0] - points[j][0]
            dy = points[i][1] - points[j][1]
            dz = points[i][2] - points[j][2]
            distances.append((dx*dx + dy*dy + dz*dz, i, j))

    distances.sort()

    components = n
    last_i, last_j = None, None

    for _, i, j in distances:
        if union(i, j):
            components -= 1
            last_i, last_j = i, j
            if components == 1:
                break

    print(points[last_i][0] * points[last_j][0])

solve()