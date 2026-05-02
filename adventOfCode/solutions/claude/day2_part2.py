with open("tasks/day2/input.txt") as f:
    data = f.read().strip()

def is_invalid(n):
    s = str(n)
    length = len(s)
    for seg_len in range(1, length // 2 + 1):
        if length % seg_len == 0:
            seg = s[:seg_len]
            if seg * (length // seg_len) == s:
                return True
    return False

total = 0
for r in data.split(","):
    r = r.strip()
    if not r:
        continue
    lo, hi = map(int, r.split("-"))
    for n in range(lo, hi + 1):
        if is_invalid(n):
            total += n

print(total)