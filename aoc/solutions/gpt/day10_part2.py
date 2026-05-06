import re
from functools import lru_cache

INF = 10**18

buttons = []
button_bits = []
button_indices_per_counter = []
n = 0

def parse_line(line):
    req = list(map(int, re.search(r"\{([^}]*)\}", line).group(1).split(",")))
    btns = []
    for part in re.findall(r"\((.*?)\)", line):
        mask = 0
        if part.strip():
            for x in part.split(","):
                mask |= 1 << int(x.strip())
        btns.append(mask)
    return req, btns

def support_indices(mask):
    out = []
    while mask:
        b = mask & -mask
        out.append(b.bit_length() - 1)
        mask ^= b
    return out

def count_options(target, ubs, cap=10**9):
    dp = [0] * (target + 1)
    dp[0] = 1
    for ub in ubs:
        ndp = [0] * (target + 1)
        window = 0
        for s in range(target + 1):
            window += dp[s]
            if s - ub - 1 >= 0:
                window -= dp[s - ub - 1]
            if window > cap:
                window = cap
            ndp[s] = window
        dp = ndp
    return dp[target]

def enumerate_assignments(covs, pos, residual):
    target = residual[pos]
    items = []
    for j in covs:
        ub = min(residual[k] for k in buttons[j])
        items.append((ub, j))
    items.sort()
    js = [j for _, j in items]
    ubs = [ub for ub, _ in items]
    sums = [0] * (len(ubs) + 1)
    for i in range(len(ubs) - 1, -1, -1):
        sums[i] = sums[i + 1] + ubs[i]

    counts = [0] * len(js)

    def rec(idx, remain):
        if idx == len(js) - 1:
            if 0 <= remain <= ubs[idx]:
                counts[idx] = remain
                yield list(zip(js, counts))
            return
        lo = max(0, remain - sums[idx + 1])
        hi = min(ubs[idx], remain)
        for x in range(lo, hi + 1):
            counts[idx] = x
            yield from rec(idx + 1, remain - x)

    yield from rec(0, target)

def solve_machine(req, btn_masks):
    global buttons, button_bits, button_indices_per_counter, n
    n = len(req)

    uniq = []
    seen = set()
    for m in btn_masks:
        if m and m not in seen:
            seen.add(m)
            uniq.append(m)

    buttons = [support_indices(m) for m in uniq]
    button_bits = uniq
    button_indices_per_counter = [[] for _ in range(n)]
    for j, inds in enumerate(buttons):
        for i in inds:
            button_indices_per_counter[i].append(j)

    @lru_cache(maxsize=None)
    def dp(residual):
        residual = list(residual)
        while True:
            zero_mask = 0
            for i, v in enumerate(residual):
                if v == 0:
                    zero_mask |= 1 << i

            usable = [j for j, m in enumerate(button_bits) if (m & zero_mask) == 0]

            if all(v == 0 for v in residual):
                return 0

            covers = [[] for _ in range(n)]
            for j in usable:
                for i in buttons[j]:
                    covers[i].append(j)

            for i, v in enumerate(residual):
                if v > 0 and not covers[i]:
                    return INF

            forced = []
            for i, v in enumerate(residual):
                if v > 0 and len(covers[i]) == 1:
                    forced.append((covers[i][0], v))

            if not forced:
                break

            need = {}
            for j, v in forced:
                if j in need and need[j] != v:
                    return INF
                need[j] = v

            added = 0
            for j, t in need.items():
                added += t
                for i in buttons[j]:
                    residual[i] -= t
                    if residual[i] < 0:
                        return INF

            sub = dp(tuple(residual))
            return added + sub if sub < INF else INF

        best_pos = None
        best_score = None
        best_covs = None

        for i, v in enumerate(residual):
            if v == 0:
                continue
            covs = covers[i]
            ubs = [min(residual[k] for k in buttons[j]) for j in covs]
            score = (count_options(v, sorted(ubs), cap=10**6), len(covs), v)
            if best_score is None or score < best_score:
                best_score = score
                best_pos = i
                best_covs = covs

        ans = INF
        base_cost = residual[best_pos]

        for assignment in enumerate_assignments(best_covs, best_pos, residual):
            nxt = residual[:]
            ok = True
            for j, cnt in assignment:
                if cnt:
                    for i in buttons[j]:
                        nxt[i] -= cnt
                        if nxt[i] < 0:
                            ok = False
                            break
                    if not ok:
                        break
            if ok:
                sub = dp(tuple(nxt))
                if sub < INF:
                    cand = base_cost + sub
                    if cand < ans:
                        ans = cand
        return ans

    return dp(tuple(req))

total = 0
with open("tasks/day10/input.txt", "r") as f:
    for line in f:
        line = line.strip()
        if line:
            req, btns = parse_line(line)
            total += solve_machine(req, btns)

print(total)