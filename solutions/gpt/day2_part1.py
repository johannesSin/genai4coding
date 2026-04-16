def sum_arith(a, b):
    if a > b:
        return 0
    return (a + b) * (b - a + 1) // 2

with open("tasks/day2/input.txt", "r", encoding="utf-8") as f:
    data = f.read().strip()

total = 0

for part in data.replace("\n", "").split(","):
    if not part:
        continue
    left, right = map(int, part.split("-"))

    for k in range(1, 20):
        mul = 10**k + 1
        lo = max(10**(k - 1), (left + mul - 1) // mul)
        hi = min(10**k - 1, right // mul)
        if lo <= hi:
            total += mul * sum_arith(lo, hi)

print(total)