from functools import lru_cache

graph = {}

with open("tasks/day11/input.txt", "r", encoding="utf-8") as f:
    for line in f:
        line = line.strip()
        if not line:
            continue
        node, rest = line.split(":")
        graph[node.strip()] = rest.strip().split()

DAC = 1
FFT = 2
BOTH = DAC | FFT

@lru_cache(maxsize=None)
def count_paths(node, seen):
    if node == "out":
        return 1 if seen == BOTH else 0

    total = 0
    for nxt in graph.get(node, []):
        new_seen = seen
        if nxt == "dac":
            new_seen |= DAC
        if nxt == "fft":
            new_seen |= FFT
        total += count_paths(nxt, new_seen)
    return total

start_seen = 0
if "svr" == "dac":
    start_seen |= DAC
if "svr" == "fft":
    start_seen |= FFT

print(count_paths("svr", start_seen))