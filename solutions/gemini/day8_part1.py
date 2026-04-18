import math
import heapq

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
    edges = []
    for i in range(num_nodes):
        for j in range(i + 1, num_nodes):
            x1, y1, z1 = nodes[i]
            x2, y2, z2 = nodes[j]
            dist_sq = (x1 - x2)**2 + (y1 - y2)**2 + (z1 - z2)**2
            edges.append((dist_sq, i, j))

    edges.sort()

    parent = list(range(num_nodes))
    size = [1] * num_nodes

    def find(i):
        if parent[i] == i:
            return i
        parent[i] = find(parent[i])
        return parent[i]

    def union(i, j):
        root_i = find(i)
        root_j = find(j)
        if root_i != root_j:
            if size[root_i] < size[root_j]:
                root_i, root_j = root_j, root_i
            parent[root_j] = root_i
            size[root_i] += size[root_j]
            return True
        return False

    connections_made = 0
    for _, u, v in edges:
        if connections_made >= 1000:
            break
        union(u, v)
        connections_made += 1

    final_sizes = []
    roots = set()
    for i in range(num_nodes):
        root = find(i)
        if root not in roots:
            roots.add(root)
            final_sizes.append(size[root])

    final_sizes.sort(reverse=True)
    
    result = 1
    for i in range(min(3, len(final_sizes))):
        result *= final_sizes[i]
    
    print(result)

if __name__ == "__main__":
    solve()