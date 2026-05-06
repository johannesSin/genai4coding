def largest_k_subsequence(s, k):
    n = len(s)
    result = []
    start = 0
    for i in range(k):
        # From start, we can pick at most (n - start) digits
        # We need to pick (k - i) more digits total
        # So the current digit must come from s[start .. n-(k-i)]
        end = n - (k - i) + 1
        best_pos = start
        for j in range(start, end):
            if s[j] > s[best_pos]:
                best_pos = j
        result.append(s[best_pos])
        start = best_pos + 1
    return ''.join(result)

total = 0
with open("tasks/day3/input.txt") as f:
    for line in f:
        line = line.strip()
        if not line:
            continue
        total += int(largest_k_subsequence(line, 12))

print(total)