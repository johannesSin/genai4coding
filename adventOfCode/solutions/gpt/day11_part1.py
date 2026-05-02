from functools import lru_cache

graph = {}

with open("tasks/day11/input.txt", "r", encoding="utf-8") as f:
    for line in f:
        line = line.strip()
        if not line:
            continue
        node, rest = line.split(":")
        graph[node.strip()] = rest.strip().split()

@lru_cache(maxsize=None)
def count_paths(node):
    if node == "out":
        return 1
    return sum(count_paths(nxt) for nxt in graph.get(node, []))

print(count_paths("you"))