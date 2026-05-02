with open("tasks/day5/input.txt") as f:
    content = f.read()

ranges_section = content.strip().split("\n\n")[0].strip().splitlines()

ranges = []
for line in ranges_section:
    a, b = line.strip().split("-")
    ranges.append((int(a), int(b)))

ranges.sort()
merged = []
for lo, hi in ranges:
    if merged and lo <= merged[-1][1] + 1:
        merged[-1] = (merged[-1][0], max(merged[-1][1], hi))
    else:
        merged.append([lo, hi])

print(sum(hi - lo + 1 for lo, hi in merged))