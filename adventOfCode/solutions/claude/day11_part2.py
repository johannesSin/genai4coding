from collections import defaultdict
from functools import lru_cache

graph = defaultdict(list)

with open("tasks/day11/input.txt") as f:
    for line in f:
        line = line.strip()
        if not line:
            continue
        left, right = line.split(": ")
        graph[left].extend(right.split())

# Count paths from node to "out" that visit required nodes (as frozenset of remaining required)
@lru_cache(maxsize=None)
def count_paths(node, required_remaining):
    new_required = frozenset(r for r in required_remaining if r != node)
    if node == "out":
        return 1 if not new_required else 0
    return sum(count_paths(t, new_required) for t in graph[node])

print(count_paths("svr", frozenset(["dac", "fft"])))