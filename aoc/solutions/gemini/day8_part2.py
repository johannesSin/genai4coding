import math

def solve():
    nodes = []
    try:
        with open('tasks/day8/input.txt', 'r') as f:
            for line in f:
                line = line.strip()
                if line:
                    nodes.append(tuple(map(int, line.split(','))))
    except FileNotFoundError:
        return

    num_nodes = len(nodes)
    if num_nodes < 2:
        return

    edges = []
    for i in range(num_nodes):
        for j in range(i + 1, num_nodes):
            x1, y1, z1 = nodes[i]
            x2, y2, z2 = nodes[j]
            dist_sq = (x1 - x2)**2 + (y1 - y2)**2 + (z1 - z2)**2
            edges.append((dist_sq, i, j))

    edges.sort()

    parent = list(range(num_nodes))
    num_circuits = num_nodes

    def find(i):
        if parent[i] == i:
            return i
        parent[i] = find(parent[i])
        return parent[i]

    def union(i, j):
        root_i = find(i)
        root_j = find(j)
        if root_i != root_j:
            parent[root_i] = root_j
            return True
        return False

    for _, u, v in edges:
        if union(u, v):
            num_circuits -= 1
            if num_circuits == 1:
                print(nodes[u][0] * nodes[v][0])
                break

if __name__ == "__main__":
    solve()