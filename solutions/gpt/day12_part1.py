import re
from functools import lru_cache

def normalize(coords):
    min_x = min(x for x, y in coords)
    min_y = min(y for x, y in coords)
    return tuple(sorted((x - min_x, y - min_y) for x, y in coords))

def orientations(coords):
    out = set()
    for fx in (1, -1):
        for fy in (1, -1):
            pts = [(fx * x, fy * y) for x, y in coords]
            for _ in range(4):
                pts = [(y, -x) for x, y in pts]
                out.add(normalize(pts))
    return sorted(out)

def generate_placements(oris, w, h):
    placements = []
    seen = set()
    for ori in oris:
        max_x = max(x for x, y in ori)
        max_y = max(y for x, y in ori)
        for dx in range(w - max_x):
            for dy in range(h - max_y):
                m = 0
                for x, y in ori:
                    m |= 1 << ((dy + y) * w + (dx + x))
                if m not in seen:
                    seen.add(m)
                    placements.append(m)
    placements.sort(key=lambda x: (x.bit_count(), x))
    return placements

with open("tasks/day12/input.txt", "r", encoding="utf-8") as f:
    lines = [line.rstrip("\n") for line in f]

shape_rows = {}
regions = []
i = 0
while i < len(lines):
    line = lines[i].strip()
    if not line:
        i += 1
        continue
    if re.match(r"^\d+x\d+:", line):
        break
    m = re.match(r"^(\d+):$", line)
    if m:
        idx = int(m.group(1))
        i += 1
        rows = []
        while i < len(lines):
            s = lines[i].strip()
            if not s:
                i += 1
                break
            if re.match(r"^\d+:$", s) or re.match(r"^\d+x\d+:", s):
                break
            rows.append(s)
            i += 1
        shape_rows[idx] = rows
        continue
    i += 1

while i < len(lines):
    line = lines[i].strip()
    i += 1
    if not line:
        continue
    m = re.match(r"^(\d+)x(\d+):\s*(.*)$", line)
    if not m:
        continue
    w = int(m.group(1))
    h = int(m.group(2))
    counts = tuple(int(x) for x in m.group(3).split())
    regions.append((w, h, counts))

max_idx = max(shape_rows)
shapes = []
areas = []
for idx in range(max_idx + 1):
    rows = shape_rows[idx]
    coords = []
    for y, row in enumerate(rows):
        for x, ch in enumerate(row):
            if ch == "#":
                coords.append((x, y))
    shapes.append(orientations(coords))
    areas.append(len(coords))

placement_cache = {}

def can_fit(w, h, counts):
    board_cells = w * h
    total_area = sum(c * areas[t] for t, c in enumerate(counts))
    if total_area > board_cells:
        return False

    type_placements = []
    for t, c in enumerate(counts):
        if c == 0:
            type_placements.append(())
            continue
        key = (t, w, h)
        if key not in placement_cache:
            placement_cache[key] = tuple(generate_placements(shapes[t], w, h))
        pls = placement_cache[key]
        if not pls:
            return False
        type_placements.append(pls)

    @lru_cache(maxsize=None)
    def dfs(occ, remaining):
        free_cells = board_cells - occ.bit_count()
        rem_area = sum(remaining[t] * areas[t] for t in range(len(remaining)))
        if rem_area == 0:
            return True
        if free_cells < rem_area:
            return False

        best_t = -1
        best_valid = None

        for t, c in enumerate(remaining):
            if c == 0:
                continue
            valid = []
            for p in type_placements[t]:
                if not (p & occ):
                    valid.append(p)
            if not valid:
                return False
            if best_valid is None or len(valid) < len(best_valid):
                best_t = t
                best_valid = valid

        rem_list = list(remaining)
        rem_list[best_t] -= 1
        next_remaining = tuple(rem_list)

        for p in best_valid:
            if dfs(occ | p, next_remaining):
                return True
        return False

    return dfs(0, tuple(counts))

answer = sum(1 for w, h, counts in regions if can_fit(w, h, counts))
print(answer)