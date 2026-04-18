from collections import defaultdict

graph = defaultdict(list)

with open("tasks/day11/input.txt") as f:
    for line in f:
        line = line.strip()
        if not line:
            continue
        left, right = line.split(": ")
        targets = right.split()
        graph[left].extend(targets)

def count_paths(node, graph, memo={}):
    if node == "out":
        return 1
    if node in memo:
        return memo[node]
    total = sum(count_paths(t, graph, memo) for t in graph[node])
    memo[node] = total
    return total

print(count_paths("you", graph, {}))