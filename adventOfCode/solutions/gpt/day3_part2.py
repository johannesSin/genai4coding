def best_value(s: str, k: int = 12) -> int:
    drop = len(s) - k
    stack = []
    for ch in s:
        while drop and stack and stack[-1] < ch:
            stack.pop()
            drop -= 1
        stack.append(ch)
    if drop:
        stack = stack[:-drop]
    return int("".join(stack[:k]))


total = 0
with open("tasks/day3/input.txt", "r", encoding="utf-8") as f:
    for line in f:
        s = line.strip()
        if s:
            total += best_value(s)

print(total)