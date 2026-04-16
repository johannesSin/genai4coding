from functools import lru_cache

def sum_arith(a, b):
    return (a + b) * (b - a + 1) // 2 if a <= b else 0

@lru_cache(maxsize=None)
def divisors(n):
    ds = []
    for i in range(1, int(n ** 0.5) + 1):
        if n % i == 0:
            ds.append(i)
            if i * i != n:
                ds.append(n // i)
    ds.sort()
    return tuple(ds)

@lru_cache(maxsize=None)
def mobius(n):
    x = n
    p = 2
    cnt = 0
    while p * p <= x:
        if x % p == 0:
            x //= p
            if x % p == 0:
                return 0
            cnt += 1
            while x % p == 0:
                x //= p
        p += 1 if p == 2 else 2
    if x > 1:
        cnt += 1
    return -1 if cnt % 2 else 1

@lru_cache(maxsize=None)
def rep_multiplier(total_len, block_len):
    times = total_len // block_len
    base = 10 ** block_len
    return (base ** times - 1) // (base - 1)

@lru_cache(maxsize=None)
def primitive_sum_prefix(length, n):
    if n < 10 ** (length - 1):
        return 0
    upper = min(n, 10 ** length - 1)
    total = 0
    for d in divisors(length):
        mu = mobius(length // d)
        if mu == 0:
            continue
        mult = rep_multiplier(length, d)
        hi = min(10 ** d - 1, upper // mult)
        lo = 10 ** (d - 1)
        if lo <= hi:
            total += mu * mult * sum_arith(lo, hi)
    return total

def primitive_sum_interval(length, lo, hi):
    if lo > hi:
        return 0
    return primitive_sum_prefix(length, hi) - primitive_sum_prefix(length, lo - 1)

with open("tasks/day2/input.txt", "r", encoding="utf-8") as f:
    s = f.read().replace("\n", "").strip()

total = 0

for part in s.split(","):
    if not part:
        continue
    l, r = map(int, part.split("-"))
    max_len = len(str(r))
    for total_len in range(2, max_len + 1):
        for block_len in divisors(total_len):
            if block_len == total_len:
                continue
            mult = rep_multiplier(total_len, block_len)
            lo = max(10 ** (block_len - 1), (l + mult - 1) // mult)
            hi = min(10 ** block_len - 1, r // mult)
            if lo <= hi:
                total += mult * primitive_sum_interval(block_len, lo, hi)

print(total)