from collections import defaultdict

points = []
with open("tasks/day9/input.txt") as f:
    for line in f:
        line = line.strip()
        if line:
            x, y = map(int, line.split(","))
            points.append((x, y))

n = len(points)

horiz = defaultdict(list)
verts = []

for i in range(n):
    x1, y1 = points[i]
    x2, y2 = points[(i + 1) % n]
    if y1 == y2:
        if x1 > x2:
            x1, x2 = x2, x1
        horiz[y1].append((x1, x2))
    else:
        if y1 > y2:
            y1, y2 = y2, y1
        verts.append((x1, y1, y2))

def merge_intervals(intervals):
    if not intervals:
        return []
    intervals.sort()
    merged = [list(intervals[0])]
    for l, r in intervals[1:]:
        if l <= merged[-1][1] + 1:
            if r > merged[-1][1]:
                merged[-1][1] = r
        else:
            merged.append([l, r])
    return [(l, r) for l, r in merged]

xs = sorted({x for x, _ in points})
ys = sorted({y for _, y in points})

# Build x runs (single vertex columns and gaps between them)
x_runs = []
x_to_run = {}
for i, x in enumerate(xs):
    x_to_run[x] = len(x_runs)
    x_runs.append((x, x, 1))
    if i + 1 < len(xs):
        gap = xs[i + 1] - x - 1
        if gap > 0:
            x_runs.append((x + 1, xs[i + 1] - 1, gap))

# Precompute slab intervals for open bands between consecutive y values
slab_intervals = []
for i in range(len(ys) - 1):
    y_low = ys[i]
    y_high = ys[i + 1]
    active_x = []
    for x, a, b in verts:
        if a < y_high and b > y_low:
            active_x.append(x)
    active_x.sort()
    intervals = []
    for j in range(0, len(active_x), 2):
        intervals.append((active_x[j], active_x[j + 1]))
    slab_intervals.append(intervals)

# Build y runs and row intervals
y_runs = []
y_to_run = {}
for i, y in enumerate(ys):
    intervals = []
    if i > 0:
        intervals.extend(slab_intervals[i - 1])
    if i < len(ys) - 1:
        intervals.extend(slab_intervals[i])
    intervals.extend(horiz.get(y, []))
    intervals = merge_intervals(intervals)

    y_to_run[y] = len(y_runs)
    y_runs.append((y, y, 1, intervals))

    if i + 1 < len(ys):
        gap = ys[i + 1] - y - 1
        if gap > 0:
            y_runs.append((y + 1, ys[i + 1] - 1, gap, slab_intervals[i]))

R = len(y_runs)
C = len(x_runs)

# Build boolean matrix of allowed compressed cells
grid = []
for _, _, _, intervals in y_runs:
    row = bytearray(C)
    p = 0
    for c, (a, b, _) in enumerate(x_runs):
        while p < len(intervals) and intervals[p][1] < a:
            p += 1
        if p < len(intervals):
            l, r = intervals[p]
            if a >= l and b <= r:
                row[c] = 1
    grid.append(row)

# Prefix sum of blocked cells
ps = [[0] * (C + 1) for _ in range(R + 1)]
for r in range(R):
    row_sum = 0
    gr = grid[r]
    psr1 = ps[r + 1]
    psr = ps[r]
    for c in range(C):
        row_sum += 1 - gr[c]
        psr1[c + 1] = psr[c + 1] + row_sum

def rect_blocked(r1, c1, r2, c2):
    return (
        ps[r2 + 1][c2 + 1]
        - ps[r1][c2 + 1]
        - ps[r2 + 1][c1]
        + ps[r1][c1]
    )

best = 0
for i in range(n):
    x1, y1 = points[i]
    c1 = x_to_run[x1]
    r1 = y_to_run[y1]
    for j in range(i + 1, n):
        x2, y2 = points[j]
        c2 = x_to_run[x2]
        r2 = y_to_run[y2]
        if c1 > c2:
            lc, rc = c2, c1
        else:
            lc, rc = c1, c2
        if r1 > r2:
            tr, br = r2, r1
        else:
            tr, br = r1, r2
        if rect_blocked(tr, lc, br, rc) == 0:
            area = (abs(x1 - x2) + 1) * (abs(y1 - y2) + 1)
            if area > best:
                best = area

print(best)