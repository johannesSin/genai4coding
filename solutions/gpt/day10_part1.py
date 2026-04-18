import re
from collections import deque

def parse_line(line):
    diagram = re.search(r'\[([.#]+)\]', line).group(1)
    target = 0
    for i, ch in enumerate(diagram):
        if ch == '#':
            target |= 1 << i

    buttons = []
    for part in re.findall(r'\((.*?)\)', line):
        mask = 0
        if part.strip():
            for x in part.split(','):
                x = x.strip()
                if x:
                    mask ^= 1 << int(x)
        buttons.append(mask)
    return len(diagram), target, buttons

def rref_solve(n, buttons, target):
    m = len(buttons)
    rows = []
    rhs = []
    for i in range(n):
        row = 0
        bit = 1 << i
        for j, b in enumerate(buttons):
            if b & bit:
                row |= 1 << j
        rows.append(row)
        rhs.append((target >> i) & 1)

    pivot_cols = []
    r = 0
    for c in range(m):
        pivot = None
        for i in range(r, n):
            if (rows[i] >> c) & 1:
                pivot = i
                break
        if pivot is None:
            continue
        rows[r], rows[pivot] = rows[pivot], rows[r]
        rhs[r], rhs[pivot] = rhs[pivot], rhs[r]
        for i in range(n):
            if i != r and ((rows[i] >> c) & 1):
                rows[i] ^= rows[r]
                rhs[i] ^= rhs[r]
        pivot_cols.append(c)
        r += 1
        if r == n:
            break

    for i in range(r, n):
        if rows[i] == 0 and rhs[i]:
            return None

    pivot_set = set(pivot_cols)
    free_cols = [c for c in range(m) if c not in pivot_set]

    particular = 0
    row_of_pivot = {}
    for row_idx, c in enumerate(pivot_cols):
        row_of_pivot[c] = row_idx
        if rhs[row_idx]:
            particular |= 1 << c

    kernel = []
    for f in free_cols:
        vec = 1 << f
        for c in pivot_cols:
            row_idx = row_of_pivot[c]
            if (rows[row_idx] >> f) & 1:
                vec |= 1 << c
        kernel.append(vec)

    return particular, kernel

def min_by_kernel(particular, kernel):
    k = len(kernel)
    if k > 24:
        return None
    cur = particular
    best = cur.bit_count()
    prev_gray = 0
    for i in range(1, 1 << k):
        gray = i ^ (i >> 1)
        diff = gray ^ prev_gray
        idx = diff.bit_length() - 1
        cur ^= kernel[idx]
        w = cur.bit_count()
        if w < best:
            best = w
        prev_gray = gray
    return best

def build_basis(vectors):
    basis = {}
    order = []
    for v in vectors:
        x = v
        for p in sorted(basis.keys(), reverse=True):
            if (x >> p) & 1:
                x ^= basis[p][0]
        if x:
            p = x.bit_length() - 1
            basis[p] = (x, len(order))
            order.append((p, x))
    return basis, len(order)

def encode_with_basis(v, basis):
    coeff = 0
    x = v
    for p in sorted(basis.keys(), reverse=True):
        if (x >> p) & 1:
            b, idx = basis[p]
            x ^= b
            coeff ^= 1 << idx
    if x:
        return None
    return coeff

def min_by_bfs(buttons, target):
    basis, r = build_basis(buttons)
    if r > 24:
        return None
    encoded_buttons = []
    seen = set()
    for b in buttons:
        e = encode_with_basis(b, basis)
        if e and e not in seen:
            seen.add(e)
            encoded_buttons.append(e)
    t = encode_with_basis(target, basis)
    if t is None:
        return None
    if t == 0:
        return 0

    dist = [-1] * (1 << r)
    q = deque([0])
    dist[0] = 0
    while q:
        s = q.popleft()
        d = dist[s] + 1
        for b in encoded_buttons:
            ns = s ^ b
            if dist[ns] == -1:
                if ns == t:
                    return d
                dist[ns] = d
                q.append(ns)
    return None

def min_by_mitm(buttons, target):
    m = len(buttons)
    if m > 46:
        return None
    a = buttons[:m // 2]
    b = buttons[m // 2:]

    left = {0: 0}
    for mask in a:
        updates = []
        for x, c in left.items():
            nx = x ^ mask
            nc = c + 1
            if nx not in left or nc < left[nx]:
                updates.append((nx, nc))
        for nx, nc in updates:
            if nx not in left or nc < left[nx]:
                left[nx] = nc

    best = None
    right = {0: 0}
    for mask in b:
        updates = []
        for x, c in right.items():
            nx = x ^ mask
            nc = c + 1
            if nx not in right or nc < right[nx]:
                updates.append((nx, nc))
        for nx, nc in updates:
            if nx not in right or nc < right[nx]:
                right[nx] = nc

    for x, c in right.items():
        need = x ^ target
        if need in left:
            total = c + left[need]
            if best is None or total < best:
                best = total
    return best

def solve_machine(n, target, buttons):
    res = rref_solve(n, buttons, target)
    if res is not None:
        particular, kernel = res
        ans = min_by_kernel(particular, kernel)
        if ans is not None:
            return ans

    ans = min_by_bfs(buttons, target)
    if ans is not None:
        return ans

    ans = min_by_mitm(buttons, target)
    if ans is not None:
        return ans

    raise RuntimeError("No solution method applicable")

total = 0
with open("tasks/day10/input.txt") as f:
    for line in f:
        line = line.strip()
        if not line:
            continue
        n, target, buttons = parse_line(line)
        total += solve_machine(n, target, buttons)

print(total)