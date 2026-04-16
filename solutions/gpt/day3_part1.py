def max_bank_value(s: str) -> int:
    digits = [ord(c) - 48 for c in s]
    suffix_max = [0] * len(digits)
    suffix_max[-1] = digits[-1]
    for i in range(len(digits) - 2, -1, -1):
        suffix_max[i] = max(digits[i], suffix_max[i + 1])

    best = 0
    for i in range(len(digits) - 1):
        best = max(best, digits[i] * 10 + suffix_max[i + 1])
    return best


total = 0
with open("tasks/day3/input.txt", "r", encoding="utf-8") as f:
    for line in f:
        s = line.strip()
        if s:
            total += max_bank_value(s)

print(total)